#!/bin/zsh
##Everything i need to hibernate until 2am, wake up, and hibernate again at 5am

rtcHibernate () {
    if [ "$(date -d now +%H)" -ge "0" -a "$(date -d now +%H)" -le "9" ]; then
        source <(gpg -qd ~/.passwords.asc) && export SUDO_PASSPHRASE && expect /home/wynand/Git/OneOffCodes/Expects/rtcHibernate.exp ${SUDO_PASSPHRASE} $(date -d T0100 +%s)
    else
        source <(gpg -qd ~/.passwords.asc) && export SUDO_PASSPHRASE && expect /home/wynand/Git/OneOffCodes/Expects/rtcHibernate.exp ${SUDO_PASSPHRASE} $(date -d "now + 1day T0100" +%s)
    fi
}
#Always hibernate until the next 2am

reHybernate () {
    rehybernate=10800
    while [ $rehybernate -gt 0 ]; do
        echo "Computer will hibernate in $rehybernate seconds......\033[0K\r"
        sleep 1
        : $((rehybernate--))
    done
}
#Hardcoded hibernate_in set to 10800s

testHibernate () {
    while [ $(awk '{getline t<".time_before.txt"; print $0-t}' .time_after.txt) -le 60 ]; do
        date +%s > .time_before.txt
        rtcHibernate
        lock
        date +%s > .time_after.txt
    done
}
#Creates a tmp file to see if computer actually hibernated by comparing the time before the hibernate command was sent and the current time

postHibernate () {
    rm -f .time_before.txt .time_after.txt > /dev/null 2>&1
    reset_wifi > /dev/null 2>&1
    variety -n > /dev/null 2>&1 &
}
#Deletes the hibernate tests, resets wifi, and gets me a new wallpaper

ttBackup () {
    time_tb=$((3600-($(date +\%s)%3600)))
    while [ $time_tb -gt 0 ]; do
        echo -ne "Backup will start in $time_tb seconds......\033[0K\r"
        sleep 1
        : $((time_tb--))
    done
}
#TimeToBackup, but is funtionally just a countdown to the top of the next hour

if [ "$(date -d now +%H)" -ge "2" -a "$(date -d now +%H)" -le "6"   ]; then
    lock
    reHybernate
    date +%s > .time_before.txt
    rtcHibernate
    lock
    date +%s > .time_after.txt
    testHibernate
    postHibernate
else;
    date +%s > .time_before.txt
    rtcHibernate
    lock
    date +%s > .time_after.txt
    testHibernate
    postHibernate
    if [ "$(date -d now +%H)" -ge "2" -a "$(date -d now +%H)" -le "6"  ]; then
        reHybernate
        date +%s > .time_before.txt
        rtcHibernate
        lock
        date +%s > .time_after.txt
        testHibernate
        postHibernate
    fi
fi
#hibernate function that puts everything together.
