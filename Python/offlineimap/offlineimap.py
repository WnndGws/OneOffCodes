#!/usr/bin/python
## Runs offline imap

import subprocess

def run_offlineimap():
    subprocess.call(["killall", "-9", "offlineimap"])
    subprocess.Popen(["offlineimap", "-o", "-u", "quiet"])

if __name__ == '__main__':
    run_offlineimap()
