# System - Core

IgnorePath '*cache*'

# ld
IgnorePath '/etc/ld.so.cache' # "File containing an ordered list of libraries found in the directories specified in /etc/ld.so.conf, as well as those found in the trusted directories."

# info
IgnorePath '/usr/share/info/dir'

# locate
IgnorePath '/var/lib/mlocate/mlocate.db' # 

# logrotate
IgnorePath '/var/lib/logrotate.status'

# upower
IgnorePath '/var/lib/upower/history-*.dat'

# udev
IgnorePath '/etc/udev/hwdb.bin' # https://www.freedesktop.org/software/systemd/man/hwdb.html

# System - Core - Configuration

# locale
IgnorePath '/usr/lib/locale/locale-archive'

# systemd
IgnorePath '/var/lib/systemd/catalog/database' # Message catalog cache
#IgnorePath '/var/lib/systemd/clock' # systemd-timesyncd - "This file contains the timestamp of the last successful synchronization."
IgnorePath '/var/lib/systemd/coredump/core.*.lz4' # Core dumps
IgnorePath '/var/lib/systemd/random-seed'
IgnorePath '/var/lib/systemd/timers/stamp-*.timer' # systemd timer timestamps

# systemd-update-done.service
IgnorePath '/etc/.updated'
IgnorePath '/var/.updated'

# cron

IgnorePath '/var/spool/anacron/cron.daily' # anacron (provided by cronie)
IgnorePath '/var/spool/anacron/cron.monthly' # ditto
IgnorePath '/var/spool/anacron/cron.weekly' # ditto

# systemd journal
IgnorePath '/var/log/journal'

# System - Core - Configuration - Accounts

# passwd
IgnorePath '/etc/.pwd.lock' # http://blog.dailystuff.nl/2011/08/the-hunt-for-etc-pwd-lock/

# User accounts
IgnorePath '/etc/group-' # 
IgnorePath '/etc/gshadow' # 
IgnorePath '/etc/gshadow-' # 
IgnorePath '/etc/passwd-' # 
IgnorePath '/etc/shadow' # 
IgnorePath '/etc/shadow-' # 

# sudo password
IgnorePath '/usr/local/etc/sudopasswd' # sudo mkdir -p /usr/local/etc ; sudo htpasswd -cB /usr/local/etc/sudopasswd vladimir ; sudo chmod 000 /usr/local/etc/sudopasswd

# Login attempts
IgnorePath '/var/log/btmp'
IgnorePath '/var/log/btmp.*'
IgnorePath '/var/log/faillog'
IgnorePath '/var/log/lastlog'
IgnorePath '/var/log/wtmp'
IgnorePath '/var/log/wtmp.*'

# System - Core - Tools

# System - Boot

# Boot
IgnorePath '/boot/EFI/grub/grubx64.efi' # grub for EFI
IgnorePath '/boot/grub' # grub's install
IgnorePath '/boot/grub/grub.cfg' # grub config
IgnorePath '/boot/initramfs-*.img'
IgnorePath '/boot/shellx64_v2.efi'

IgnorePath '/boot/vmlinuz-linux-git'

# grub2efi
IgnorePath '/var/local/grub2efi/links'

# Linux kernel
#IgnorePath '/usr/lib/modules' # Experimental kernel modules
IgnorePath '/usr/lib/modules/*-ARCH/modules.alias' # Modified for nvidia
IgnorePath '/usr/lib/modules/*-ARCH/modules.alias.bin' # Ditto
IgnorePath '/usr/lib/modules/*-ARCH/modules.dep' # Ditto
IgnorePath '/usr/lib/modules/*-ARCH/modules.dep.bin' # Ditto
IgnorePath '/usr/lib/modules/*-ARCH/modules.symbols' # Ditto
IgnorePath '/usr/lib/modules/*-ARCH/modules.symbols.bin' # Ditto

# System - Network

# ntp
IgnorePath '/var/lib/ntp/ntp.drift'

# samba
IgnorePath '/var/lib/samba/private/msg.sock/*'

IgnorePath '/var/lib/samba/account_policy.tdb' # Database
IgnorePath '/var/lib/samba/group_mapping.tdb' # Database
IgnorePath '/var/lib/samba/private/passdb.tdb' # Database
IgnorePath '/var/lib/samba/private/randseed.tdb' # Database
IgnorePath '/var/lib/samba/private/secrets.tdb' # Database
IgnorePath '/var/lib/samba/registry.tdb' # Database
IgnorePath '/var/lib/samba/share_info.tdb' # Database

IgnorePath '/var/log/samba' # Log

# SSH
IgnorePath '/etc/ssh/*_key' # Host private keys
IgnorePath '/etc/ssh/*_key.pub' # Host public keys

# System - Network - VPN

# OpenVPN
IgnorePath '/etc/openvpn/*.key' # Private keys
IgnorePath '/etc/openvpn/*.conf' # Configuration files may contain embedded keys
IgnorePath '/etc/openvpn/*.ovpn' # Ditto
IgnorePath '/etc/openvpn/*.pem' # Certificates
IgnorePath '/etc/openvpn/*.crt' # Ditto
IgnorePath '/etc/openvpn/*.csr' # Signing requests
IgnorePath '/etc/openvpn/openvpn-status.log' # Log

# btrfs
IgnorePath '/var/lib/btrfs/scrub.status.*'

IgnorePath '/??' # Links for NTFS symlinks

# System - Storage - RAID

# LVM
IgnorePath '/etc/lvm/cache/.cache' # "The vgscan command scans all supported disk devices in the system looking for LVM physical volumes and volume groups. This builds the LVM cache in the /etc/lvm/.cache file, which maintains a listing of current LVM devices."

# System - Libraries

# GTK
IgnorePath '/etc/gtk-2.0/gdk-pixbuf.loaders'
IgnorePath '/usr/lib32/gdk-pixbuf-2.0/2.10.0/loaders.cache'
IgnorePath '/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache'

IgnorePath '/usr/lib32/gtk-2.0/2.10.0/immodules.cache'
IgnorePath '/usr/lib/gtk-2.0/2.10.0/immodules.cache'
IgnorePath '/usr/lib/gtk-3.0/3.0.0/immodules.cache'

# Gnome
IgnorePath '/usr/lib/gio/modules/giomodule.cache'
IgnorePath '/usr/share/glib-2.0/schemas/gschemas.compiled' # https://developer.gnome.org/gio/stable/glib-compile-schemas.html

# mimeinfo
IgnorePath '/usr/local/share/applications/mimeinfo.cache'
IgnorePath '/usr/share/applications/mimeinfo.cache'

# MIME database
IgnorePath '/usr/share/mime/aliases' # MIME aliases
IgnorePath '/usr/share/mime/*.xml' # Localizations
IgnorePath '/usr/share/mime/generic-icons'
IgnorePath '/usr/share/mime/globs' # File extensions
IgnorePath '/usr/share/mime/globs2' # Weighted file extensions?
IgnorePath '/usr/share/mime/icons'
IgnorePath '/usr/share/mime/magic' # Binary magic database
IgnorePath '/usr/share/mime/mime.cache' # Binary
IgnorePath '/usr/share/mime/subclasses'
IgnorePath '/usr/share/mime/treemagic' # Directory magic
IgnorePath '/usr/share/mime/types'
IgnorePath '/usr/share/mime/version'
IgnorePath '/usr/share/mime/XMLnamespaces'


# System - Misc


IgnorePath '/etc/xml/catalog' # http://xmlsoft.org/catalog.html

# System - Arch Linux

# pacman
IgnorePath '/var/lib/pacman/local/ALPM_DB_VERSION'
IgnorePath '/var/lib/pacman/local/*/changelog'
IgnorePath '/var/lib/pacman/local/*/desc'
IgnorePath '/var/lib/pacman/local/*/files'
IgnorePath '/var/lib/pacman/local/*/install'
IgnorePath '/var/lib/pacman/local/*/mtree'
IgnorePath '/var/lib/pacman/sync/*.db' # repos
IgnorePath '/var/lib/pacman/sync/*.db.sig' # repo sigs
IgnorePath '/var/lib/pacman/sync/*.files' # for pacman -F
IgnorePath '/etc/pacman.d/gnupg' # keyring
IgnorePath '/var/log/pacman.log' # Log

# Certificates

IgnorePath '/etc/ca-certificates/extracted' # WATCH ME
IgnorePath '/etc/ssl/certs' # Symlinks to the above

#####################################################################################################################

# Development - General

# Development - Languages - D

# Something keeps creating these mysterious symlinks...
IgnorePath '/usr/lib/libdruntime-ldc*.so.*'
IgnorePath '/usr/lib/libphobos2*.so.*'

# Development - Languages - Python

IgnorePath '/usr/lib/python2.7/site-packages/*.pyc'
IgnorePath '/usr/share/gcc-*/python/*/__pycache__/*.pyc'
IgnorePath '/usr/share/gdb/python/*/__pycache__/*.pyc'
IgnorePath '/usr/share/nautilus-python/extensions/*.pyc'

# atop
IgnorePath '/var/log/atop'

# Media - Audio

# ALSA
IgnorePath '/var/lib/alsa/asound.state'

# mpd
IgnorePath '/var/lib/mpd/.config/pulse/*-runtime'

# Media - Video

# vlc
IgnorePath '/usr/lib/vlc/plugins/plugins.dat'

# Desktop - Fonts

IgnorePath '/usr/share/fonts/misc/fonts.dir'
IgnorePath '/usr/share/fonts/misc/fonts.scale'
IgnorePath '/usr/share/fonts/OTF/fonts.dir'
IgnorePath '/usr/share/fonts/OTF/fonts.scale'
IgnorePath '/usr/share/fonts/ttf-brill/fonts.dir'
IgnorePath '/usr/share/fonts/ttf-brill/fonts.scale'
IgnorePath '/usr/share/fonts/TTF/fonts.dir'
IgnorePath '/usr/share/fonts/TTF/fonts.scale'
IgnorePath '/usr/share/fonts/Type1/fonts.dir'
IgnorePath '/usr/share/fonts/Type1/fonts.scale'

# Desktop - Environment

# icons
IgnorePath '/usr/share/icons/*/icon-theme.cache'

# Desktop - X11

# Logs
IgnorePath '/var/log/Xorg.*.log'
IgnorePath '/var/log/Xorg.*.log.old'

# Desktop - Apps - Office - Languages

# words
IgnorePath '/usr/share/dict/words'

# Services - Mail

# postfix - cache/temp
IgnorePath '/var/lib/postfix/master.lock' # 
IgnorePath '/var/spool/postfix/pid/master.pid' # 
IgnorePath '/var/spool/postfix/pid/unix.bounce' # 
IgnorePath '/var/spool/postfix/pid/unix.cleanup' # 
IgnorePath '/var/spool/postfix/pid/unix.defer' # 
IgnorePath '/var/spool/postfix/pid/unix.local' # 
IgnorePath '/var/spool/postfix/pid/unix.smtp' # 
IgnorePath '/var/spool/postfix/private/anvil' # 
IgnorePath '/var/spool/postfix/private/bounce' # 
IgnorePath '/var/spool/postfix/private/defer' # 
IgnorePath '/var/spool/postfix/private/discard' # 
IgnorePath '/var/spool/postfix/private/error' # 
IgnorePath '/var/spool/postfix/private/lmtp' # 
IgnorePath '/var/spool/postfix/private/local' # 
IgnorePath '/var/spool/postfix/private/proxymap' # 
IgnorePath '/var/spool/postfix/private/proxywrite' # 
IgnorePath '/var/spool/postfix/private/relay' # 
IgnorePath '/var/spool/postfix/private/retry' # 
IgnorePath '/var/spool/postfix/private/rewrite' # 
IgnorePath '/var/spool/postfix/private/scache' # 
IgnorePath '/var/spool/postfix/private/smtp' # 
IgnorePath '/var/spool/postfix/private/tlsmgr' # 
IgnorePath '/var/spool/postfix/private/trace' # 
IgnorePath '/var/spool/postfix/private/verify' # 
IgnorePath '/var/spool/postfix/private/virtual' # 
IgnorePath '/var/spool/postfix/public/cleanup' # 
IgnorePath '/var/spool/postfix/public/flush' # 
IgnorePath '/var/spool/postfix/public/pickup' # 
IgnorePath '/var/spool/postfix/public/qmgr' # 
IgnorePath '/var/spool/postfix/public/showq' # 

# postfix - data
IgnorePath '/etc/postfix/aliases.db'
IgnorePath '/var/spool/mail'
IgnorePath '/var/spool/postfix/maildrop'

# Services - Databases

# MariaDB
IgnorePath '/usr/data/aria_log.*'
IgnorePath '/usr/data/aria_log_control'
IgnorePath '/usr/data/ibdata1'
IgnorePath '/usr/data/ib_logfile*'
IgnorePath '/usr/data/mysql-bin.*'
IgnorePath '/usr/data/mysql'
IgnorePath '/usr/data/performance_schema/db.opt'
