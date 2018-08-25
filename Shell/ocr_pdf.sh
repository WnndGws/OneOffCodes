#!/usr/bin/zsh
## Convert a pdf to tiff, then ocr it

in_file_name=$(echo "$1" | sed 's/\.pdf//')

convert -density 300 "$1" -depth 8 -strip -background white -alpha off "$in_file_name.tiff"
tesseract "$in_file_name.tiff" "$in_file_name"_ocr pdf
rm -rf "$in_file_name.tiff"
