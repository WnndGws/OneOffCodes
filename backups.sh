#!/bin/zsh

# Recovery process
# 1) Download aconfmgr files from mega
# 2) Install and restore aconfmgr
# 3) Restore Antergos
# 4) Restore GoogleDrive

source <(gpg -qd ~/.passwords.asc)
export BORG_PASSPHRASE
export mega_user
export google_password

#Create daily update of GoogleDrive
borg create -p -C lz4 ~/wynZFS/Wynand/Backups/GoogleDrive/::"{hostname}-{now:%Y%m%d-%H%M}" ~/GoogleDrive

borg create -p -C lz4 ~/wynZFS/Wynand/Backups/Antergos/::"{hostname}-{now:%Y%m%d-%H%M}" /home/ --exclude ~/.PlayOnLinux --exclude "*cache*" --exclude ~/GoogleDrive --exclude ~/Downloads --exclude ~/wynZFS --exclude "*.nohup*" --exclude "*steam*" --exclude "*Steam*"

# Backup Gmail
expect ~/GoogleDrive/01_Personal/05_Software/Antergos/gmail_expect_script.exp ${google_password}

# Save packages and configurations
expect ~/GoogleDrive/01_Personal/05_Software/Antergos/aconfmgr_expect_script.exp ${BORG_PASSPHRASE}

 #Prune Backups
echo "Pruning........."
borg prune ~/wynZFS/Wynand/Backups/GoogleDrive/ --prefix "{hostname}-" --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=12 --keep-yearly=10
borg prune ~/wynZFS/Wynand/Backups/Antergos/ --prefix "{hostname}-" --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=12 --keep-yearly=10

# Check backups and alert if issues
echo "Checking........"
borg check ~/wynZFS/Wynand/Backups/GoogleDrive/ &>> ~/wynZFS/Wynand/Backups/tmp.txt
borg check ~/wynZFS/Wynand/Backups/Antergos/ &>> ~/wynZFS/Wynand/Backups/tmp.txt
if grep -Fq "Completed repository check, errors found" ~/wynZFS/Wynand/Backups/tmp.txt
then
    notify-send "Backup Error" "There was an error found in one of the Borg backups"
    rm -rf ~/wynZFS/Wynand/Backups/tmp.txt
else
    rm -rf ~/wynZFS/Wynand/Backups/tmp.txt
    # Only copy files to SDD and mega if no errors
    echo "Copying........."
    # Copy to Windows Drive
    rsync -rtuvc --progress --delete-delay ~/wynZFS/Wynand/Backups /mnt/328E16488E16054F/AntergosBackups

    #Upload to mega.nz
    megasync
    # I might just crontab this eventually

    # If i ever want to kill it after a time use wait and;
    # kill -- $(ps -e | grep "megasync" | grep -v grep | awk "{print $1}")
fi
