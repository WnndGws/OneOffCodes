#!/usr/bin/zsh
## Changes all my download things systemd to start in correct group

sudo sed -i 's/Group=plex/Group=media_management/' /usr/lib/systemd/system/plexmediaserver.service
sudo sed -i 's/Group=radarr/Group=media_management/' /usr/lib/systemd/system/radarr.service
sudo sed -i 's/Group=sabnzbd/Group=media_management/' /usr/lib/systemd/system/sabnzbd.service
sudo sed -i 's/Group=sonarr/Group=media_management/' /usr/lib/systemd/system/sonarr.service
sudo sed -i 's/Group=transmission/Group=media_management/' /usr/lib/systemd/system/transmission.service
