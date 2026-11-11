"""Command-line orchestration and interactive shell."""

import argparse
import shlex
import shutil
import sys
from pathlib import Path

from . import __version__
from .config import DB_PATH
from .lyrics import fetch
from .models import Media
from .player import play
from .providers import search
from .storage import Storage
from .ui import print_media


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        prog="terminal-music",
        description="Open-source YouTube and YouTube Music client for the terminal.",
    )
    cli.add_argument("--version", action="version", version=f"terminal-music {__version__}")
    commands = cli.add_subparsers(dest="command")
    for name, kind in (("search", "video"), ("music", "music")):
        command = commands.add_parser(name, help=f"Search YouTube {kind}")
        command.add_argument("query", nargs="+")
        command.add_argument("-n", "--limit", type=int, default=10)
    chart = commands.add_parser("chart", help="Search popular music by region")
    chart.add_argument("country", nargs="*", default=[])
    chart.add_argument("-n", "--limit", type=int, default=20)
    play_command = commands.add_parser("play", help="Search and play media")
    play_command.add_argument("query", nargs="+")
    play_command.add_argument("--video", action="store_true")
    play_command.add_argument("--speed", type=float, default=1.0)
    play_command.add_argument("--pitch", type=float, default=0.0)
    play_command.add_argument("--normalize", action="store_true")
    local = commands.add_parser("local", help="Play a local audio file")
    local.add_argument("path")
    lyrics = commands.add_parser("lyrics", help="Fetch lyrics for a song")
    lyrics.add_argument("query", nargs="+")
    commands.add_parser("next", help="Play and remove the first queued item")
    commands.add_parser("queue", help="Show the playback queue")
    queue_add = commands.add_parser("queue-add", help="Search and add media to the queue")
    queue_add.add_argument("query", nargs="+")
    queue_add.add_argument("-n", "--limit", type=int, default=1)
    commands.add_parser("queue-clear", help="Clear the playback queue")
    commands.add_parser("library", help="Show saved media")
    like = commands.add_parser("like", help="Search and save media")
    like.add_argument("query", nargs="+")
    unlike = commands.add_parser("unlike", help="Remove a saved URL")
    unlike.add_argument("url")
    commands.add_parser("history", help="Show playback history")
    commands.add_parser("stats", help="Show local listening statistics")
    playlist = commands.add_parser("playlist", help="Manage local playlists")
    playlist.add_argument("action", choices=("list", "create", "show", "add"))
    playlist.add_argument("name", nargs="?")
    playlist.add_argument("query", nargs="*")
    subscribe = commands.add_parser("subscribe", help="Follow a channel locally")
    subscribe.add_argument("channel")
    unsubscribe = commands.add_parser("unsubscribe", help="Unfollow a channel")
    unsubscribe.add_argument("channel")
    commands.add_parser("subscriptions", help="Show followed channels")
    commands.add_parser("doctor", help="Check runtime dependencies")
    commands.add_parser("interactive", aliases=["shell", "chat"], help="Start the interactive client")
    return cli


def row_media(row: object) -> Media:
    return Media(row["title"], row["url"], row["channel"] or "", row["duration"] or "", row["kind"])


def first(items: list[Media]) -> Media:
    if not items:
        raise RuntimeError("No media found.")
    return items[0]


def execute(args: argparse.Namespace, storage: Storage) -> int:
    command = args.command
    if command == "doctor":
        try:
            import yt_dlp  # noqa: F401
            youtube = "installed"
        except ImportError:
            youtube = "missing"
        print(f"yt-dlp: {youtube}")
        print(f"player: {shutil.which('mpv') or shutil.which('ffplay') or 'missing (URLs still work)'}")
        print(f"library: {DB_PATH}")
    elif command in {"search", "music"}:
        print_media(search(" ".join(args.query), max(1, args.limit), command))
    elif command == "chart":
        country = " ".join(args.country) or "global"
        print_media(search(f"YouTube Music top songs {country}", max(1, args.limit), "music"))
    elif command == "play":
        play(first(search(" ".join(args.query), 1)), storage, not args.video, args.speed, args.pitch, args.normalize)
    elif command == "local":
        path = Path(args.path).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"Local file does not exist: {path}")
        play(Media(path.name, str(path), kind="local"), storage)
    elif command == "lyrics":
        title, artist, text = fetch(" ".join(args.query))
        print(f"{title}\n{artist}\n{'-' * 60}\n{text}")
    elif command == "queue-add":
        for item in search(" ".join(args.query), max(1, args.limit), "music"):
            storage.enqueue(item)
            print(f"Queued: {item.title}")
    elif command == "queue":
        print_media([row_media(row) for row in storage.queue()])
    elif command == "queue-clear":
        storage.clear_queue()
        print("Queue cleared.")
    elif command == "next":
        item = storage.pop_queue()
        if item:
            play(row_media(item), storage)
        else:
            print("Queue is empty.")
    elif command == "library":
        print_media([row_media(row) for row in storage.library()])
    elif command == "like":
        item = first(search(" ".join(args.query), 1))
        storage.save(item)
        print(f"Saved: {item.title}")
    elif command == "unlike":
        storage.remove(args.url)
        print("Removed from library.")
    elif command == "history":
        print_media([Media(row["title"], row["url"], row["channel"] or "") for row in storage.history()])
    elif command == "stats":
        rows = storage.history()
        print(f"Plays recorded: {len(rows)}")
        channels = {}
        for row in rows:
            channel = row["channel"] or "Unknown"
            channels[channel] = channels.get(channel, 0) + 1
        for channel, count in sorted(channels.items(), key=lambda item: (-item[1], item[0]))[:10]:
            print(f"  {count:>3}  {channel}")
    elif command == "playlist":
        if args.action == "list":
            for row in storage.playlists():
                print(row["name"])
        elif not args.name:
            raise ValueError("A playlist name is required.")
        elif args.action == "create":
            storage.create_playlist(args.name)
            print(f"Created playlist: {args.name}")
        elif args.action == "show":
            print_media([row_media(row) for row in storage.playlist_items(args.name)])
        else:
            item = first(search(" ".join(args.query), 1))
            storage.add_to_playlist(args.name, item)
            print(f"Added to {args.name}: {item.title}")
    elif command == "subscribe":
        storage.subscribe(args.channel)
        print(f"Subscribed locally: {args.channel}")
    elif command == "unsubscribe":
        storage.unsubscribe(args.channel)
        print(f"Unsubscribed locally: {args.channel}")
    elif command == "subscriptions":
        for row in storage.subscriptions():
            print(row["channel"])
    elif command in {"interactive", "shell", "chat", None}:
        return interactive(storage)
    return 0


def interactive(storage: Storage) -> int:
    print("\033[1;36mTerminal Music\033[0m — YouTube client for your terminal")
    print("Type help for commands or exit to quit.\n")
    cli = parser()
    commands = (
        "search ", "music ", "play ", "chart ", "queue", "queue-add ", "queue-clear",
        "next", "library", "like ", "unlike ", "history", "stats", "lyrics ", "local ",
        "playlist ", "subscribe ", "unsubscribe ", "subscriptions", "doctor",
    )
    while True:
        try:
            line = input("\033[1;35m tm>\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if line in {"exit", "quit", ":q"}:
            return 0
        if line in {"help", "?"}:
            cli.print_help()
            continue
        if not line:
            continue
        if not line.startswith(commands):
            line = f"search {line}"
        try:
            execute(cli.parse_args(shlex.split(line)), storage)
        except (RuntimeError, ValueError, IndexError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
        except SystemExit:
            pass


def main() -> int:
    try:
        return execute(parser().parse_args(), Storage(DB_PATH))
    except (RuntimeError, ValueError, IndexError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
