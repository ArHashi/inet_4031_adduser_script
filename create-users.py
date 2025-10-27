#!/usr/bin/python3

# INET4031
# Abdirahman Hashi
# Data Created: 10/27/25
# Date Last Modified: 10/27/25

# Import modules used for system commands, regular expressions, and input reading
import os	# allows execution of system-level commands (adduser)
import re	# used to match and filter lines using regular expressions
import sys	# allows reading input from stdin (piped files like create-users.input)


def main():
    # Reads each line from the input file (create-users.input) one at a time
    for line in sys.stdin:

        # Skips any line that starts with '#' (commented-out user)
        match = re.match("^#",line)

        # Splits each valid line into fields using ':' as a delimite
        fields = line.strip().split(':')

        # Skips the line if it is commented out OR does not have exactly 5 fields
        # This prevents errors if a line is malformed or incomplete
        if match or len(fields) != 5:
            continue

        # Assign variables to each field based on the order in the input file
        username = fields[0]	# username for the new account
        password = fields[1]	# password for the account
        gecos = "%s %s,,," % (fields[3],fields[2])	# first and last name for GECOS field

	# Splits the last field by commas to handle multiple groups per user
        groups = fields[4].split(',')

        # Print what would happen (without actually adding users)
        print("==> Creating account for %s..." % (username))
        # This builds the Linux command to create a new user with no password and full name info.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        # These lines show and then execute the command that creates the user account.
       	print (cmd)
        os.system(cmd)

        # Displays which user’s password is being set next.
        print("==> Setting the password for %s..." % (username))
        # Builds the command to set the user’s password using echo and passwd.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        # Shows and executes the password-setting command.
        print (cmd)
        os.system(cmd)

        for group in groups:
            # Shows and executes the password-setting command.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print (cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
