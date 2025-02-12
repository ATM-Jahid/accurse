from pathlib import Path
import tomllib
from accurse.svg_util import create_svgdir
from accurse.hycur import handle_hypr
from accurse.xcur import handle_xcur

def read_toml(metadata_path: str) -> bool:
    metadata_path = Path(metadata_path).resolve()
    asset_path = metadata_path.parent
    asset_dir = asset_path.name
    pack_dir = f'AC-{asset_dir}'

    dest_path = asset_path.parent/pack_dir
    if not dest_path.exists():
        dest_path.mkdir(parents=True)
    else:
        print('Package directory already exists! Aborting ...')
        return False

    with metadata_path.open('rb') as file:
        data = tomllib.load(file)

    create_svgdir(asset_path, dest_path, data)

    handle_hypr(dest_path, data)
    handle_xcur(dest_path, data)

    return True
