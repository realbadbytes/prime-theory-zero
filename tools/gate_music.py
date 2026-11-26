#!/usr/bin/env python3
"""Gate-trial soundtrack: ethereal 8-bit chiptune, computed from primes.

Repository philosophy -- "computed, not quoted" -- applied to music.
Every gate has its own theme: the key root, tempo and arpeggio pattern
are derived from the N-th prime and the digits of pi; four layers
(pulse-wave pad, square arpeggio, sine bells, bass) run through a
dotted-eighth echo for the ethereal sheen. Zero audio assets shipped,
zero dependencies: synthesis is pure stdlib, playback uses any player
found on PATH (pw-play/paplay/aplay/ffplay/mpv) or falls back to
talking to ALSA directly through ctypes+libasound -- which means it
works even on a bare tty Linux box with a sound card and no PulseAudio.

Auto-start: `unlock.py grade N` starts the loop in a detached daemon;
passing the gate stops it and plays a victory fanfare. Manual:

    python3 unlock.py music status|stop|on|off
    python3 tools/gate_music.py render <gate|fanfare>   (write wav only)
    python3 tools/gate_music.py play <gate>             (foreground)

Env:  PTZ_MUSIC=0 disables entirely (also respected by the grader).
      PTZ_ALSA_DEVICE=hw:4,0   force an ALSA device.
      PTZ_MUSIC_MAXMIN=40      daemon hard stop (anti-orphan).

Own music: drop tracks you have the rights to play (your purchases,
CC-licensed chiptune, ...) into music/ -- they replace the synth and
rotate per gate starting at the gate's PRIME index, so every gate hears
the collection from a different deterministic place. Example: the
Wayward Souls OST by Joey Grady (joeygrady.bandcamp.com) is sold, not
free-licensed -- buy it, keep the files in music/ (git-ignored,
personal use), and NEVER commit audio you do not hold a redistribution
license for. music/gateN.* claims one track for one gate; music/
fanfare.* overrides the victory jingle. See music/README.md.

This repository ships ZERO third-party audio: everything not in the
git-ignored music/ folder is synthesized from mathematics on your
machine.
"""
import array
import ctypes
import ctypes.util
import json
import math
import os
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

SR = 44100
ROOT = Path(__file__).resolve().parent.parent
MUSIC_DIR = ROOT / "music"
CACHE = Path(os.environ.get("PTZ_MUSIC_CACHE", "/tmp/ptz-chiptune-v1"))
PIDF = CACHE / "music.pid"
STOPF = CACHE / "music.stop"
PI = "14159265358979323846264338327950288419716939937510582097"
SCALE_AEOLIAN = [0, 2, 3, 5, 7, 8, 10]
PROGRESSION = [0, 5, 2, 6]          # i - VI - III - VII (aeolian degrees)
ROOTS = [45, 48, 50, 52, 53, 55, 57, 43]   # A2 C3 D3 E3 F3 G3 A3 G2


# ------------------------------------------------------------------ config
def enabled() -> bool:
    env = os.environ.get("PTZ_MUSIC")
    if env is not None:
        return env != "0"
    cfg = ROOT / ".unlock_state" / "config.json"
    try:
        return json.loads(cfg.read_text()).get("music_enabled", True)
    except Exception:
        return True


def set_enabled(on: bool) -> None:
    cfg = ROOT / ".unlock_state" / "config.json"
    cfg.parent.mkdir(exist_ok=True)
    cfg.write_text(json.dumps({"music_enabled": bool(on)}, indent=2))


# ------------------------------------------------------------------ primes
def nth_prime(n: int) -> int:
    sieve, c = [True] * (n * (math.log(n) + math.log(math.log(n))) + 10
                         if n >= 6 else 15), 0
    for i in range(2, len(sieve)):
        if sieve[i]:
            c += 1
            if c == n:
                return i
            for j in range(i * i, len(sieve), i):
                sieve[j] = False
    raise ValueError(n)


# ------------------------------------------------------------- synthesis
def _midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def _wave_table(duty, harm):
    """Band-limited pulse cycle, 4096 samples (Fourier of a duty-cycle
    square: keeps the 8-bit bite without brutal aliasing)."""
    N = 4096
    tab = [0.0] * N
    for k in range(1, harm + 1):
        a = math.sin(math.pi * k * duty) / (math.pi * k)      # Fourier coeff
        if abs(a) < 1e-12:
            continue
        for i in range(N):
            tab[i] += 2.0 * a * math.sin(2 * math.pi * k * i / N)
    m = max(abs(v) for v in tab) or 1.0
    return [v / m for v in tab], N


def _osc(freq, n, tab, tablen, phase=0.0):
    out = [0.0] * n
    inc = freq * tablen / SR
    pos = phase
    for i in range(n):
        out[i] = tab[int(pos) & (tablen - 1)]
        pos += inc
        if pos >= tablen:
            pos -= tablen
    return out


def _adsr(n, a, peak_hold, d, sustain):
    env = [0.0] * n
    na, nh = max(1, int(n * a)), max(1, int(n * peak_hold))
    nd = max(1, n - na - nh)
    for i in range(min(na, n)):
        env[i] = i / na
    for i in range(na, min(na + nh, n)):
        env[i] = 1.0
    for i in range(na + nh, n):
        t = (i - na - nh) / max(1, nd)
        env[i] = (1.0 - t) * (1.0 - t) * (1.0 - sustain) + sustain * (1 - t)
    return env


def _add(buf, start, sig, gain):
    end = min(len(buf), start + len(sig))
    for i in range(end - start):
        buf[start + i] += sig[i] * gain


def gate_spec(gate):
    p = nth_prime(gate + 2)                       # gate 0 -> first prime 2...
    root = ROOTS[p % len(ROOTS)]
    bpm = 62 + (p % 7) * 5
    digits = [int(c) for c in PI[gate:gate + 32]]
    return p, root, bpm, digits


def render_gate(gate):
    """One seamless loop of the gate theme. Deterministic."""
    p, root, bpm, dig = gate_spec(gate)
    beat = 60.0 / bpm
    bar = 4 * beat
    loop_bars = 8
    cf = 1.5                                       # crossfade for the seam
    total = loop_bars * bar + cf
    n = int(total * SR)
    pad = [0.0] * n
    bass = [0.0] * n
    arpb = [0.0] * n
    bell = [0.0] * n

    pad_tab, PTL = _wave_table(0.3, 16)
    arp_tab, ATL = _wave_table(0.5, 10)
    bas_tab, BTL = _wave_table(0.35, 8)

    chord_midis = []
    for d in PROGRESSION:
        triad = []
        for off in (0, 2, 4):
            deg = (d + off) % 7
            octv = 12 * ((d + off) // 7)
            triad.append(root + SCALE_AEOLIAN[deg] + octv)
        chord_midis.append(triad)

    # ---- pad: two detuned pulse voices per 2-bar chord, slow attack
    for c in range(loop_bars // 2):
        seg = int(2 * bar * SR) + int(cf * SR * 0.4)
        st = int(c * 2 * bar * SR)
        for m in chord_midis[c % 4]:
            f = _midi_hz(m)
            for det, pan_gain in ((0.9963, 0.09), (1.0037, 0.07)):
                sig = _osc(f * det, seg, pad_tab, PTL)
                na = int(seg * 0.35)
                for i in range(seg):
                    if i < na:
                        sig[i] *= i / na
                    else:
                        sig[i] *= 1.0 - 0.4 * ((i - na) / seg) ** 2
                _add(pad, st, sig, pan_gain)

    # ---- bass: steady eighths on the chord root, two octaves down
    for step in range(loop_bars * 8):
        st = int(step * beat / 2 * SR)
        chord = chord_midis[(step // 8) % 4]
        f = _midi_hz(min(chord) - 24)
        ln = int(beat * 0.45 * SR)
        sig = _osc(f, ln, bas_tab, BTL)
        env = _adsr(ln, 0.02, 0.3, 0.7, 0.0)
        _add(bass, st, [s * e for s, e in zip(sig, env)], 0.115)

    # ---- arpeggio: sixteenths, contour from pi digits (math as melody)
    step16 = beat / 4
    for step in range(loop_bars * 16):
        if step % 16 in (dig[step % 32] % 16, (dig[(step + 7) % 32] + 3) % 16):
            continue                              # pi-gated rests breathe
        chord = chord_midis[(step // 16) % 4]
        m = chord[dig[step % 32] % 3] + 12 * (1 + dig[(step + 11) % 32] % 2)
        f = _midi_hz(m)
        st = int(step * step16 * SR)
        ln = int(beat * 0.7 * SR)
        sig = _osc(f, ln, arp_tab, ATL)
        env = _adsr(ln, 0.01, 0.15, 0.85, 0.0)
        pan = 0.20 if step % 2 else 0.24
        _add(arpb, st, [s * e for s, e in zip(sig, env)], pan)

    # ---- bells: sine sparkle only on steps coprime to 6 (prime motif)
    for step in range(loop_bars * 16):
        k = step % 16
        if k % 2 == 0 or k % 3 == 0:
            continue
        chord = chord_midis[(step // 16) % 4]
        f = _midi_hz(max(chord) + 24 + SCALE_AEOLIAN[step % 7] % 4)
        st = int(step * step16 * SR)
        ln = int(1.6 * SR)
        s1 = _osc(f, ln, pad_tab, PTL)            # reuse table (near-sine)
        dec = [math.exp(-4.2 * i / ln) for i in range(ln)]
        sig = [a * d for a, d in zip(s1, dec)]
        _add(bell, st, sig, 0.11 if (step // 16) % 2 else 0.13)

    # ---- echo (dotted-eighth comb + second tap) on arps & bells
    delay = int(0.75 * beat * SR)
    for bus in (arpb, bell):
        for i in range(delay, len(bus)):
            bus[i] += 0.42 * bus[i - delay]
        d2 = 2 * delay
        for i in range(d2, len(bus)):
            bus[i] += 0.16 * bus[i - d2]

    # ---- mix to stereo (Haas delay on the pad for width)
    haas = int(0.011 * SR)
    L = [0.0] * n
    R = [0.0] * n
    for i in range(n):
        a = pad[i]
        bassv = bass[i]
        mid = arpb[i] + bell[i]
        L[i] = a * 0.7 + bassv + mid
        R[i] = (pad[i - haas] if i >= haas else 0.0) * 0.7 + bassv + mid

    # ---- loop seam: crossfade the tail onto the head
    head = int(loop_bars * bar * SR)
    for i in range(int(cf * SR)):
        w = i / (cf * SR)
        j = head - int(cf * SR) + i
        if j >= 0:
            L[j] = L[j] * (1 - w) + L[head + i] * w
            R[j] = R[j] * (1 - w) + R[head + i] * w
    L, R = L[:head], R[:head]

    peak = max(max(abs(v) for v in L), max(abs(v) for v in R), 1e-9)
    g = 0.86 / peak
    out = array.array("h", [0]) * (2 * len(L))
    for i in range(len(L)):
        out[2 * i] = int(max(-1.0, min(1.0, math.tanh(1.15 * L[i] * g))) * 32767)
        out[2 * i + 1] = int(max(-1.0, min(1.0, math.tanh(1.15 * R[i] * g))) * 32767)
    return out


def render_fanfare():
    """'Level up': rising major pulse arpeggio + sustained chord."""
    total, n = 2.1, int(2.1 * SR)
    mix = [0.0] * (2 * n)
    tab, TL = _wave_table(0.5, 12)
    root = 69     # A4, bright
    seq = [0, 4, 7, 12, 16, 19]
    beat = 0.11
    for i, semi in enumerate(seq):
        st = int(i * beat * SR)
        ln = int(0.5 * SR)
        sig = _osc(_midi_hz(root + semi), ln, tab, TL)
        env = _adsr(ln, 0.01, 0.2, 0.8, 0.0)
        for j in range(ln):
            v = sig[j] * env[j] * 0.30
            mix[2 * (st + j)] += v
            mix[2 * (st + j) + 1] += v
    st = int(len(seq) * beat * SR)
    for semi in (12, 19, 24, 28):
        ln = int((2.05 - st / SR) * SR)
        sig = _osc(_midi_hz(root + semi), ln, tab, TL)
        for j in range(ln):
            v = sig[j] * 0.16 * min(1.0, j / (0.02 * SR)) * math.exp(-1.1 * j / ln)
            mix[2 * (st + j)] += v
            mix[2 * (st + j) + 1] += v
    d = int(0.12 * SR)
    for ch in (0, 1):
        for i in range(d, n):
            mix[2 * i + ch] += 0.35 * mix[2 * (i - d) + ch]
    peak = max(abs(v) for v in mix) or 1.0
    g = 0.9 / peak
    out = array.array("h", [0]) * (2 * n)
    for i in range(2 * n):
        out[i] = int(max(-1.0, min(1.0, math.tanh(1.2 * mix[i] * g))) * 32767)
    return out


def _write_wav(path, samples):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.wav")
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.tobytes())
    tmp.replace(path)


def render_gate_wav(gate, force=False):
    CACHE.mkdir(exist_ok=True)
    out = CACHE / f"gate{gate}.wav"
    if out.exists() and not force:
        return out
    user = _user_file(f"gate{gate}")
    if user:
        return user
    _write_wav(out, render_gate(gate))
    return out


def render_fanfare_wav(force=False):
    CACHE.mkdir(exist_ok=True)
    out = CACHE / "fanfare.wav"
    if out.exists() and not force:
        return out
    user = _user_file("fanfare")
    if user:
        return user
    _write_wav(out, render_fanfare())
    return out


def _user_file(stem):
    if not MUSIC_DIR.exists():
        return None
    for ext in (".wav", ".flac", ".ogg", ".mp3", ".m4a"):
        cand = MUSIC_DIR / f"{stem}{ext}"
        if cand.exists():
            return cand
    return None


# ------------------------------------------------------------- playback
EXTS = (".wav", ".mp3", ".ogg", ".oga", ".flac", ".m4a", ".mp4")


def _external_player():
    for name, extra in (("pw-play", []), ("paplay", []), ("aplay", []),
                        ("ffplay", ["-nodisp", "-autoexit", "-loglevel",
                                    "quiet"]),
                        ("mpv", ["--no-video", "--really-quiet"])):
        if shutil.which(name):
            return [name] + extra
    return None


# --------------------------------------------------------- ctypes decoders
class Mpg123In:
    """Streaming MP3 decoder via the system libmpg123 (on most distros)."""

    S16 = 0x0002                              # MPG123_ENC_SIGNED_16

    def __init__(self, path):
        self.lib = ctypes.CDLL("libmpg123.so.0")
        err = ctypes.c_int(0)
        self.lib.mpg123_new.restype = ctypes.c_void_p
        self.lib.mpg123_new.argtypes = [ctypes.c_char_p,
                                        ctypes.POINTER(ctypes.c_int)]
        self.h = self.lib.mpg123_new(None, ctypes.byref(err))
        if not self.h:
            raise RuntimeError(f"mpg123_new: {err.value}")
        self.lib.mpg123_open.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        if self.lib.mpg123_open(self.h, str(path).encode()):
            raise RuntimeError("mpg123_open failed")
        rate, ch, enc = ctypes.c_long(), ctypes.c_int(), ctypes.c_int()
        self.lib.mpg123_getformat(self.h, ctypes.byref(rate),
                                  ctypes.byref(ch), ctypes.byref(enc))
        if enc.value != self.S16:
            self.lib.mpg123_format_none(self.h)
            self.lib.mpg123_format(self.h, rate.value, ch.value, self.S16)
            self.lib.mpg123_getformat(self.h, ctypes.byref(rate),
                                      ctypes.byref(ch), ctypes.byref(enc))
        self.rate, self.channels = rate.value, ch.value
        if not self.rate or not self.channels:
            raise RuntimeError("mpg123: unknown format")

    def read(self, frames):
        buf = ctypes.create_string_buffer(frames * self.channels * 2)
        done = ctypes.c_size_t(0)
        self.lib.mpg123_read(self.h, buf, len(buf), ctypes.byref(done))
        return buf.raw[:done.value] if done.value else None

    def close(self):
        try:
            self.lib.mpg123_delete(self.h)
        except Exception:
            pass


class VorbisIn:
    """Streaming Ogg Vorbis decoder via the system libvorbisfile."""

    def __init__(self, path):
        self.lib = ctypes.CDLL("libvorbisfile.so.3")
        # OggVorbis_File is opaque; over-allocate generously.
        self.ov = (ctypes.c_char * 8192)()
        if self.lib.ov_fopen(str(path).encode(), ctypes.byref(self.ov)):
            raise RuntimeError("ov_fopen failed")
        info = self.lib.ov_info(ctypes.byref(self.ov), ctypes.c_long(-1))
        if not info:
            raise RuntimeError("ov_info failed")
        # vorbis_info: { int version; int channels; long rate; ... }
        self.channels = ctypes.cast(
            ctypes.byref(info.contents, 4),
            ctypes.POINTER(ctypes.c_int)).contents.value
        self.rate = ctypes.cast(
            ctypes.byref(info.contents, 8),
            ctypes.POINTER(ctypes.c_long)).contents.value

    def read(self, frames):
        buf = ctypes.create_string_buffer(frames * self.channels * 2)
        cur, eos = ctypes.c_int(0), ctypes.c_int(0)
        n = self.lib.ov_read(ctypes.byref(self.ov), buf, len(buf), 0,
                             ctypes.byref(cur), ctypes.byref(eos))
        return buf.raw[:n] if n > 0 else None

    def close(self):
        try:
            self.lib.ov_clear(ctypes.byref(self.ov))
        except Exception:
            pass


class AlsaOut:
    """Direct ALSA PCM output via ctypes -- no packages, no sound daemon."""

    def __init__(self):
        libname = ctypes.util.find_library("asound")
        if not libname:
            raise RuntimeError("libasound not found")
        self.lib = ctypes.CDLL(libname)
        self.pcm = None
        self.device = None

    @staticmethod
    def _prefer_device():
        dev = os.environ.get("PTZ_ALSA_DEVICE")
        if dev:
            return dev.encode()
        try:                                   # prefer USB audio: on many
            for line in Path("/proc/asound/cards").read_text().splitlines():
                if "USB-Audio" in line:        # boxes the HDMI cards are
                    idx = line.strip().split()[0]
                    return f"hw:{idx},0".encode()   # monitor-only
        except Exception:
            pass
        return b"default"

    def _unmute(self):
        """Best-effort: unmute + set 80% on every playback element of the
        chosen device (bare tty boxes have no alsamixer running)."""
        target = self.device.decode()
        if target.startswith("hw:"):            # mixer wants a card index
            target = target.split(":")[1].split(",")[0]
        try:
            h = ctypes.c_void_p()
            if self.lib.snd_mixer_open(ctypes.byref(h), 0):
                return
            for cand in dict.fromkeys((target, "default")):
                if not self.lib.snd_mixer_attach(h, cand.encode()):
                    break
            else:
                self.lib.snd_mixer_close(h)
                return
            self.lib.snd_mixer_selem_register(h, None, None)
            self.lib.snd_mixer_load(h)
            self.lib.snd_mixer_first_elem.restype = ctypes.c_void_p
            self.lib.snd_mixer_elem_next.restype = ctypes.c_void_p
            e = self.lib.snd_mixer_first_elem(h)
            while e:
                if self.lib.snd_mixer_selem_has_playback_switch(e):
                    self.lib.snd_mixer_selem_set_playback_switch_all(e, 1)
                if self.lib.snd_mixer_selem_has_playback_volume(e):
                    lo, hi = ctypes.c_long(), ctypes.c_long()
                    if not self.lib.snd_mixer_selem_get_playback_volume_range(
                            e, ctypes.byref(lo), ctypes.byref(hi)):
                        tgt = lo.value + int(0.8 * (hi.value - lo.value))
                        self.lib.snd_mixer_selem_set_playback_volume_all(e,
                                                                         tgt)
                e = self.lib.snd_mixer_elem_next(e)
            self.lib.snd_mixer_close(h)
        except Exception:
            pass

    def _open(self, rate, ch):
        lib = self.lib
        lib.snd_pcm_open.argtypes = [ctypes.POINTER(ctypes.c_void_p),
                                     ctypes.c_char_p, ctypes.c_int,
                                     ctypes.c_int]
        lib.snd_pcm_set_params.argtypes = [ctypes.c_void_p] + \
            [ctypes.c_uint] * 4 + [ctypes.c_int, ctypes.c_uint,
                                   ctypes.c_ulong]
        lib.snd_pcm_writei.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_ulong]
        lib.snd_pcm_writei.restype = ctypes.c_long
        lib.snd_pcm_recover.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                        ctypes.c_int]
        self.pcm = ctypes.c_void_p()
        tried = dict.fromkeys((self._prefer_device(), b"default", b"hw:0,0"))
        for dev in tried:
            if lib.snd_pcm_open(ctypes.byref(self.pcm), dev, 0, 0) == 0:
                self.device = dev
                break
        else:
            raise RuntimeError("no ALSA playback device")
        if lib.snd_pcm_set_params(self.pcm, 2, 3, ch, rate, 1, 100000,
                                  500000) < 0:
            lib.snd_pcm_close(self.pcm)
            self.pcm = None
            raise RuntimeError(f"device {self.device!r} rejected "
                               f"{rate} Hz / {ch} ch")
        self._unmute()

    def play_stream(self, reader, rate, ch, stop_check=None):
        """reader(frames) -> s16le bytes | None (stream end)."""
        self._open(rate, ch)
        lib = self.lib
        try:
            while True:
                if stop_check and stop_check():
                    lib.snd_pcm_drop(self.pcm)
                    return False
                data = reader(8192)
                if not data:
                    break
                buf = ctypes.create_string_buffer(data, len(data))
                off, tries = 0, 0
                while off < len(data) and tries < 30:
                    got = lib.snd_pcm_writei(
                        self.pcm,
                        ctypes.cast(ctypes.byref(buf, off), ctypes.c_void_p),
                        (len(data) - off) // (2 * ch))
                    if got < 0:
                        if lib.snd_pcm_recover(self.pcm, got, 0) < 0:
                            raise RuntimeError("ALSA write failed")
                        tries += 1
                    else:
                        off += got * 2 * ch
            lib.snd_pcm_drain(self.pcm)
            return True
        finally:
            if self.pcm:
                lib.snd_pcm_close(self.pcm)
                self.pcm = None

    def play_wav(self, path, stop_check=None):
        with wave.open(str(path)) as w:
            if w.getsampwidth() != 2:
                raise RuntimeError("need 16-bit wav")
            rate, ch = w.getframerate(), w.getnchannels()

            def rd(f, w=w):
                return w.readframes(f)

            return self.play_stream(rd, rate, ch, stop_check)


def play_one(path, stop_check=None):
    """Play one file through the best available route. False = impossible."""
    ext = Path(path).suffix.lower()
    if ext == ".wav" and ctypes.util.find_library("asound"):
        try:
            return AlsaOut().play_wav(path, stop_check)
        except Exception:
            pass
    player = _external_player()
    if player:
        try:
            subprocess.run(player + [str(path)],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=3600)
            return True
        except Exception:
            return False
    dec_cls = {".mp3": Mpg123In, ".ogg": VorbisIn,
               ".oga": VorbisIn}.get(ext)
    if dec_cls and ctypes.util.find_library("asound"):
        try:
            dec = dec_cls(path)
            try:
                return AlsaOut().play_stream(dec.read, dec.rate,
                                             dec.channels, stop_check)
            finally:
                dec.close()
        except Exception:
            return False
    return False


def _pool():
    """All user-provided tracks (everything in music/ except fanfare)."""
    if not MUSIC_DIR.exists():
        return []
    return sorted(p for p in MUSIC_DIR.iterdir()
                  if p.is_file() and p.suffix.lower() in EXTS
                  and not p.stem.startswith("fanfare"))


def playlist_for(gate):
    """Track rotation for a gate. A dedicated music/gateN.* wins outright;
    otherwise the whole pool rotates, starting at the gate's prime index
    (each gate hears the album from a different, deterministic place)."""
    per = _user_file(f"gate{gate}")
    if per:
        return [per]
    files = _pool()
    if not files:
        return []
    k = nth_prime(gate + 2) % len(files)
    return files[k:] + files[:k]


def music_available() -> bool:
    return _external_player() is not None or \
        ctypes.util.find_library("asound") is not None


def run_rotation(gate, deadline, foreground=False):
    """Loop the gate's playlist (or the procedural synth if no own music)
    until stop marker / deadline."""
    tracks = playlist_for(gate)
    i = 0
    while time.time() < deadline and not STOPF.exists():
        if tracks:
            ok = play_one(tracks[i % len(tracks)],
                          stop_check=STOPF.exists)
            i += 1 if ok else 0
        else:
            ok = play_one(render_gate_wav(gate), stop_check=STOPF.exists)
        if not ok:
            if foreground:
                raise RuntimeError("no working audio route: install "
                                   "mpv/ffplay/paplay or libasound, or "
                                   "set PTZ_MUSIC=0")
            time.sleep(5)
        time.sleep(0.2)


# ------------------------------------------------------------- daemon
def _pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def daemon_info():
    try:
        pid, gate = PIDF.read_text().split()
        pid = int(pid)
        if _pid_alive(pid):
            return pid, gate
    except Exception:
        pass
    return None, None


def stop():
    pid, _ = daemon_info()
    CACHE.mkdir(exist_ok=True)
    STOPF.touch()
    if pid:
        for sig in (15, 9):
            if not _pid_alive(pid):
                break
            try:
                os.kill(pid, sig)
            except OSError:
                break
            time.sleep(0.4)
    for f in (PIDF, STOPF, CACHE / "music.gate"):
        if f.exists():
            f.unlink()
    return pid is not None


def ensure_playing(gate):
    """Start the gate soundtrack daemon unless one is already running.
    True = newly started."""
    if not enabled() or not music_available():
        return False
    pid, g = daemon_info()
    if pid:
        if g == str(gate):
            return False
        stop()
    CACHE.mkdir(exist_ok=True)
    if not playlist_for(gate):
        render_gate_wav(gate)                 # pre-render so audio starts
    subprocess.Popen(                           # immediately, not after a
        [sys.executable, str(Path(__file__)),   # render stall in the
         "daemon", str(gate)],                  # student's hot seat
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    time.sleep(0.15)
    return True


def fanfare():
    if not enabled() or not music_available():
        return
    stop()
    subprocess.Popen([sys.executable, str(Path(__file__)), "once",
                      str(render_fanfare_wav())],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)


def status_dict():
    pid, gate = daemon_info()
    pool = _pool()
    return {
        "enabled": enabled(),
        "available": music_available(),
        "player": (" ".join(_external_player()) if _external_player()
                   else ("alsa-ctypes" if music_available() else "none")),
        "daemon_pid": pid, "daemon_gate": gate,
        "cache": str(CACHE),
        "own_music_tracks": len(pool),
        "own_music": [p.name for p in pool[:6]],
        "user_fanfare": bool(_user_file("fanfare")),
    }


# ------------------------------------------------------------- CLI
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "render":
        target = sys.argv[2]
        if target == "fanfare":
            print(render_fanfare_wav(force=True))
        else:
            print(render_gate_wav(int(target), force=True))
    elif cmd == "play":
        gate = int(sys.argv[2])
        pl = playlist_for(gate)
        print(f"gate {gate} soundtrack: "
              f"{len(pl)} own track(s) or procedural synth "
              f"(Ctrl-C to stop)")
        try:
            run_rotation(gate, time.time() + 10 ** 9, foreground=True)
        except KeyboardInterrupt:
            print("\nstopped")
    elif cmd == "daemon":
        gate = int(sys.argv[2])
        PIDF.write_text(f"{os.getpid()} {gate}")
        try:
            run_rotation(gate, time.time() + 60.0 * float(
                os.environ.get("PTZ_MUSIC_MAXMIN", "40")))
        finally:
            if PIDF.exists():
                PIDF.unlink()
    elif cmd == "once":
        play_one(sys.argv[2])
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
