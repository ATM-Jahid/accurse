import shutil
from pathlib import Path
import zipfile

def handle_hycur(dest_path: Path, data: dict[str, any]) -> bool:
    print('Making hyprcursors ...')

    hycur_path = dest_path/'hyprcursors'
    hycur_path.mkdir(parents=True)

    for shape, props in data['cursors'].items():
        print(f'Processing {shape}')

        hypr_shape_path = hycur_path/shape
        shutil.copytree(dest_path/'svgs'/shape, hypr_shape_path)

        # Only the names of svg files (for meta.hl files)
        svg_files = [f.name for f in hypr_shape_path.iterdir() if f.suffix == ".svg"]
        svg_files.sort() # because iterdir() messes up the order of the files
        print(f'\t{len(svg_files)} SVG file(s) found')

        xhot = props.get('x_hotspot', data['config'].get('x_hotspot', 0))
        yhot = props.get('y_hotspot', data['config'].get('y_hotspot', 0))
        canvas_sz = data['config']['shape_size']
        # If mirror image is requested and if the shape flips
        if data['config'].get('mirror', 0) == 1 and props.get('flips', 0) == 1:
            xhot = canvas_sz - xhot

        sym_str = ''
        for syml in props.get('symlinks', []):
            sym_str += f'define_override = {syml}\n'

        file_str = ''
        if props.get('animated', 0) == 1:
            delay = props.get('anim_delay', 25)
            for svg_f in svg_files:
                file_str += f'define_size = 0, {svg_f}, {delay}\n'
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

        print('\tzipping')
        zip_f = hycur_path/f'{shape}.hlc'
        with zipfile.ZipFile(zip_f, 'w', zipfile.ZIP_DEFLATED) as hlc_f:
            for path in hypr_shape_path.rglob('*'):
                if path.is_file():
                    hlc_f.write(path, path.name)

        if 'hycur' in data['config'].get('cleanup', []):
            shutil.rmtree(hypr_shape_path)

    manifest_hl_str = (
        f'cursors_directory = hyprcursors\n'
        f'name = {data['theme']['name']}\n'
        f'description = {data['theme']['description']}\n'
        f'version = {data['theme'].get('version', 'none')}\n'
        f'author = {data['theme'].get('author', 'nobody')}\n'
    )

    manifest_hl_path = dest_path/'manifest.hl'
    with manifest_hl_path.open('w') as f:
        f.write(manifest_hl_str)

    print('Finished making hyprcursors.\n')
    return True
