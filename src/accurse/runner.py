import sys
from pathlib import Path
from accurse.toml_util import read_toml, check_integrity
from accurse.dir_util import get_dest_path, create_svgdir
from accurse.svg_util import proc_svgs
from accurse.hycur import handle_hycur
from accurse.xcur import handle_xcur

def main() -> bool:
    # Provide path to the TOML file
    metadata_path = Path(sys.argv[1]).resolve()

    # Load metadata.toml
    toml_data = read_toml(metadata_path)
    if toml_data is None:
        print('Aborting ...')
        return False

    # Check for toml integrity here
    valid_toml = check_integrity(toml_data)
    if not valid_toml:
        print('Aborting ...')
        return False

    # metadata.toml should be in the same dir as svg assets
    asset_path = metadata_path.parent
    dest_path = get_dest_path(asset_path)
    if dest_path is None:
        print('Aborting ...')
        return False

    # Copy svgs in asset_path to dest_path/svgs
    create_svgdir(asset_path, dest_path, toml_data)

    # Process svgs: rescale, recolor, flip
    proc_svgs(dest_path, toml_data)

    handle_hycur(dest_path, toml_data)

    handle_xcur(dest_path, toml_data)

    return True
