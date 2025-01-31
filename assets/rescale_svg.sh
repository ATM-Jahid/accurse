#!/bin/sh

# Provide the path that has subdirs of svg and meta
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for subdir in "$path"/*/; do
	for file in "$subdir"*.svg; do
		rsvg-convert -w 256 -h 256 "$file" -f svg -o "$file"
	done
done
