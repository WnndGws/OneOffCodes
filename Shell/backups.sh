#!/bin/zsh

# Recovery process
# 1) Download aconfmgr files from mega
# 2) Install and restore aconfmgr
# 3) Restore Antergos
# 4) Restore GoogleDrive

source <(gpg -qd ~/.passwords.asc)
export BORG_PASSPHRASE
export mega_user
export mega_password
export google_password

# Monitor files for changes
inotifywait -mr -e modify -e move -e create -e delete --format "%e %w%f" /home/wynand/wynZFS/Wynand/Backups -o ~/log

# Backup my crontab
crontab -l > ~/GoogleDrive/01_Personal/05_Software/Antergos/wyntergos_crontab

#Create daily update of GoogleDrive
borg create -p -C lz4 /wynZFS/Wynand/Backups/Antergos/::"{hostname}-{now:%Y%m%d-%H%M}" /home --exclude "*cache*" --exclude ~/Downloads --exclude ~/wynZFS --exclude "*.nohup*" --exclude "*steam*" --exclude "*Steam*"

# Backup Gmail
# expect ~/GoogleDrive/01_Personal/05_Software/Antergos/gmail_expect_script.exp ${google_password}

# Save packages and configurations
expect ~/GoogleDrive/01_Personal/05_Software/Antergos/aconfmgr_expect_script.exp ${BORG_PASSPHRASE}

 #Prune Backups
echo "Pruning........."
borg prune /wynZFS/Wynand/Backups/Antergos/ --prefix "{hostname}-" --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=12 --keep-yearly=10

# Check backups and alert if issues
echo "Checking........"
borg check /wynZFS/Wynand/Backups/Antergos/ &>> ~/wynZFS/Wynand/Backups/.tmp.txt

if grep -Fq "Completed repository check, errors found" ~/wynZFS/Wynand/Backups/.tmp.txt
then
    notify-send "Backup Error" "There was an error found in one of the Borg backups"
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt
else
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt
    
    # Only copy files to HDD and mega if no errors
   
    echo "Finding changed files..."
    # Need to see if any files changed, and delete them from mega so that the new files can be uploaded
    diff -qrN /wynZFS/Wynand/Backups /run/media/wynand/Wyntergos_Backups/Backups | cut -d \  -f 4 >~/wynZFS/Wynand/Backups/.tmp.txt
    cat ~/wynZFS/Wynand/Backups/.tmp.txt | xargs -i rm -rf {}
    sed -i 's/\/run\/media\/wynand\/Wyntergos_Backups\/Backups\//\/Root\//g' ~/wynZFS/Wynand/Backups/.tmp.txt
    cat ~/wynZFS/Wynand/Backups/.tmp.txt | xargs -i megarm -u ${mega_user} -p ${mega_password} {}
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt

    echo "Copying........."
    # Copy to External Drive
    cp -Lruv ~/wynZFS/Wynand/Backups /run/media/wynand/Wyntergos_Backups | mbuffer -P 75 -m 8M

    #Upload to mega.nz
    echo "Uploading......."
#   nocorrect megacopy -u ${mega_user} -p ${mega_password} -r /Root/Backups -l  /wynZFS/Wynand/Backups
fi
