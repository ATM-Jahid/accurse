#!/bin/sh

# Provide the path containing svg without meta
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for file in "$path"/*.svg; do
	filename=$(basename "$file" .svg)
	subdir="$path/$filename"
	mkdir -p "$subdir"
	mv "$file" "$subdir"
done
