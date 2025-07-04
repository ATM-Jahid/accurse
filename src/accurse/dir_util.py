import shutil
from typing import Any
from pathlib import Path

def get_dest_path(asset_path: Path) -> Path | None:
    asset_dirname = asset_path.name
    pack_dirname = f'AC-{asset_dirname}'
    dest_path = asset_path.parent/pack_dirname

    # The directory cannot exist for us to proceed
    if dest_path.exists():
        print(f'Directory "{dest_path}" already exists!')
        return None
    else:
        dest_path.mkdir(parents=True)
        print(f'Created dir "{dest_path}".\n')
        return dest_path

def create_svgdir(asset_path: Path, dest_path: Path, data: dict[str, Any]) -> bool:
    # Copy shape svgs if mentioned in metadata.toml
    for shape, props in data['cursors'].items():
        new_path = dest_path/'svgs'/shape
        new_path.mkdir(parents=True)

        # Check for animated shapes
        if props.get('animated') == 1:
            svg_pattern = f'{shape}*.svg'
        else:
            svg_pattern = f'{shape}.svg'

        # Finally copy them to the new location
        for file in asset_path.rglob(svg_pattern):
            shutil.copy(file, new_path)

    return True
