"""External media providers."""

from typing import Any

from .models import Media


def _client() -> Any:
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError(
            "Install YouTube support with: python -m pip install -r requirements.txt"
        ) from exc
    return yt_dlp


def search(query: str, limit: int = 10, kind: str = "video") -> list[Media]:
    options = {"quiet": True, "no_warnings": True, "extract_flat": True, "skip_download": True}
    with _client().YoutubeDL(options) as client:
        info = client.extract_info(f"ytsearch{limit}:{query}", download=False)
    return [
        Media.from_provider_result(item, kind)
        for item in (info.get("entries") or [])
        if item
    ]
