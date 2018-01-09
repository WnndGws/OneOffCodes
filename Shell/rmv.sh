#!/bin/zsh
#Allows moving through wildcard use. rcp /path/to/files/\*.mkv /path/to/dest

pat=$(echo "$1")
# Path to copy from

dep=$(($(grep -o "/" <<< $pat | wc -l)))
# Depth if the path, counts / in pat

term=$(echo $pat | rev | cut -d "/" -f 1 | rev)
# The search term, defined as everything after the final /

pat=$(echo $pat | cut -d "/" -f 1-$dep)
# pat is redefined as the path but now without the search term
# My long way of copying pwd

n=$((1))
total_copies=$(find "$pat" -maxdepth 1 -iname "$term" | wc -l)
# Counts how many files will be copied

if [ ! -d "$2" ]; then
    mkdir -p "$2"
fi
# If copy to directory doesn't exist then make it

find $pat -maxdepth 1 -iname "$term" -print0 | while IFS= read -r -d $'\0' line;
    do
        echo "Copying file $n of $total_copies\033[0K\r"
        rsync -vrhP --remove-source-files "$line" "$2"
        n=$((n+1))
        echo "\n"
    done
# Find term in path and copies, then removes source thus simulating moving, while outputing how many have been done

if [[ "$2" = $HOME\/run\/media\/wynand\/.* ]]; then
    sync &
    watch grep -e Dirty: -e Writeback: /proc/meminfo
fi
# If the copy was to a USB then sync and display writeback
