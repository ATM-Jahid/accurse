# accurse
Atomsky's cursor maintainer

## Why?
I want to theme Xcursor and Hyprcursor in a manageable way.

## Dependencies
- hyprcursor-util
- librsvg
- xcursorgen

## Workflow
Xcursor and Hyprcursor themes should be built together from a single SVG theme
and packaged in a single folder. The workflow will be:
- Having a unified folder (Hyprcursor format) with uniquely named (l/r) shapes
- Generating a theme folder by symlinking to the unified folder
- Using hyprcursor-util to compile the theme folder
- Using librsvg to convert SVG to PNG
- Using xcursorgen to build the compiled Xcursor version

## License
Copyright (C) 2025 ATM Jahid Hasan<br>
**accurse** is released under the
[GNU AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html).
