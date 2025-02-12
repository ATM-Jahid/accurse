import shutil
from pathlib import Path
from lxml import etree

def rescale_svg(file: Path, shape_size: int) -> bool:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser)
    root = tree.getroot()

    # Change viewport in the svg file
    root.set('width', str(shape_size))
    root.set('height', str(shape_size))

    tree.write(file,
               pretty_print=True,
               xml_declaration=True,
               encoding='utf-8')

    return True

def change_substr(file: Path) -> bool:
    return True

def flip_hor(file: Path) -> bool:
    return True

def proc_svgs(dest_path: Path, data: dict[str, any]) -> bool:
    # Make sure shape_size exists in check_integrity
    # Also make sure it's a positive value
    shape_size = data['config'].get('shape_size', 32)

    # Make sure they are of equal length in check_integrity
    old_substr = data['config'].get('old_substr', [])
    new_substr = data['config'].get('new_substr', [])
    mod_substr = 0 if not old_substr else 1

    # Check for mirror request
    mirror = data['config'].get('mirror', 0)

    for shape, props in data['cursors'].items():
        shape_path = dest_path/'svgs'/shape

        # Process the copied over svgs
        for file in shape_path.rglob('*.svg'):
            # rescale viewPort
            rescale_svg(file, shape_size)

            # change substrings
            if mod_substr:
                change_substr(file, old_substr, new_substr)

            # flip horizontally
            if mirror == 1:
                flip_hor(file)

    return True
