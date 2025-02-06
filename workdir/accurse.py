#!/usr/bin/env python

import sys
import shutil
from pathlib import Path
import tomllib
import zipfile
import subprocess

def svg_to_png(input_svg, output_png, width, height):
    subprocess.run([
        'rsvg-convert',
        '-w', str(width),
        '-h', str(height),
        '-o', output_png,
        input_svg
    ])

def handle_xcur(dest_path, data):
    # get it from data['config']['xcur_sizes']
    png_size = 24

    png_path = dest_path/'pngs'
    png_path.mkdir(parents=True)
    svg_path = dest_path/'svgs'

    xcur_path = dest_path/'cursors'
    xcur_path.mkdir(parents=True)

    for shape, props in data['cursors'].items():
        svg_shape_path = svg_path/shape
        svg_files = [f for f in svg_shape_path.iterdir() if f.suffix == ".svg"]
        svg_files.sort()

        xhot = props.get('x_hotspot', data['config'].get('x_hotspot', 0))
        yhot = props.get('y_hotspot', data['config'].get('y_hotspot', 0))
        canvas_sz = data['config']['shape_size']
        ani_delay = props.get('anim_delay', 0)

        # for the shape.in file
        shape_in_str = ''

        # save to png files; populate shape_in_str
        for svg_f in svg_files:
            png_name = f'{svg_f.stem}.png'
            svg_to_png(svg_f, png_path/png_name, png_size, png_size)

            inc_str = (
                f'{png_size} '
                f'{int(xhot/canvas_sz*png_size+0.5)} '
                f'{int(yhot/canvas_sz*png_size+0.5)} '
                f'{png_path/png_name} '
                f'{ani_delay}\n'
            )
            shape_in_str += inc_str

        # generate shape.in
        shape_in_path = png_path/f'{shape}.in'
        with shape_in_path.open('w') as f:
            f.write(shape_in_str)

        # Subprocess run needs some magic because different cli programs do
        # different things with paths

        # generate shape (xcur)
        subprocess.run([
            'xcursorgen',
            shape_in_path,
            xcur_path/shape
        ])

        # symlinks
        if 'symlinks' in props:
            for syml in props['symlinks']:
                subprocess.run([
                    'ln',
                    '-s',
                    shape,
                    xcur_path/syml
                ])

    index_str = (
        f'[Icon Theme]\n'
        f'Name={data['theme']['name']}\n'
        f'Comment={data['theme']['description']}\n'
    )

    index_path = dest_path/'index.theme'
    with index_path.open('w') as f:
        f.write(index_str)

    return True

def handle_hypr(dest_path, data):
    hycur_path = dest_path/'hyprcursors'
    hycur_path.mkdir(parents=True)

    for shape, props in data['cursors'].items():
        hypr_shape_path = hycur_path/shape
        shutil.copytree(dest_path/'svgs'/shape, hypr_shape_path)

        xhot = props.get('x_hotspot', data['config'].get('x_hotspot', 0))
        yhot = props.get('y_hotspot', data['config'].get('y_hotspot', 0))
        canvas_sz = data['config']['shape_size']

        sym_str = ''
        if 'symlinks' in props:
            for syml in props['symlinks']:
                sym_str += f'define_override = {syml}\n'

        file_str = ''
        svg_files = [f.name for f in hypr_shape_path.iterdir() if f.suffix == ".svg"]
        svg_files.sort() # because iterdir() messes up the order of the files
        if props.get('animated') == 1:
            ani_delay = props['anim_delay']
            for svg_f in svg_files:
                file_str += f'define_size = 0, {svg_f}, {ani_delay}\n'
        else:
            file_str += f'define_size = 0, {svg_files[0]}'

        meta_hl_str = (
            f'resize_algorithm = none\n'
            f'hotspot_x = {xhot/canvas_sz:.3f}\n'
            f'hotspot_y = {yhot/canvas_sz:.3f}\n'
            f'nominal_size = 1.000\n'
            f'{sym_str}\n'
            f'{file_str}'
        )

        meta_hl_path = hypr_shape_path/'meta.hl'
        with meta_hl_path.open('w') as f:
            f.write(meta_hl_str)

        zip_f = hycur_path/f'{shape}.hlc'
        with zipfile.ZipFile(zip_f, 'w', zipfile.ZIP_DEFLATED) as hlc_f:
            for path in hypr_shape_path.rglob('*'):
                if path.is_file():
                    hlc_f.write(path, path.name)

        if data.get('config', {}).get('cleanup') == 1:
            shutil.rmtree(hypr_shape_path)

    manifest_hl_str = (
        f'cursors_directory = hyprcursors\n'
        f'name = {data['theme']['name']}\n'
        f'description = {data['theme']['description']}\n'
        f'version = {data['theme']['version']}\n'
        f'author = {data['theme']['author']}\n'
    )

    manifest_hl_path = dest_path/'manifest.hl'
    with manifest_hl_path.open('w') as f:
        f.write(manifest_hl_str)

    return True

def create_svgdir(asset_path, dest_path, data):
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

def read_toml(metadata_path):
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

def main():
    # Provide path to the TOML file
    metadata_path = sys.argv[1]
    read_toml(metadata_path)

if __name__ == '__main__':
    main()
