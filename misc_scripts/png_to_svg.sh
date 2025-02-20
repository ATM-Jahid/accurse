#!/bin/sh

# Provide the path that has pngs
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

find "$path" -type f -name "*.png" | while read -r file; do
	svg_file="${file%.png}.svg"

	if [ -f $svg_file ]; then
		echo "Skipping: $svg_file already exists"
	else
		echo "Converting $file"
		inkscape --export-type=svg "$file"
	fi
done

echo "Processing done!"
