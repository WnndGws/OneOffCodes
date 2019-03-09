#!/usr/bin/zsh
## Download from URL

url="$1"

curl $url | rg 'href=".*"' | awk -F\" '{print u"/"$2}' u=$url | parallel --jobs=1 --keep-order wget
rm index.html
