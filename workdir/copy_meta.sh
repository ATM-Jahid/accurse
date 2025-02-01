#!/bin/sh

# Provide the path that has subdirs of svg and meta
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for subdir in "$path"/*/; do
	cp meta_template.hl "$subdir"/meta.hl

	for file in "$subdir"/*.svg; do
		filename=$(basename "$file")
		line="define_size = 0, $filename"
		echo "$line" >>"$subdir/meta.hl"
	done
done
