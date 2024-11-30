import os
from pathlib import Path
from typing import TypedDict

from toml import load

from ezbatch.conf import CONFIG_FILE


# Define the configuration file structure
class EZBatchConfig(TypedDict):
    apple: str


# Default Configuration file path, if not set in environment variable
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "ezbatch.toml"
CONFIG_PATH = Path(os.environ.get("EZBATCH_CONFIG_PATH", str(CONFIG_FILE)))

# test if the file exists
if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Configuration file not found at: {CONFIG_PATH}")
CONFIG = load(CONFIG_PATH)
