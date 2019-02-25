#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# http://pypi.python.org/pypi/psutil/

from subprocess import *


def message(text):
    print("* * * * * * * * * * * * * * * * *")
    print(text)
    print("* * * * * * * * * * * * * * * * *")


#
# Check and display memory status to the user
#
def check_memory():

    message('Checking memory status')
    try:
        check_memory_cmd = 'sudo cat /proc/meminfo'
        run(check_memory_cmd, check=True, shell=True)

    except CalledProcessError:
        print('something is Wrong')


# Define a main() function.
def main():
    check_memory()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
