#!/usr/bin/env python

import os
import sys
import shutil
import tomllib
import zipfile

def handle_hypr(asset_path, dest_path, data):
    hycur_path = os.path.join(dest_path, 'hyprcursors')
    os.makedirs(hycur_path)

    for shape, props in data['cursors'].items():
        asset_shape_path = os.path.join(asset_path, shape)
        pack_shape_path = os.path.join(hycur_path, shape)
        if os.path.exists(asset_shape_path):
            shutil.copytree(asset_shape_path, pack_shape_path)
        else:
            print(shape, ': asset name and metadata do not match!')
            return False

        xhot = props.get('x_hotspot', data['config'].get('x_hotspot', 0))
        yhot = props.get('y_hotspot', data['config'].get('y_hotspot', 0))
        canvas_sz = data['config']['shape_size']

        sym_str = ''
        if 'symlinks' in props:
            for syml in props['symlinks']:
                sym_str += f'define_override = {syml}\n'
            ## define_override doesn't follow the standard
            #sym_str = '; '.join(props['symlinks'])

        file_str = ''
        ani_delay = data['config']['anim_delay']
        svg_files = [f for f in os.listdir(pack_shape_path)
            if f.endswith(".svg")]
        if len(svg_files) == 1:
            file_str += f'define_size = 0, {svg_files[0]}'
        elif len(svg_files) > 1:
            for svg_f in svg_files:
                file_str += f'define_size = 0, {svg_f}, {ani_delay}\n'
        else:
            print('No SVG files in the directory!')
            return False

        meta_str = (
            f'resize_algorithm = none\n'
            f'hotspot_x = {xhot/canvas_sz:.3f}\n'
            f'hotspot_y = {yhot/canvas_sz:.3f}\n'
            f'nominal_size = 1.000\n'
            f'{sym_str}\n'
            f'{file_str}'
        )

        metahl_path = os.path.join(pack_shape_path, 'meta.hl')
        with open(metahl_path, 'w') as f:
            f.write(meta_str)

        zip_f = os.path.join(hycur_path, f'{shape}.hlc')
        with zipfile.ZipFile(zip_f, 'w', zipfile.ZIP_DEFLATED) as hlc_f:
            for path, _, files in os.walk(pack_shape_path):
                for file in files:
                    hlc_f.write(os.path.join(path, file), file)

    manifest_str = (
        f'cursors_directory = hyprcursors\n'
        f'name = {data['theme']['name']}\n'
        f'description = {data['theme']['description']}\n'
        f'version = {data['theme']['version']}\n'
        f'author = {data['theme']['author']}\n'
    )

    manifest_path = os.path.join(dest_path, 'manifest.hl')
    with open(manifest_path, 'w') as f:
        f.write(manifest_str)

    return True

def read_toml(metadata_path):
    asset_path, _ = os.path.split(metadata_path)
    asset_dir = os.path.basename(asset_path)
    pack_dir = f'AC-{asset_dir}'

    dest_path = os.path.join(os.path.dirname(asset_path), pack_dir)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    else:
        print('Package directory already exists! Aborting ...')
        return False

    with open(metadata_path, 'rb') as file:
        data = tomllib.load(file)

    handle_hypr(asset_path, dest_path, data)

    return True

def main():
    # Provide path to the TOML file
    metadata_path = sys.argv[1]
    read_toml(metadata_path)

if __name__ == '__main__':
    main()
