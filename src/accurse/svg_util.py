import shutil
import subprocess
from pathlib import Path
from lxml import etree
from accurse.hash_util import gen_hash

def gen_png(input_svg: Path, output_png: Path, width: int, height: int) -> bool:
    subprocess.run([
        'rsvg-convert',
        '-w', str(width),
        '-h', str(height),
        '-o', output_png,
        input_svg
    ])

    return True

def rescale_svg(file: Path, shape_size: int) -> bool:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser)
    root = tree.getroot()

    # Change viewport in the svg file
    root.set('width', str(shape_size))
    root.set('height', str(shape_size))

    tree.write(file,
               pretty_print=True,
               xml_declaration=False,
               encoding='utf-8')

    return True

def change_substr(file: Path, old_substr: list[str], hash_substr: list[str], new_substr: list[str]) -> bool:
    with file.open('r', encoding='utf-8') as f:
        content = f.read()

    for x, y in zip(old_substr, hash_substr):
        content = content.replace(x, y)

    for x, y in zip(hash_substr, new_substr):
        content = content.replace(x, y)

    with file.open('w', encoding='utf-8') as f:
        f.write(content)

    return True

def flip_hor(file: Path) -> bool:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser)
    root = tree.getroot()

    viewBox = root.get('viewBox')
    if not viewBox:
        print('SVG must have viewBox defined for horizontal flip.')
        print(f'Could not flip {file.name}.')
        return False

    x, _, width, _ = map(float, viewBox.split())
    new_g = etree.Element('g', attrib={'transform': f'translate({2*x + width}, 0) scale(-1, 1)'})

    # list(root) is a copy of the root children
    for child in list(root):
        root.remove(child)
        new_g.append(child)

    root.append(new_g)

    tree.write(file,
               pretty_print=True,
               xml_declaration=True,
               encoding='utf-8')

    return True

def proc_svgs(dest_path: Path, data: dict[str, any]) -> bool:
    shape_size = data['config']['shape_size']

    old_substr = data['config'].get('old_substr', [])
    new_substr = data['config'].get('new_substr', [])

    if not old_substr or not new_substr:
        mod_substr = 0
    elif len(old_substr) != len(new_substr):
        print('WARNING: "old_substr" & "new_substr" are of different length!')
        mod_substr = 0
    else:
        mod_substr = 1

    if mod_substr:
        # String replacements are not shape-specific
        hash_substr = [gen_hash(x, 32) for x in old_substr]

    # Check for horizontal flip request
    mirror = data['config'].get('mirror', 0)

    for shape, props in data['cursors'].items():
        shape_path = dest_path/'svgs'/shape

        # Process the copied over svgs
        for file in shape_path.rglob('*.svg'):
            # rescale viewPort
            rescale_svg(file, shape_size)

            # change substrings
            if mod_substr:
                change_substr(file, old_substr, hash_substr, new_substr)

            # flip horizontally
            if mirror == 1 and props.get('flips', 0) == 1:
                flip_hor(file)

    return True
