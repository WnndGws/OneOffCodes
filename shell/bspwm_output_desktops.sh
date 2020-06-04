#!/usr/bin/env sh
## Prints a string to put in sxhkd

desktop_head="$(bspc query --desktops | head -n1)"
desktop_head="${desktop_head%?}" # Split off last character
all_desktops="$(bspc query --desktops)"

manipulated_string="<++>"
new_string="bspc desktop --focus ""$desktop_head{"
for i in $(IFS=' '; echo "$all_desktops"); do
    new_string="$new_string""${i##$desktop_head}," # ## searches from the back until it finds that whole string
done

new_string="\n#Added by script\nalt + {1-9,0}\n    ${new_string%?}}"
echo "$new_string"
