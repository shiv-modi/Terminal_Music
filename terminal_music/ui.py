"""Terminal rendering helpers."""

from .models import Media


def print_media(items: list[Media]) -> None:
    if not items:
        print("No results.")
        return
    print(f"{'#':>3}  {'TITLE':<50}  {'CHANNEL':<24}  TIME")
    print("-" * 92)
    for index, item in enumerate(items, 1):
        print(f"{index:>3}  {item.title[:50]:<50}  {item.channel[:24]:<24}  {item.duration}")
