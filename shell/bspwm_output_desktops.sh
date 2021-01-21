#!/usr/bin/env sh
## Prints a string to put in sxhkd

desktop_head="$(bspc query --desktops | head --lines 1)"
desktop_head="${desktop_head%?}" # Split off last character
desktop_head="${desktop_head%?}" # Split off last character again
all_desktops="$(bspc query --desktops)"

manipulated_string="<++>"
new_string="bspc {node --to-desktop, desktop --focus} ""$desktop_head{"
for i in $(IFS=' '; echo "$all_desktops"); do
    new_string="$new_string""${i##$desktop_head}," # Searches from the back until it finds that whole string
done

new_string="#Added by script\n#Focus or Move window to desktops\nalt + {shift + ,_} {1-9,0}\n    ${new_string%?}}"
echo "$new_string"
