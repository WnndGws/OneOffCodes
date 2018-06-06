#!/bin/zsh
##Created youtube-ul. Run as youtube-ul /path/to/dir/ or \*.flv or similar. Deletes files after upload

if [ ! -d "$1" ]; then
    mkdir Uploads
    find . -mindepth 1 -maxdepth 1 -iname "*$1*" | xargs -i mv {} Uploads
    cd Uploads
else
    cd "$1"
fi
# If passed arguement is not a directory then create dir and move files to it
# If it is a directory then change into the dir

n=$((1))
total_copies=$(find . -mindepth 1 -type f -printf "%f\n" | wc -l)
# Count how many files need to be uploaded

source $HOME/.virtualenvs/youtube-upload/bin/activate
# Source youtube-ul in it's virtual env

find . -mindepth 1 -type f -print0 | while IFS= read -r -d $'\0' line;
    do
        echo "Uploading file $n of $total_copies\033[0K\r"
        n=$((n+1))
        title=$(echo "$line" | rev | cut -d \/ -f1 | rev)
        $HOME/.virtualenvs/youtube-upload/youtube-upload/bin/youtube-upload --client-secrets $HOME/.youtube-uploads.credentials.json --privacy unlisted --playlist "Uploaded on $(date +%Y%m%d)" -t "$title" "$line"
        echo "\n"
    done
deactivate
## find all files in current folder and upload them

cd ..
rm -rf Uploads
