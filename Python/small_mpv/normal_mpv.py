#!/usr/bin/python
### Resizes all mpv videos to small windows

import i3ipc
import re

# Create the Connection object that can be used to send commands and subscribe
# to events.
i3 = i3ipc.Connection()

mpv_leafs = 0

while mpv_leafs == 0:
    windows_open = i3.get_tree().leaves()
    for leaf in windows_open:
        if re.match(".*(- mpv)|(Plex).*", leaf.name, re.IGNORECASE) is not None:
            mpv_leafs += 1

for leaf in windows_open:
    windows_open = i3.get_tree().leaves()
    if re.match(".*(- mpv)|(Plex).*", leaf.name, re.IGNORECASE) is not None:
        connection_id = leaf.id
        print(connection_id)
        leaf.command(f'[con_id="{connection_id}"] resize set 50 ppt 100 ppt')
