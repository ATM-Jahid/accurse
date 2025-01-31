#!/bin/sh

# Use in the assets directory where the template files are
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"
cp manifest_template.hl "$path"/manifest.hl

for dir in "$path"/*/; do
	cp meta_template.hl "$dir"/meta.hl
done
