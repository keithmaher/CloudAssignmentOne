#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/


# http://pypi.python.org/pypi/psutil/

# import time
# import sys
# import boto3
# ec2 = boto3.resource('ec2')
# # s3 = boto3.resource('s3')
from functions import *


def launch_instance():

    user_data_script = """#!/bin/bash
    echo "Updating yum" >> /tmp/log.txt
    sudo yum update -y
    echo "Installing java 1.8" >> /tmp/log.txt
    sudo yum install java-1.8.0-openjdk* -y
    echo "Getting Jenkins repo" >> /tmp/log.txt
    sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins.io/redhat/jenkins.repo
    echo "Importing key" >> /tmp/log.txt
    sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
    echo "Installing Jenkins" >> /tmp/log.txt
    sudo yum install jenkins -y
    echo "Starting Jenkins" >> /tmp/log.txt
    sudo service jenkins start
    echo "Installing Apache" >> /tmp/log.txt
    sudo yum install httpd -y
    sudo systemctl enable httpd
    sudo cp /var/lib/jenkins/secrets/initialAdminPassword /tmp/password.txt 
    echo Password for Jenkins in password.txt >> /tmp/log.txt"""

    userdatae = """#!/bin/bash
    echo "Updating yum" >> /tmp/log.txt"""

    instance = ec2.create_instances(
        ImageId= 'ami-0bdb1d6c15a40392c',
        KeyName= 'Keiths_KeyPair',
        SecurityGroups = [
            'collegeSSH'
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Exercise4'
                    },
                ]
            },
        ],
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        UserData=userdatae
    )

    message("New instance created with ID: "+instance[0].id)
    newInstance = instance[0].id
    return newInstance

https://github.com/keithmaher/CloudAssignmentOne.git



def main():

    instance_id = launch_instance()
    dns = copy_and_check(instance_id)
    now = datetime.datetime.now()
    micro = str(now.microsecond)
    bucket_name = create_bucket(micro)
    upload_img(bucket_name)
    create_new_home_page(bucket_name, dns)


if __name__ == '__main__':
    main()