#!/bin/zsh
## Allows me to ping by IP address and then sends me an email if I am home

while /bin/true; do
    timeout 1.0 ping -c1 $1
    ip=$(echo $?)
    # Gets the exit code after one ping

    if [ "$ip" -eq 0 ]; then
        set -a
        source <(gpg -qd ~/.passwords.asc)
        set +a        
        echo -e "$1 is home" | mailx -v -s "Home Report" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S mta=smtp://smtp.gmail.com:587 -S from="$GMAIL" -S smtp-auth-user=$GMAIL -S smtp-auth-password=$GMAIL_PASSPHRASE -S ssl-verify=ignore -S nss-config-dir=~/.cert $GMAIL
        unset GMAIL
        unset GMAIL_PASSPHRASE
        unset SUDO_PASSPHRASE
        # If exit code is 0 then ping worked, ie home

        for n in {1..4}; do
        ip=0
            while [[ -z "$ip" ]]; do
                sleep 300
                ip=$(nmap $1 | grep "Host is up")
            done
        done
        # use nmap to test if host is up, needs to fail 4 times to avoid false positives

        set -a
        source <(gpg -qd ~/.passwords.asc)
        set +a        
        echo -e "$1 has left home" | mailx -v -s "Home Report" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S mta=smtp://smtp.gmail.com:587 -S from="$GMAIL" -S smtp-auth-user=$GMAIL -S smtp-auth-password=$GMAIL_PASSPHRASE -S ssl-verify=ignore -S nss-config-dir=~/.cert $GMAIL
        unset GMAIL
        unset GMAIL_PASSPHRASE
        unset SUDO_PASSPHRASE

        sleeptime=$(date -d 11 +%T)
        sleeptime=$(echo "$(date -d $sleeptime +%s) + 86400" | bc)
        nowtime=$(date -d now +%s)
        time_ts=$(echo "$sleeptime - $nowtime" | bc)

        while [ $time_ts -gt 0 ]; do
            echo -ne "Sleeping for $(date -u -d @$time_ts +'%T')......\033[0K\r"
            sleep 1
            ((time_ts--))
        done
    else
        echo "Not online"
        echo "Sleeping"
        sleep 300
    fi
done
