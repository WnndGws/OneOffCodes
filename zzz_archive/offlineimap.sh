#!/usr/bin/zsh
## Sync offlineimap if are connected to internet and can ping IMAP server

imapserver="imap.gmail.com"
imapactive=$(ps -ef | grep '[o]fflineimap' | wc -l) netactive=$(ping -c3 $imapserver >/dev/null 2>&1 && echo up || echo down)

# kill offlineimap if active, sometimes it hangs
case $imapactive in
'1')
 killall -9 offlineimap && sleep 5
;;
esac

# Check that you can access the SMTP server
case $netactive in
'up')
 /usr/bin/offlineimap -u quiet -q
;;
'down')
 :
;;
esac
