#!/usr/bin/python3

# INET4031
# Abdirahman Hashi
# Date Created: [enter date]
# Date Last Modified: [enter date]

import os
import re
import sys

def main():
    # Prompt user interactively even if stdin is redirected from a file
    if sys.stdin.isatty():
        dry_run = input("Run in dry-run mode? (Y/N): ").strip().upper()
    else:
        # Use /dev/tty to read from keyboard when input is redirected
        dry_run = input_from_tty("Run in dry-run mode? (Y/N): ").strip().upper()

    for line in sys.stdin:
        match = re.match("^#", line)
        fields = line.strip().split(':')

        # Handle commented lines and bad data differently based on mode
        if match:
            if dry_run == "Y":
                print(f"Skipping commented line: {line.strip()}")
            continue

        if len(fields) != 5:
            if dry_run == "Y":
                print(f"Error: Bad line format -> {line.strip()}")
            continue

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        print(f"==> Creating account for {username}...")
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        print(cmd)
        if dry_run != "Y":
            os.system(cmd)

        print(f"==> Setting the password for {username}...")
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        print(cmd)
        if dry_run != "Y":
            os.system(cmd)

        for group in groups:
            if group != '-':
                print(f"==> Assigning {username} to the {group} group...")
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)
                if dry_run != "Y":
                    os.system(cmd)

def input_from_tty(prompt):
    """Reads input from the user's keyboard even when stdin is redirected."""
    with open("/dev/tty", "r") as tty:
        print(prompt, end='', flush=True)
        return tty.readline().strip()

if __name__ == '__main__':
    main()

