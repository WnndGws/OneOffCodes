#!/usr/bin/python3
## Utility to test if package exists as a snap, and installs it

import re
import subprocess


def get_installed_packages():
    raw_installed_packages = subprocess.check_output(["pikaur", "-Q"])
    installed_packages = []
    for item in raw_installed_packages.splitlines():
        installed_packages.append(item.split(b" ")[0])
    return installed_packages


def check_snaps():
    installed_packages = get_installed_packages()
    found_snaps = []
    for package in installed_packages:
        if not re.findall(r"^lib.*", package.decode()):
            snap_found = subprocess.check_output(["snap", "find", package.decode()])
            if snap_found != (b""):
                found_snaps.append(package.decode())
    return found_snaps


found_snaps = check_snaps()
