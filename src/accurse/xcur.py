import os
import shutil
from pathlib import Path
import subprocess
from accurse.svg_util import gen_png

def handle_xcur(dest_path: Path, data: dict[str, any]) -> bool:
    print('Making xcursors ...')

    png_sizes = data['config'].get('xcur_sizes', [])

    png_path = dest_path/'pngs'
    png_path.mkdir(parents=True)
    svg_path = dest_path/'svgs'

    xcur_path = dest_path/'cursors'
    xcur_path.mkdir(parents=True)

    for shape, props in data['cursors'].items():
        print(f'Processing {shape}')

        svg_shape_path = svg_path/shape

        # Full path of svg files (for xcursorgen)
        svg_files = [f for f in svg_shape_path.iterdir() if f.suffix == ".svg"]
        svg_files.sort() # because iterdir() messes up the order of the files
        print(f'\t{len(svg_files)} SVG file(s) found')

        xhot = props.get('x_hotspot', data['config'].get('x_hotspot', 0))
        yhot = props.get('y_hotspot', data['config'].get('y_hotspot', 0))
        canvas_sz = data['config']['shape_size']
        # If mirror image is requested and if the shape flips
        if data['config'].get('mirror', 0) == 1 and props.get('flips', 0) == 1:
            xhot = canvas_sz - xhot

        # xcursorgen can ignore ani_delay for static cursors
        ani_delay = props.get('anim_delay', 0)

        shape_in_str = ''
        # make pngs in size dirs; populate shape_in_str
        print('\tgenerating pngs')
        for svg_f in svg_files:
            png_name = f'{svg_f.stem}.png'

            for png_sz in png_sizes:
                sz_path = png_path/f'{png_sz}x{png_sz}'
                sz_path.mkdir(parents=True, exist_ok=True)

                # create pngs from the svg file
                gen_png(svg_f, sz_path/png_name, png_sz, png_sz)

                inc_str = (
                    f'{png_sz} '
                    f'{int(xhot/canvas_sz*png_sz+0.5)} '
                    f'{int(yhot/canvas_sz*png_sz+0.5)} '
                    f'{sz_path/png_name} '
                    f'{ani_delay}\n'
                )
                shape_in_str += inc_str

        # generate shape.in
        shape_in_path = png_path/f'{shape}.in'
        with shape_in_path.open('w') as f:
            f.write(shape_in_str)

        # Be careful about subprocess runs because different cli programs
        # expect different paths. It also depends on where you are running this
        # python program from. Thus, use absolute path if possible.

        # generate shape (xcur)
        print('\tcompiling')
        subprocess.run([
            'xcursorgen',
            shape_in_path, # absolute path to the shape.in file
            xcur_path/shape # absolute path to cursors/shape (xcur file)
        ])

        # symlinks
        for syml in props.get('symlinks', []):
            os.symlink(shape, xcur_path/syml)

    index_str = (
        f'[Icon Theme]\n'
        f'Name={data['theme']['name']}\n'
        f'Comment={data['theme']['description']}\n'
    )

    index_path = dest_path/'index.theme'
    with index_path.open('w') as f:
        f.write(index_str)

    if 'xcur' in data.get('config', {}).get('cleanup', []):
        shutil.rmtree(png_path)

    print('Finished making xcursors.\n')
    return True
