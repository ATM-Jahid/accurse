#!/usr/bin/env python

import os
import sys
from lxml import etree

def fix_svg_dims(svg_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(svg_path, parser)
    root = tree.getroot()

    root.set('width', '256')
    root.set('height', '256')
    root.set('viewBox', '0 0 256 256')

    tree.write(svg_path,
               pretty_print=True,
               xml_declaration=False,
               encoding='utf-8')

def process_svgs(directory):
    for path, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.svg'):
                svg_path = os.path.join(path, file)
                fix_svg_dims(svg_path)

def main():
    # Provide the path containing svg files
    svg_dir = sys.argv[1]
    process_svgs(svg_dir)

if __name__ == '__main__':
    main()
