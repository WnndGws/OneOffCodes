#!/bin/zsh
## Moves lines from created aconfmgr to seperate files


cat ./99-unsorted.sh | grep 'C.*File ' >> 98.tmp; cat ./99-unsorted.sh | grep 'C.*Link ' >> 98.tmp; sort 98.tmp | uniq -u >> ./04-AddFiles.sh; rm -f 98.tmp
cat ./99-unsorted.sh | grep 'AddPackage ' >> 98.tmp; sort 98.tmp | uniq -u >> ./02-Packages.sh; rm -f 98.tmp
cat ./99-unsorted.sh | grep 'RemovePackage ' >> 98.tmp; sort 98.tmp | uniq -u >> ./05-RemovePackages.sh; rm -f 98.tmp
cat ./02-Packages.sh | grep 'foreign' >> 98.tmp; sort 98.tmp | uniq -u >> ./03-ForeignPackages.sh; rm -f 98.tmp
sed -i '/--foreign/d' ./02-Packages.sh
rm -f ./99-unsorted.sh
