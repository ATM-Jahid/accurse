#!/bin/sh

# Provide the path containing svg files
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

BASE_OLD="#00FF00"
OUTLINE_OLD="#0000FF"

BASE_NEW="#4D4D4D"
OUTLINE_NEW="#FFFFFF"

find "$path" -type f -name "*.svg" | while read -r file; do
	echo "Processing: $file"

	sed -i "s/$BASE_OLD/tmp001/g" "$file"
	sed -i "s/$OUTLINE_OLD/tmp002/g" "$file"

	sed -i "s/tmp001/$BASE_NEW/g" "$file"
	sed -i "s/tmp002/$OUTLINE_NEW/g" "$file"
done

echo "Processing done!"
