#!/bin/zsh
PATH=$PATH:$HOME/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin

# Recovery process
# 1) Download aconfmgr files from mega
# 2) Install and restore aconfmgr
# 3) Restore Antergos
# 4) Restore GoogleDrive

source <(gpg -qd $HOME/.passwords.asc)
export BORG_PASSPHRASE
export mega_user
export mega_password
export google_password

notify-send "Backup Started"""

# Monitor files for changes
inotifywait --exclude "\.changes|\.tmp\.txt" -mr -e modify -e move -e create -e delete --format "%e %w%f" $HOME/wynZFS/Wynand/Backups -o $HOME/wynZFS/Wynand/Backups/.changes &

# Backup my crontab
crontab -l > $HOME/GoogleDrive/01_Personal/05_Software/Antergos/wyntergos_crontab

#Create daily update of GoogleDrive
borg create -p -C lz4 /wynZFS/Wynand/Backups/Antergos/::"{hostname}-{now:%Y%m%d-%H%M}" /home --exclude "*cache*" --exclude $HOME/Downloads --exclude $HOME/wynZFS --exclude "*.nohup*" --exclude "*steam*" --exclude "*Steam*"

# Backup Gmail in a venv
source $HOME/.virtualenv2/gmvault/bin/activate
$HOME/GoogleDrive/01_Personal/05_Software/Antergos/gmail_expect_script.exp ${google_password}
deactivate

# Save packages and configurations
$HOME/GoogleDrive/01_Personal/05_Software/Antergos/aconfmgr_expect_script.exp ${BORG_PASSPHRASE}

 #Prune Backups
echo "Pruning........."
borg prune /wynZFS/Wynand/Backups/Antergos/ --prefix "{hostname}-" --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=12 --keep-yearly=10

# Check backups and alert if issues
echo "Checking........"
borg check /wynZFS/Wynand/Backups/Antergos/ &>> $HOME/wynZFS/Wynand/Backups/.tmp.txt

if grep -Fq "Completed repository check, errors found" $HOME/wynZFS/Wynand/Backups/.tmp.txt
then
    notify-send "Backup Error" "There was an error found in one of the Borg backups"
#   rm -rf $HOME/wynZFS/Wynand/Backups/.tmp.txt
    mv $HOME/wynZFS/Wynand/Backups/.tmp.txt $HOME/BorgCheck.txt
else
    rm -rf $HOME/wynZFS/Wynand/Backups/.tmp.txt
    notify-send "Backups Checked" "All clear"
    # Only copy files to HDD and mega if no errors
   
    echo "Finding changed files..."
    # Need to see if any files changed, and delete them from mega so that the new files can be uploaded
#   diff -qrN /wynZFS/Wynand/Backups /run/media/wynand/Wyntergos_Backups/Backups | cut -d \  -f 4 >$HOME/wynZFS/Wynand/Backups/.tmp.txt
    cut -d \  -f 2 $HOME/wynZFS/Wynand/Backups/.changes >$HOME/wynZFS/Wynand/Backups/.tmp.txt
    rm -rf $HOME/wynZFS/Wynand/Backups/.changes
    sed -i 's/\/home\/wynand\/wynZFS\/Wynand\//\/run\/media\/wynand\/Wyntergos_Backups\//g' $HOME/wynZFS/Wynand/Backups/.tmp.txt
    cat $HOME/wynZFS/Wynand/Backups/.tmp.txt | xargs -i rm -rf {}
    sed -i 's/\/run\/media\/wynand\/Wyntergos_Backups\//\/Root\//g' $HOME/wynZFS/Wynand/Backups/.tmp.txt
    cat $HOME/wynZFS/Wynand/Backups/.tmp.txt | xargs -i megarm -u ${mega_user} -p ${mega_password} {}
    rm -rf $HOME/wynZFS/Wynand/Backups/.tmp.txt

    echo "Copying........."
    # Copy to External Drive
    cp -Lruv $HOME/wynZFS/Wynand/Backups /run/media/wynand/Wyntergos_Backups

    #Upload to mega.nz
    echo "Uploading......."
#   nocorrect megacopy -u ${mega_user} -p ${mega_password} -r /Root/Backups -l  /wynZFS/Wynand/Backups
fi

kill $(pgrep inotifywait)
