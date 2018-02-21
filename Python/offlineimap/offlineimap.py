#!/usr/bin/python
## Runs offline imap

import subprocess

def run_offlineimap():
    subprocess.call(["killall", "-9", "offlineimap"])
    subprocess.call(["offlineimap", "-o"])

if __name__ == '__main__':
    run_offlineimap()
