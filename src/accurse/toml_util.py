from typing import Any
from pathlib import Path
import tomllib

def check_toml(toml_data: dict[str, Any]) -> bool:
    tables = ['theme', 'config', 'cursors']
    for t in tables:
        if t not in toml_data:
            print(f'Table [{t}] is not provided.')
            return False

    theme_keys = ['name', 'description']
    for k in theme_keys:
        if k not in toml_data['theme']:
            print(f'"{k}" is not provided in [theme].')
            return False

    config_keys = ['shape_size', 'x_hotspot', 'y_hotspot']
    for k in config_keys:
        if k not in toml_data['config']:
            print(f'"{k}" is not provided in [config].')
            return False
        else:
            if toml_data['config'][k] <= 0:
                print(f'Provide a positive value for "{k}".')
                return False

    if toml_data['config']['x_hotspot'] > toml_data['config']['shape_size']:
        print('"x_hotspot" cannot be larger than "shape_size".')
        return False

    if toml_data['config']['y_hotspot'] > toml_data['config']['shape_size']:
        print('"y_hotspot" cannot be larger than "shape_size".')
        return False

    return True

def read_toml(metadata_path: Path) -> dict[str, Any] | None:
    try:
        with metadata_path.open('rb') as file:
            return tomllib.load(file)
    except (tomllib.TOMLDecodeError, FileNotFoundError, IsADirectoryError):
        print('Path to a valid TOML is not provided.')
        return None
