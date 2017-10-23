#!/bin/zsh
## Locks and mutes PC

# Mutes and unmutes
# muted status (yes = muted)
active_sink=$(pacmd list-sinks | awk '/* index:/{print $3}')
muteStatus=$(pacmd list-sinks | grep -A 15 'index: '$active_sink | grep 'muted' | awk '{print $2}')

# Mute even if already muted, but dont change muteStatus as this will be used as our 'before'
pactl set-sink-mute $active_sink 1

scrot /tmp/screen.png
# Screenshot

convert /tmp/screen.png -scale 5% -scale 2000% /tmp/screen.png
convert /tmp/screen.png -paint 1 /tmp/screen.png
# Shrinks down, then resizes up so screenshot is blurry

[[ -f $HOME/.dotfiles/i3/.config/i3/lock.png ]] && convert /tmp/screen.png $HOME/.dotfiles/i3/.config/i3/lock.png -gravity center -composite -matte /tmp/screen.png
# Adds lock image over the blurry screenshot

i3lock --no-unlock-indicator --ignore-empty-password --image=/tmp/screen.png --nofork &&\
if [ $muteStatus = "no" ]
then
    pactl set-sink-mute $active_sink 0
else
    exit
fi

trash-empty

#xset dpms force off
# Turns off screen
