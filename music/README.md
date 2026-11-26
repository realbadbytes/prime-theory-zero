# Gate soundtrack — your own music goes here

Drop audio files you have the rights to **play** and they replace the
built-in procedural chiptune during gate trials:

- `music/gate3.mp3` — claims one track for one gate (loops just it).
- any other `music/*.mp3|ogg|wav|flac` — general pool; each gate rotates
  through the whole pool starting at *its prime index* (gate N starts at
  track  p(N+2) mod count ), so every gate "hears the album" from a
  different deterministic place.
- `music/fanfare.*` — overrides the victory jingle on a perfect pass.

Everything here except this README is **git-ignored on purpose.**

## Licensing — read this once

The repo ships zero third-party audio and stays that way. Playing a
track while you study is personal use; **committing** it to a public
MIT/CC repository is redistribution, which almost no commercial music
permits. So:

- Bought it (Bandcamp, etc.)? Files here. Never in git. Example: the
  *Wayward Souls* OST by Joey Grady — sold at joeygrady.bandcamp.com,
  all rights reserved — is a great study-album; keep it local.
- Ripping streams (YouTube & co.) violates the platforms' terms; don't
  put ripped files in a public repo, and don't ask this repo to ship them.
- Want shareable music? Use genuinely free sources: OpenGameArt.org,
  itch.io (CC-BY collections), archive.org (CC audio) — and credit the
  artist in a `music/ATTRIBUTION.txt` if you fork this repo publicly.
