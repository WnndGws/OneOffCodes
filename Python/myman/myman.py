#!/usr/bin/python
## Use tldr for man if exits, otherwise rtfm

import click
import os
import re
import subprocess


def get_programs(ctx, args, incomplete):
    programs = subprocess.run(["pacman", "-Qqe"], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    return [k for k in programs if incomplete in k]

@click.command()
@click.argument("program", type=click.STRING, autocompletion=get_programs)
def try_tldr(program):
    """Checks to see if there is a tldr"""
    success = False
    program_list = subprocess.check_output(["tldr", "--list"]).strip()
    match = re.findall(r"(%s)" % program, str(program_list))
    if len(match) > 0:
        try:
            args = ["tldr", program]
            subprocess.check_call(args)
            success = True
        except subprocess.CalledProcessError:
            success = False
    if not success:
        try:
            args = ["man", program]
            subprocess.check_call(args)
            success = True
        except subprocess.CalledProcessError:
            success = False
    if not success:
        try:
            args = [program, "--help"]
            subprocess.call(args)
            success = True
        except OSError:
            success = False
            click.echo(
                f"There either is no program called {program}, or it does not have a man-page"
            )

if __name__ == "__main__":
    try_tldr()
