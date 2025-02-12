from typing import Any, Optional
from pathlib import Path
import tomllib

def check_integrity(toml_data: dict[str, Any]) -> bool:
    # check if essential values exist
    return True

def read_toml(metadata_path: Path) -> Optional[dict[str, Any]]:
    try:
        with metadata_path.open('rb') as file:
            return tomllib.load(file)
    except (tomllib.TOMLDecodeError, FileNotFoundError, IsADirectoryError):
        print('Path to a valid TOML is not provided.')
        return None
