#!/bin/sh

# Provide the path containing manifest.hl
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path_to_directory>"
	exit 1
fi

path="$1"

for dir in "$path"/*/; do
	if [ -f "$dir/meta.hl" ]; then
		hotspot_x=$(sed -n '2p' "$dir/meta.hl" | awk -F' = ' '{print $2}')
		hotspot_y=$(sed -n '3p' "$dir/meta.hl" | awk -F' = ' '{print $2}')

		echo "In directory $dir:"
		echo "hotspot_x = $hotspot_x"
		echo "hotspot_y = $hotspot_y"
		echo "----------------------------"
	fi
done
