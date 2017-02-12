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
borg check ~/wynZFS/Wynand/Backups/GoogleDrive/ &>> ~/wynZFS/Wynand/Backups/.tmp.txt
borg check ~/wynZFS/Wynand/Backups/Antergos/ &>> ~/wynZFS/Wynand/Backups/.tmp.txt
if grep -Fq "Completed repository check, errors found" ~/wynZFS/Wynand/Backups/.tmp.txt
then
    notify-send "Backup Error" "There was an error found in one of the Borg backups"
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt
else
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt
    
    # Only copy files to SDD and mega if no errors
   
    echo "Finding duplicates..."
    # Need to see if any files changed, and delete them from mega so that the new files can be uploaded
    diff -qrN ~/wynZFS/Wynand/Backups /mnt/328E16488E16054F/AntergosBackups/Backups | cut -d \  -f 4 >~/wynZFS/Wynand/Backups/.tmp.txt
    cat ~/wynZFS/Wynand/Backups/.tmp.txt | xargs -i rm -rf {}
    sed -i 's/\/mnt\/328E16488E16054F\/AntergosBackups\//\/Root\//g' ~/wynZFS/Wynand/Backups/.tmp.txt
    cat ~/wynZFS/Wynand/Backups/.tmp.txt | xargs -i megarm -u ${mega_user} -p ${mega_password} {}
    rm -rf ~/wynZFS/Wynand/Backups/.tmp.txt

    echo "Copying........."
    # Copy to Windows Drive
    cp -Lruv ~/wynZFS/Wynand/Backups /mnt/328E16488E16054F/AntergosBackups

    #Upload to mega.nz
    echo "Uploading......."
#   nocorrect megacopy -u ${mega_user} -p ${mega_password} -r /Root/Backups -l  ~/wynZFS/Wynand/Backups
fi
