"""Domain models used across the application."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Media:
    title: str
    url: str
    channel: str = ""
    duration: str = ""
    kind: str = "video"

    @classmethod
    def from_provider_result(cls, result: dict[str, Any], kind: str) -> "Media":
        return cls(
            title=result.get("title") or "Untitled",
            url=result.get("webpage_url") or result.get("url") or "",
            channel=result.get("channel") or result.get("uploader") or "",
            duration=format_duration(result.get("duration")),
            kind=kind,
        )


def format_duration(value: Any) -> str:
    if not value:
        return ""
    try:
        seconds = int(value)
    except (TypeError, ValueError):
        return ""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
