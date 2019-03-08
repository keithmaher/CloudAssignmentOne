#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

from functions import *


# Define a main() function.
def main():

    # Start message
    start()

    # Take some user inputs for the bucket name
    bucket_name = bucket_user_input()

    # Take user input for the instance name
    instance_name = instance_user_input()

    # Start Automation message
    start_auto()
    sleep(2)

    # Launch an instance and return instance Id
    instance_id = launch_instance(instance_name)

    # Check the instance for Apache
    instance_dns = copy_and_check(instance_id)

    # Create S3 bucket using the user input
    create_bucket(bucket_name)

    # Upload an image to the S3 bucket using the bucket name returned prior
    upload_img(bucket_name)

    # Create a new home page for the IP od the instance.
    create_new_home_page(bucket_name, instance_dns)

    # Download and install Jenkins - Additional Features
    download_jenkins(instance_dns)

    # Check memory usage and display to the user - Non functional issues
    memory_usage(instance_dns)

    # Finished message
    finished()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
