#!/bin/sh

# Provide the path that has subdirs of svg and meta
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for subdir in "$path"/*/; do
	if [ -f "$subdir/meta.hl" ]; then
		hotspot_x=$(sed -n '2p' "$subdir/meta.hl" | awk -F' = ' '{print $2}')
		hotspot_y=$(sed -n '3p' "$subdir/meta.hl" | awk -F' = ' '{print $2}')

		echo "In subdirectory $subdir:"
		echo "hotspot_x = $hotspot_x"
		echo "hotspot_y = $hotspot_y"
		echo "----------------------------"
	fi
done
