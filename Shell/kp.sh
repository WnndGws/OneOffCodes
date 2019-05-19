#!/usr/bin/zsh
## Kill a process by name

ps -e | rg $1 | awk '{print $1}' | xargs -I {} kill {}
