#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

from functions import *


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


def main():

    instance_id = launch_instance()
    instance_dns = copy_and_check(instance_id)
    now = datetime.datetime.now()
    micro = str(now.microsecond)
    name_input = input("Please name your S3 storage bucket (lowercase) -> ")
    bucket_name_input = name_input.lower()
    bucket_name = create_bucket(bucket_name_input, micro)
    upload_img(bucket_name)
    create_new_home_page(bucket_name, instance_dns)
    download_jenkins(instance_dns)
    memory_usage(instance_dns)


if __name__ == '__main__':
    main()
