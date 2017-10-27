#!/bin/zsh
## Locks and mutes PC

# Find resolution of screen(s)
resolution=$(xdpyinfo | grep dimensions | awk '{print $2}')

# Location of lock image
lock_image="$HOME/.dotfiles/i3/.config/i3/lock.png"

# Set filters to apply to the image
filters='noise=alls=10,scale=iw*.05:-1,scale=iw*20:-1:flags=neighbor'

# Output file location
output_loc="/tmp/screen.png"

# Take screenshot and apply filters, and overlay lock_image
ffmpeg -y -loglevel 0 -s "$resolution" -f x11grab -i $DISPLAY -i $lock_image -vframes 1 -vf "$filters" -filter_complex 'overlay' $output_loc

i3lock --no-unlock-indicator --ignore-empty-password --image=$output_loc --nofork &&\

# Mutes and unmutes
# muted status (yes = muted)
active_sink=$(pacmd list-sinks | awk '/* index:/{print $3}')
muteStatus=$(pacmd list-sinks | grep -A 15 'index: '$active_sink | grep 'muted' | awk '{print $2}')

# Mute even if already muted, but dont change muteStatus as this will be used as our 'before'
pactl set-sink-mute $active_sink 1

if [ $muteStatus = "no" ]
then
    pactl set-sink-mute $active_sink 0
else
    exit
fi

trash-empty

#xset dpms force off
# Turns off screen
