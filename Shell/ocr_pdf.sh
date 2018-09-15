#!/usr/bin/zsh
## Convert a pdf to tiff, then ocr it

full_in_name="$1"
in_file_name=$(echo "$1" | rev | cut -d'.' -f2- | rev)

#convert -density 300 "output.pdf" -depth 8 -strip -background white -alpha off "$in_file_name.tiff"
$HOME/Git/OneOffCodes/Shell/textcleaner -g -e stretch -f 35 -o 15 -a 2 -s 1 "$1" "cleaned.tiff"
tesseract -l eng "cleaned.tiff" "$in_file_name"_ocr pdf
rm -rf "cleaned.tiff"
mupdf "$in_file_name"_ocr.pdf
#rm -rf output.pdf page*
