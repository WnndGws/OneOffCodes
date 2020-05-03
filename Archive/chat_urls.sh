#!/usr/bin/zsh
## 
rm -f /tmp/chatlogs.txt
find $HOME/.centerim5/logs -type f -mtime 0 | xargs -I{} cat {} >> /tmp/chatlogs.txt
urlscan --compact --dedup < /tmp/chatlogs.txt
