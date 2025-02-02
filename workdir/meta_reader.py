#!/usr/bin/env python

import os
import sys
import tomllib

def read_toml(meta_dir):
    meta_path = os.path.join(meta_dir, 'metadata.toml')

    # No error checks!
    with open(meta_path, 'rb') as file:
        data = tomllib.load(file)

    print(data['cursors']['zoom_out'])

def main():
    # Provide path to the dir containing metadata
    meta_dir = sys.argv[1]
    read_toml(meta_dir)

if __name__ == '__main__':
    main()
