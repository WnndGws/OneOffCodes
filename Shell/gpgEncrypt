#!/bin/zsh
#GPG encrypt a file to the recipient and myself

if [[ ${1:0:1} != "/" ]]; then
    file_to_encrypt=\.\/$1
else
    file_to_encrypt=$1
fi
#If first character of $1 is not a slash then add ./ to the start of $1
#Set file_to_encrypt as $1

pat=$(echo "$file_to_encrypt")
dep=$(($(grep -o "/" <<< $pat | wc -l)))
#Count how many slashes is in name of the path

if [[ -d "$1" ]]; then
    7z a ${1%/}.7z $1
    encrypt_file=${1%/}.7z
else
    encrypt_file=$1
fi
#If the file_to_encrypt is a folder then zip it first, thus turning a folder into a file

pat=$(echo $pat | cut -d "/" -f 1-$dep)
#New path is the path minus the final term. My heavy-handed way of simulating pwd

recipient="$2"
rename=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)
#Generate a random string of characters and numers 16 characters long

if [ "$#" -ne 2 ]
then
    echo "Please specify <file> and <recipient> as arguments"
else
    gpg -esa -r Wynand -r $recipient -o $pat/$(date +%Y%m%d_%H%M%S)_$rename.asc $encrypt_file
fi
if [[ -d "$1" ]]; then
    rm -rf $encrypt_file
fi
#if a zip was created then delete
