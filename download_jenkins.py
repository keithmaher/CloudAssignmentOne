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


#
# Check to see if jenkins is running
# If not running download and install
#
def download_jenkins():
	try:
		check_jenkins = 'ps -A | grep jenkins'
		start_jenkins = """#!/bin/bash
		sudo yum install java-1.8.0-openjdk* -y
		sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins.io/redhat/jenkins.repo
		sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
		sudo yum install jenkins -y
		sudo service jenkins start"""

		run(check_jenkins, check=True, shell=True)
		message("Jenkins IS running")

	except CalledProcessError:
		message("Jenkins IS NOT running")
		message("Starting Jenkins")
		try:
			run(start_jenkins, check=True, shell=True)
			message("Jenkins IS running")

		except CalledProcessError:
			message("Jenkins IS NOT running")


# Define a main() function.
def main():
	download_jenkins()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
