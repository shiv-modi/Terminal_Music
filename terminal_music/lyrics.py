"""Lyrics provider integration."""

import json
import urllib.parse
import urllib.request


def fetch(query: str) -> tuple[str, str, str]:
    params = urllib.parse.urlencode({"track_name": query})
    request = urllib.request.Request(
        f"https://lrclib.net/api/search?{params}",
        headers={"User-Agent": "terminal-music/3.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            results = json.load(response)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not fetch lyrics: {exc}") from exc
    if not results:
        return query, "", "No lyrics found."
    result = results[0]
    return (
        result.get("trackName") or query,
        result.get("artistName") or "",
        result.get("plainLyrics") or result.get("syncedLyrics") or "Lyrics unavailable.",
    )
