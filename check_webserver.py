#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

from subprocess import *


def message(text):
	print("* * * * * * * * * * * * * * * * *")
	print(text)
	print("* * * * * * * * * * * * * * * * *")


def checkhttpd():
	try:
		checkhttpd = 'ps -A | grep httpd'
		starthttpd = """#!/bin/bash
		sudo yum install httpd -y
		sudo systemctl enable httpd
		sudo systemctl start httpd"""

		run(checkhttpd, check=True, shell=True)
		message("Web Server IS running")

	except CalledProcessError:
		message("Web Server IS NOT running")
		message("Starting Web Server")
		try:
			run(starthttpd, check=True, shell=True)
			message("Web Server IS running")

		except CalledProcessError:
			message("Web Server IS NOT running")


# Define a main() function.
def main():
	checkhttpd()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()

