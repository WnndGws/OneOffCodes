#!/usr/bin/zsh
## Script to run a few things to make my dotfiles

dir=$HOME/Git/dotfiles3.0
computer="$1"
if [ -z "$computer" ]; then
    echo "Please specify a computer"
    echo "(exit)"
    exit 1
fi

# Need to pull changed files in case changed anything on other computer
echo "Pulling from git....."
cd $dir
git pull --all

echo "Updating dotfiles (may take some time)....."
dotgit decrypt
dotgit update $computer
dotgit encrypt
dotgit generate

# Get list of installed packages
echo "Getting list of packages...."
pacman -Qe | awk '{print $1}' > $dir/explicit_packages.txt
awk 'FNR==NR {a[$0]++; next} !a[$0]' $dir/packages_base.txt $dir/explicit_packages.txt > $dir/packages_unique.txt
sed -i '/xorg-.*/d' $dir/packages_unique.txt
sed -i '/xf86-.*/d' $dir/packages_unique.txt
rm $dir/explicit_packages.txt

git add .
git commit -S -m "Updated packages" .
git push
