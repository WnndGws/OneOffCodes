#!/bin/zsh
## Allows me to ping by MAC address and then adds file to my GoogleDrive if I am home
while /bin/true; do
    set -a
    source <(gpg -qd ~/.passwords.asc)
    set +a

    ip=$(expect /home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Expects/am_I_home.exp $SUDO_PASSPHRASE | grep $1)
    if [ ! -z $ip ]; then
        echo -e "$ip" | mailx -v -s "Home Report" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="$GMAIL" -S smtp-auth-user=$GMAIL -S smtp-auth-password=$GMAIL_PASSPHRASE -S ssl-verify=ignore -S nss-config-dir=~/.cert $GMAIL
        sleeptime=$(date -d 11 +%T)
        sleeptime=$(echo "$(date -d $sleeptime +%s) + 86400" | bc)
        nowtime=$(date -d now +%s)
        time_ts=$(echo "$sleeptime - $nowtime" | bc)

        while [ $time_ts -gt 0 ]; do
            echo -ne "Sleeping for $(date -u -d @$time_ts +'%T')......\033[0K\r"
            sleep 1
            ((time_ts--))
        done

        unset GMAIL
        unset GMAIL_PASSPHRASE
        unset SUDO_PASSPHRASE
    else
        echo "Not online"
        sleep 300
        echo "Sleeping"
        unset GMAIL
        unset GMAIL_PASSPHRASE
        unset SUDO_PASSPHRASE
    fi
done
