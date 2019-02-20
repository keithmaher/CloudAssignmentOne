#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/


# http://pypi.python.org/pypi/psutil/
import time
from subprocess import run

result = run("sudo service httpd status",  shell=True)
code = result.returncode

if(code != 0):
	print("Apache Web Server Is Inactive")
	print("Starting Apache Web Server")
	run("sudo yum install httpd", shell=True)
	run("sudo systemctl enable httpd", shell=True)
	run("sudo service httpd start", shell=True)
	time.sleep(2)

result = run("sudo service httpd status",  shell=True)
code = result.returncode

if(code == 0):
	print("Apache Web Server Is Active")
	time.sleep(2)


