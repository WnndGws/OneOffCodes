#!/bin/zsh
PATH=$PATH:/home/wynand/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin

if [ "$(date -d now +%H)" -ge "0" -a "$(date -d now +%H)" -le "2" ]; then
   source <(gpg -qd ~/.passwords.asc) && export BORG_PASSPHRASE && expect ~/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Expects/rtcHibernate.exp ${BORG_PASSPHRASE} $(date -d T0059 +%s)
else
   source <(gpg -qd ~/.passwords.asc) && export BORG_PASSPHRASE && expect ~/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Expects/rtcHibernate.exp ${BORG_PASSPHRASE} $(date -d "now + 1day T0059" +%s)
fi

sleep 20

i3lock -c 000000 -I 5
source <(gpg -qd ~/.passwords.asc) && export BORG_PASSPHRASE && expect ~/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Expects/reset_network.exp ${BORG_PASSPHRASE}
