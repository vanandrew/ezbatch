from pathlib import Path

from ezbatch.client import STS_CLIENT

CURRENT_AWS_ACCOUNT = STS_CLIENT.get_caller_identity()["Account"]
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "ezbatch.toml"
DEFAULT_MAX_VCPUS = 256
