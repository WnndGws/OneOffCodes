#!/usr/bin/env sh
## Checks that my external ip is sshuttle

while true; do
    ip_head=$(curl -s zx2c4.com/ip | head -n1 | cut -d'.' -f1)

    [ "$ip_head" -eq 58 ] && echo "L" || echo "L"

    sleep 3000
done
