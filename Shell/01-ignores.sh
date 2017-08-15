IgnorePath '/wynZFS'
IgnorePath '/wynZFS/*'
IgnorePath '*cache*'
IgnorePath '/usr/lib/modules/*' # don't want kernel
IgnorePath '/usr/lib/modules' # don't want kernel
IgnorePath '/boot'
IgnorePath '/boot/*'
IgnorePath '*.sock*' # anything with sockets need to be fresh

# /var
IgnorePath '/var/lib'
IgnorePath '/var/db' # databases
IgnorePath '/var/log' # logs
IgnorePath '/var/spool' # spool
IgnorePath '/var/.updated' # systemd-update-done.service
IgnorePath '/var/lib/pacman/local/*' # package metadata
IgnorePath '/var/lib/pacman/sync/*' # repos
IgnorePath '/var/lib/pacman/sync/*.db.sig' # repo sigs
IgnorePath '/var/lib/systemd/coredump/*'

# /etc
IgnorePath '/etc/pacman.d/gnupg/*' # want fresh install each time
IgnorePath '/etc/dhcpcd.duid'
IgnorePath '/etc/machine-id'
IgnorePath '/etc/ld.so.cache' # "File containing an ordered list of libraries found in the directories specified in /etc/ld.so.conf
IgnorePath '/etc/udev/hwdb.bin' # https://www.freedesktop.org/software/systemd/man/hwdb.html
IgnorePath '/etc/.pwd.lock' # passwd; http://blog.dailystuff.nl/2011/08/the-hunt-for-etc-pwd-lock/
IgnorePath '/etc/.updated' # systemd-update-done.service
IgnorePath '/etc/ca-certificates/extracted' # certs
IgnorePath '/etc/fstab'
IgnorePath '/etc/group'
IgnorePath '/etc/group-'
IgnorePath '/etc/gshadow'
IgnorePath '/etc/gshadow-'
IgnorePath '/etc/gtk-2.0/gdk-pixbuf.loaders' # GTK
IgnorePath '/etc/lvm/cache/.cache' # LVM cache
IgnorePath '/etc/pacman.d/mirrorlist.pacnew'
IgnorePath '/etc/pacman.d/gnupg' # pacman keyring
IgnorePath '/etc/passwd-'
IgnorePath '/etc/shadow'
IgnorePath '/etc/shadow-'
IgnorePath '/etc/ssh/*_key' # SSH Host private keys
IgnorePath '/etc/ssh/*_key.pub' # SSH Host public keys
IgnorePath '/etc/ssl/certs' # certs Symlinks
IgnorePath '/etc/texmf'
IgnorePath '/etc/xml/catalog' # http://xmlsoft.org/catalog.html
