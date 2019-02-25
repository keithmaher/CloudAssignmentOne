#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

from functions import *


#
# This function is designed to launch an aws EC2 instance.
# It contains user data to install httpd(Apache)
# httpd is not started on purpose so when check_webserver
# runs it will see it is not running and start it.
# This function Returns the instance ID
#
def launch_instance():

    user_data_script = """#!/bin/bash
    echo "Updating yum" >> /tmp/log.txt
    sudo yum update -y
    echo "Installing Apache" >> /tmp/log.txt
    sudo yum install httpd -y
    sudo systemctl enable httpd"""

    instance = ec2.create_instances(
        ImageId='ami-0bdb1d6c15a40392c',
        KeyName='Keiths_KeyPair',
        SecurityGroups=[
            'collegeSSH'
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Assignment One'
                    },
                ]
            },
        ],
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        UserData=user_data_script
    )

    message("New instance created with ID: "+instance[0].id)
    new_instance_id = instance[0].id
    return new_instance_id


# Define a main() function.
def main():

    # Launch an instance and return instance Id
    instance_id = launch_instance()

    # Check the instance for Apache
    instance_dns = copy_and_check(instance_id)

    # Gets the micro seconds just to add to the user input for the bucket name
    now = datetime.datetime.now()
    micro = str(now.microsecond)

    # Prompt the user to name the S3 bucket
    name_input = input("Please name your S3 storage bucket (lowercase) -> ")
    # Changes the input to lowercase
    bucket_name_input = name_input.lower()

    # Create S3 bucket using the user input and micro
    # Returns the unique bucket name
    bucket_name = create_bucket(bucket_name_input, micro)

    # Upload an image to the S3 bucket using the bucket name returned prior
    upload_img(bucket_name)

    # Create a new home page for the IP od the instance.
    create_new_home_page(bucket_name, instance_dns)

    # Download and install Jenkins - Additional Features
    download_jenkins(instance_dns)

    # Check memory usage and display to the user - Non functional issues
    memory_usage(instance_dns)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
