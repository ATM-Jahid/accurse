#!/bin/sh

# Provide the path that has pngs
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

find "$path" -type f -name "*.png" | while read -r file; do
	echo "Processing: $file"
	inkscape --export-type=svg "$file"
done

echo "Processing done!"
