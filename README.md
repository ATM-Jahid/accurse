# accurse
Atomsky's cursor compiler

## Why?
Theming cursors for different standards is a curse. `accurse` alleviates the
curse by allowing you to package hyprcursor and xcursor in a manageable way.
`accurse` can
- compile hyprcursor and xcursor from SVG assets,
- recolor cursor shapes using string replacements,
- flip (mirror) shapes horizontally to make left-handed versions,
- compute consistent hotspots after rescaling and mirroring,
- compile xcursor themes for any given list of sizes,
- and do all these with minimal dependencies.

## Installation
`accurse` is a python package. Install it with:
```sh
pip install accurse
```

For development and access to included themes, clone the repository and install
it locally:
```sh
git clone https://github.com/ATM-Jahid/accurse
cd accurse
pip install .
```

I highly recommend running `pip` in a python [virtual
environment](https://docs.python.org/3/tutorial/venv.html).

### Dependencies
Ensure the following commands are available in your `PATH`:
- `rsvg-convert`
- `xcursorgen`

On **Arch Linux**, install them with:
```sh
sudo pacman -S librsvg xorg-xcursorgen
```

## Quickstart
To compile a cursor theme, provide the path to a `metadata.toml` file that
defines cursor shapes, aliases, and hotspots.
```sh
accurse path/to/metadata.toml
```

For example, if you have cursor assets in `assets/Bibata` along with `metadata.toml`, run:
```sh
accurse assets/Bibata/metadata.toml
```

This will generate compiled hyprcursor and xcursor themes in
`assets/AC-Bibata`. Move `AC-Bibata` to `~/.local/share/icons` and update your
system's cursor settings. Here's [an example
script](https://github.com/ATM-Jahid/afrodots/blob/main/scripts/set_cursor.py)
for changing cursor settings globally.

### Directory Structure
A project structure might look like this:
```
assets/
  ├── Bibata/
  │   ├── metadata.toml
  │   ├── help.svg
  │   ├── left_ptr.svg
  │   ├── progress/
  │   │   ├── progress-01.svg
  │   │   ├── progress-02.svg
  │   │   └── ...
  │   ├── text.svg
  │   ├── wait-01.svg
  │   ├── wait-02.svg
  │   └── ...
  ├── AC-Bibata/   # Output directory after running accurse
```

## Metadata Specification
The `metadata.toml` file defines the theme, settings, and cursor mappings. A
snippet of a metadata file:
```toml
[theme]
name = "Bibata"
description = "Modified Bibata for Me"
version = "0.1"
author = "My Name"

[config]
shape_size = 64
x_hotspot = 32
y_hotspot = 32
old_substr = ["#00FF00", "#0000FF"]
new_substr = ["#FFFFFF", "#000000"]
mirror = 1
xcur_sizes = [24, 32, 48, 64]
cleanup = ["hycur", "xcur"]

[cursors]
[cursors.left_ptr]
x_hotspot = 5
y_hotspot = 5
symlinks = ["default", "arrow"]
flips = 1

[cursors.wait]
symlinks = ["wait"]
animated = 1
anim_delay = 25
flips = 0
```
See `templates/metadata.toml` for a full-length example.

The following tables specify what `accurse` looks for in the metadata file:

### `[theme]`
| Field       | Type   | Description              | Required |
|-------------|--------|--------------------------|----------|
| name        | string | name of the theme        | yes      |
| description | string | description of the theme | yes      |
| version     | string | version of the theme     | no       |
| author      | string | author of the theme      | no       |

### `[config]`
| Field      | Type             | Description                          | Required |
|------------|------------------|--------------------------------------|----------|
| shape_size | number           | size of the (square) SVGs            | yes      |
| x_hotspot  | number           | default hotspot x-coordinate         | yes      |
| y_hotspot  | number           | default hotspot y-coordinate         | yes      |
| old_substr | list of strings  | target substrings                    | no       |
| new_substr | list of strings  | replacement substrings               | no       |
| mirror     | 0 (default) or 1 | mirror shapes with flips=1 flag      | no       |
| xcur_sizes | list of numbers  | compile xcursors of these sizes      | no       |
| cleanup    | list of strings  | delete "hycur" or "xcur" build files | no       |

### `[cursors]`
This table should have `[cursors.shape]` sub-tables. A **shape** means a single
cursor in a theme, such as *left_ptr*, *text*, and *wait*. If you define a
static shape using `[cursors.shape]`, `accurse` will search for `shape.svg`
recursively in the directory that contains `metadata.toml`. If you define an
animated shape with `[cursors.shape]`, `accurse` looks for `shape*.svg`
recursively. This allows you to have files like `shape-01.svg`, `shape-02.svg`,
and so on. The expected key/value pairs for sub-tables follow:

#### `[cursors.shape]`
| Field      | Type             | Description                       | Required    |
|------------|------------------|-----------------------------------|-------------|
| x_hotspot  | number           | hotspot x-coordinate              | no          |
| y_hotspot  | number           | hotspot y-coordinate              | no          |
| symlinks   | list of strings  | shape aliases                     | no          |
| animated   | 0 (default) or 1 | whether it's animated             | no          |
| anim_delay | number           | delay between frames (ms)         | if animated |
| flips      | 0 (default) or 1 | whether to flip shape if mirror=1 | no          |

## Examples
Look into the `assets` directory for a few ready to use cursor themes. Simply
modify the provided `metadata.toml` files in the theme subdirectories and run
`accurse` on them to generate your own custom themes. Here's a glimpse of what
is possible:

![Cursor Showcase](assets/showcase.svg)

## License
Copyright (C) 2025 ATM Jahid Hasan<br>
**accurse** is released under the
[GNU AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html).
