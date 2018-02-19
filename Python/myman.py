#!/usr/bin/python
## Use tldr for man if exits, otherwise rtfm

import click
import os
import re
import subprocess

@click.group()
def run_try_tldr():
    pass

@run_try_tldr.command()
@click.option('--program', help="The program who's manualw e want to read")
def try_tldr(program):
    """Checks to see if there is a tldr"""
    success = False
    program_list = subprocess.check_output(["tldr", "--list-all", "--single-column"]).strip()
    match = re.findall(r'(%s)' %program, str(program_list))
    if len(match) > 0:
        try:
            args = ["tldr", program]
            subprocess.call(args)
            success = True
        except subprocess.CalledProcessError:
            success = False
    if not success:
        try:
            args = ["vimman", program]
            subprocess.call(args)
            success = True
        except subprocess.CalledProcessError:
            success = False
    if not success:
        try:
            args = [program, "--help"]
            subprocess.call(args)
            success = True
        except subprocess.CalledProcessError:
            success = False

TRY_TLDR = click.CommandCollection(sources=[run_try_tldr])
if __name__ == '__main__':
    TRY_TLDR()
