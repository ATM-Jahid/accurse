import shutil
from pathlib import Path

def create_svgdir(asset_path: Path, dest_path: Path, data: dict[str, any]) -> bool:
    svg_path = dest_path/'svgs'

    for shape, props in data['cursors'].items():
        new_path = svg_path/shape
        new_path.mkdir(parents=True)

        if props.get('animated') == 1:
            svg_pattern = f'{shape}*.svg'
        else:
            svg_pattern = f'{shape}.svg'

        for file in asset_path.rglob(svg_pattern):
            shutil.copy(file, new_path)

    return True
