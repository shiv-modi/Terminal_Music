"""Playback abstraction for local files and remote media."""

import shutil
import subprocess

from .models import Media
from .storage import Storage


def play(
    item: Media,
    storage: Storage,
    audio_only: bool = True,
    speed: float = 1.0,
    pitch: float = 0.0,
    normalize: bool = False,
) -> None:
    player = shutil.which("mpv") or shutil.which("ffplay")
    storage.record_play(item)
    if not player:
        print(f"{item.title}\n{item.url}")
        print("Install mpv for playback: https://mpv.io/installation/")
        return
    command = [player]
    if player.endswith("mpv"):
        if audio_only:
            command.append("--no-video")
        command.extend(["--speed", str(speed), "--gapless-audio=yes"])
        filters = []
        if pitch:
            filters.append(f"scaletempo2=scale={1 + pitch / 100:.4f}")
        if normalize:
            filters.append("loudnorm")
        if filters:
            command.extend(["--af", ",".join(filters)])
    command.append(item.url)
    print(f"Playing: {item.title}")
    subprocess.run(command, check=False)
