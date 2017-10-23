#!/bin/zsh
##Use to play .order files so can watch overlapping shows in correct order. Searches and plays 1st line in a file. If multiples found presents them. Offers choice whether want to move played file to bottom
##Relys on custom 'lsgrep' function

lines=$(head -1 "$1" | sed -e 's|\ |\*|g' -e "s|'|\\\'|g" -e 's|\.|\*|g' | xargs -i find ~/wynZFS/Media/TV/ -iname "*{}*" | wc -l )
# Takes the 1st line in the WatchOrder file, replaces spaces and ' then counts how many matches it finds

search_term=$(head -1 "$1" | sed -e 's|\ |\*|g' -e "s|'|\\\'|g" -e 's|\.|\*|g' )
# The cleaned up term as a variable

matches=$(head -1 "$1" | sed -e 's|\ |\*|g' -e "s|'|\\\'|g" -e 's|\.|\*|g' | xargs -i find ~/wynZFS/Media/TV/ -iname "*{}*" )
# The found matches as a variable

if [ $lines -eq 0 ]; then
    echo "File not found"
elif [ $lines -eq 1 ]; then
    head -1 "$1" | sed -e 's|\ |\*|g' -e "s|'|\\\'|g" -e 's|\.|\*|g' | xargs -i find ~/wynZFS/Media/TV/ -iname "*{}*" | sed -e "s|'|\\\'|g" | xargs -i xdg-open {}
else
    ~/Git/OneOffCodes/Shell/lsgrep.sh ~/wynZFS/Media/TV "*$search_term*"
fi
# If 0 matches echo, if one match open, if more than one match use "lsgrep" (another function) to display the found files

echo "Would you like to remove the episode from the WatchOrder file?..."
select yn in "Yes" "No"; do
    case $yn in
        Yes ) sed -n '1p' $1 >> $1; sed -i '1d' $1; break;;
        No ) break;;
    esac
done
# Move 1st line of WatchOrder to last line
