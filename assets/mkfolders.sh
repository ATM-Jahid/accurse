#!/bin/sh

# Provide the path the directory hosting the SVGs
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for file in "$path"/*.svg; do
	filename=$(basename "$file" .svg)
	dir_name="$path/$filename"
	mkdir -p "$dir_name"
	mv "$file" "$dir_name"
done
