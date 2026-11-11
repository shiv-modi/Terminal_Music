"""SQLite-backed local library, queue, playlists, and history."""

import sqlite3
from pathlib import Path

from .models import Media


class Storage:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS media (
                url TEXT PRIMARY KEY, title TEXT NOT NULL, channel TEXT,
                duration TEXT, kind TEXT NOT NULL, added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY, url TEXT, title TEXT, channel TEXT,
                played_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS queue (
                position INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, title TEXT,
                channel TEXT, duration TEXT, kind TEXT
            );
            CREATE TABLE IF NOT EXISTS playlists (
                name TEXT PRIMARY KEY, created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS playlist_items (
                playlist TEXT, url TEXT, title TEXT, channel TEXT, duration TEXT, kind TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (playlist, url)
            );
            CREATE TABLE IF NOT EXISTS subscriptions (
                channel TEXT PRIMARY KEY, added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    def save(self, item: Media) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO media(url,title,channel,duration,kind) VALUES(?,?,?,?,?)",
            (item.url, item.title, item.channel, item.duration, item.kind),
        )
        self.db.commit()

    def remove(self, url: str) -> None:
        self.db.execute("DELETE FROM media WHERE url = ?", (url,))
        self.db.commit()

    def library(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM media ORDER BY added_at DESC"))

    def record_play(self, item: Media) -> None:
        self.db.execute(
            "INSERT INTO history(url,title,channel) VALUES(?,?,?)",
            (item.url, item.title, item.channel),
        )
        self.db.commit()

    def history(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM history ORDER BY played_at DESC LIMIT 50"))

    def enqueue(self, item: Media) -> None:
        self.db.execute(
            "INSERT INTO queue(url,title,channel,duration,kind) VALUES(?,?,?,?,?)",
            (item.url, item.title, item.channel, item.duration, item.kind),
        )
        self.db.commit()

    def queue(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM queue ORDER BY position"))

    def pop_queue(self) -> sqlite3.Row | None:
        item = self.db.execute("SELECT * FROM queue ORDER BY position LIMIT 1").fetchone()
        if item:
            self.db.execute("DELETE FROM queue WHERE position = ?", (item["position"],))
            self.db.commit()
        return item

    def clear_queue(self) -> None:
        self.db.execute("DELETE FROM queue")
        self.db.commit()

    def create_playlist(self, name: str) -> None:
        self.db.execute("INSERT OR IGNORE INTO playlists(name) VALUES(?)", (name,))
        self.db.commit()

    def add_to_playlist(self, name: str, item: Media) -> None:
        self.create_playlist(name)
        self.db.execute(
            "INSERT OR REPLACE INTO playlist_items(playlist,url,title,channel,duration,kind) VALUES(?,?,?,?,?,?)",
            (name, item.url, item.title, item.channel, item.duration, item.kind),
        )
        self.db.commit()

    def playlists(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT name FROM playlists ORDER BY name"))

    def playlist_items(self, name: str) -> list[sqlite3.Row]:
        return list(self.db.execute(
            "SELECT * FROM playlist_items WHERE playlist = ? ORDER BY added_at DESC", (name,)
        ))

    def subscribe(self, channel: str) -> None:
        self.db.execute("INSERT OR IGNORE INTO subscriptions(channel) VALUES(?)", (channel,))
        self.db.commit()

    def unsubscribe(self, channel: str) -> None:
        self.db.execute("DELETE FROM subscriptions WHERE channel = ?", (channel,))
        self.db.commit()

    def subscriptions(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT channel FROM subscriptions ORDER BY channel"))
