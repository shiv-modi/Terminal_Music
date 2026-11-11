"""Application paths and runtime configuration."""

import os
from pathlib import Path

APP_NAME = "terminal-music"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / APP_NAME
DB_PATH = DATA_DIR / "library.db"
