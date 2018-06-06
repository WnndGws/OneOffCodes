#!/usr/bin/zsh
## Shell script to compile latex for me using mklatex

tex_file="$1"
latexmk -xelatex -f -g -silent -cd $tex_file

pdf_file=$(echo $tex_file | cut -d'.' -f1)
pdf_file=$pdf_file".pdf"
mupdf $pdf_file