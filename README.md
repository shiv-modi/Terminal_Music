# Terminal Music

An open-source YouTube and YouTube Music client for the terminal. It is designed like a modern CLI application: one-shot commands for scripts, an interactive `tm>` shell for daily use, and a local SQLite library for saved media, history, queues, playlists, and subscriptions.

## Install

```bash
python -m pip install -r requirements.txt
```

Install [mpv](https://mpv.io/installation/) for playback. Without a player, the client prints the playable URL.

## Commands

```bash
python main.py search "lofi hip hop"
python main.py music "A.R. Rahman"
python main.py chart India
python main.py play "Daft Punk Get Lucky"
python main.py play "Daft Punk Get Lucky" --speed 1.1 --normalize
python main.py local ~/Music/song.flac
python main.py lyrics "Bohemian Rhapsody"

python main.py queue-add "ambient mix"
python main.py queue
python main.py next

python main.py like "favorite song"
python main.py library
python main.py history
python main.py stats

python main.py playlist create workouts
python main.py playlist add workouts "running mix"
python main.py playlist show workouts
python main.py subscribe "NPR Music"
python main.py subscriptions
```

Start the full terminal client with:

```bash
python main.py interactive
```

Inside the shell, commands such as `search`, `music`, `play`, `queue`, `library`, `playlist`, `subscribe`, and `help` are available. Plain text is treated as a search query.

## ArchiveTune-inspired features

The CLI includes the practical terminal equivalents of ArchiveTune’s player experience:

- Local audio files alongside YouTube playback
- Background-capable playback through `mpv`
- Speed, pitch, gapless playback, and loudness normalization controls
- Lyrics lookup through LRCLIB
- Local listening history and statistics
- Saved library, playlists, queue, and subscriptions
- A scriptable shell rather than a GUI-only workflow

Account switching, cloud playlist synchronization, Spotify import, Last.fm/ListenBrainz scrobbling, Discord presence, and live translated lyrics require separate authenticated integrations and are intentionally not represented as working features yet.

## Project structure

```text
main.py                 # executable entry point
terminal_music/
  cli.py                # commands and interactive shell
  config.py             # XDG application paths
  models.py             # media domain model
  providers.py          # YouTube/YouTube Music provider
  player.py             # mpv/ffplay playback adapter
  lyrics.py             # lyrics provider
  storage.py            # SQLite library, queue, and history
  ui.py                 # terminal rendering
```

## Data and scope

Local data is stored in `~/.local/share/terminal-music/library.db` (or `$XDG_DATA_HOME`). Public YouTube and YouTube Music search is provided by `yt-dlp`; playback is delegated to a local player. Local subscriptions and playlists are intentionally account-independent. Authenticated YouTube account sync can be added later without changing the CLI storage model.

## License

MIT
