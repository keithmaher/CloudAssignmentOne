#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/
import random
from time import sleep
import boto3
from subprocess import *
import re
from messages import *
import datetime
import sys
import webbrowser

ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')


def bucket_user_input():
    print("-------------------------------------------------------------------------\n"
          "Before we begin I need some small inputs\n"
          "This is required so I can fully automate this service\n"
          "Once you have entered these two details, you can then sit back and relax\n"
          "As the whole process is handled AUTOMATICALLY after that\n"
          "-------------------------------------------------------------------------")

    name_input = input("\nPlease name your S3 storage bucket -> ")
    # Changes the input to uppercase to check
    bucket_name_input = name_input.upper()

    while bucket_name_input.isupper():
        if re.match("^[a-zA-Z0-9_]*$", bucket_name_input):
            print("Thank you")
            bucket_name_input = bucket_name_input.lower()
        else:
            print("Invalid input\nTry again")
            name_input = input("\nPlease name your S3 storage bucket -> ")
            # Changes the input to uppercase to check
            bucket_name_input = name_input.upper()

    # Gets the micro seconds just to add to the user input for the bucket name
    now = datetime.datetime.now()
    micro_number = str(now.microsecond)
    random_number = random.randint(1, 9999999)
    bucket_name = bucket_name_input+'-'+str(random_number)+micro_number

    return bucket_name


def instance_user_input():
    instance_name_in = input("\nPlease name your EC2 instance -> ")
    instance_name = instance_name_in.upper()

    while instance_name.isupper():
        if re.match("^[a-zA-Z0-9_]*$", instance_name):
            print("Thank you")
            instance_name = instance_name.lower()
        else:
            print("Invalid input\nTry again")
            instance_name_in = input("\nPlease name your EC2 instance -> ")
            instance_name = instance_name_in.upper()

    print("-------------------------------------------------------------------------\n"
          "Now sit back, relax\n"
          "And let the automation do its work\n"
          "-------------------------------------------------------------------------")
    sleep(2)

    return instance_name


#
# This function is designed to launch an aws EC2 instance.
# It contains user data to install httpd(Apache)
# httpd is not started on purpose so when check_webserver
# runs it will see it is not running and start it.
# This function Returns the instance ID
#
def launch_instance(instance_name):

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
                        'Value': instance_name
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


#
# This function downloads python3 on the instance
# Copies a python file using scp up to the instance.
# The instance eId is passed in so it can be used to find the correct instance that was just created.
# It waits till the instance is running to get the DNS name of the instance
# Also waits 120 seconds for the user data to download. (yum update)
# Runs the check_webserver.py file.
#
def copy_and_check(instance_id):
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-id',
        'Values': [instance_id]}])

    for instance in running_instances:
        message("Instance pending...")
        message("Waiting for it to run...")
        instance.wait_until_running()
        message("Configuring last few items...")
        sleep(2)
        instance.reload()
        instance_state = instance.state['Name']
        instance_name = instance.id
        instance_dns = instance.public_dns_name
        message("Connecting to: " + instance_name)
        message("Instance DNS : " + instance_dns)
        message("Instance State : " + instance_state)

        i = 0
        while i < 155:
            i += 1
            count = 155 - i
            countdown = str(count)
            message("Waiting for user data to download")
            message("Avoiding yum locks and opening ports :" + countdown)
            sleep(1)

        try:
            ssh_install_python = 'ssh -t -o StrictHostKeyChecking=no -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + instance_dns + ' sudo yum install python3 -y'
            scp_check_webserver = 'scp -i /home/keithmaher/Keiths_KeyPair.pem check_webserver.py ec2-user@' + instance_dns + ':/tmp'
            run_file = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + instance_dns + ' python3 /tmp/check_webserver.py'

            run(ssh_install_python, check=True, shell=True)
            run(scp_check_webserver, check=True, shell=True)
            run(run_file, check=True, shell=True)

        except CalledProcessError:
            message('something is Wrong')
            message('Trying again')
            run(ssh_install_python, shell=True)
            run(scp_check_webserver, shell=True)
            run(run_file, shell=True)

        return instance_dns


#
# Create an S3 bucket using the user-input and micro to make a unique bucket name/
# Return the unique bucket name.
#
def create_bucket(bucket_name):
    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        message(str(response))
    except Exception as error:
        message(str(error))


#
# Upload the image image.jpg to the S3 bucket.
# Change the permissions of the image to make it accessible.
#
def upload_img(bucket_name):
    object_name = 'image.jpg'
    try:
        response = s3.Object(bucket_name, object_name).put(ACL='public-read', ContentType='image/jpeg', Body=open(object_name, 'rb'))
        message(str(response))
    except Exception as error:
        message(str(error))


#
# Create new home page for Apache with the image that is stored in the S3 bucket
# Touch a file called index.html
# Change permissions
# Create the html file locally and then scp the file up to the instance
#
def create_new_home_page(bucket_name, dns):
    object_name = 'image.jpg'

    try:
        image_url = "https://s3-eu-west-1.amazonaws.com/"+bucket_name+"/"+object_name
        html_tag = "<!DOCTYPE html><html><head><title>Assignment One</title></head><body><h1>Assignment One</h1><p>Image displaying from</p><p><a href='" + image_url + "' target='_blank'>" + image_url + "</a></p><hr><br><img src='" + image_url + "' height='500px' width='700px'></body></html>"
        index = open("index.html", "w")
        index.write(html_tag)
        index.close()

        touch_index = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + dns + ' sudo touch /var/www/html/index.html'
        change_permissions = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + dns + ' sudo chmod 777 /var/www/html/index.html'
        scp_index = 'scp -i /home/keithmaher/Keiths_KeyPair.pem index.html ec2-user@' + dns + ':/var/www/html/'

        run(touch_index, check=True, shell=True)
        run(change_permissions, check=True, shell=True)
        run(scp_index, check=True, shell=True)

    except CalledProcessError:
        message('something is Wrong')
        message('Trying again')
        run(touch_index, shell=True)
        run(change_permissions, shell=True)
        run(scp_index, shell=True)


#
# scp download_jenkins.py file to the instance and run the file
#
def download_jenkins(dns):
    try:
        scp_download_jenkins = 'scp -i /home/keithmaher/Keiths_KeyPair.pem download_jenkins.py ec2-user@' + dns + ':/tmp'
        run_file = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + dns + ' python3 /tmp/download_jenkins.py'

        run(scp_download_jenkins, check=True, shell=True)
        run(run_file, check=True, shell=True)

    except CalledProcessError:
        message('something is Wrong')
        message('Trying again')
        run(scp_download_jenkins, shell=True)
        run(run_file, shell=True)


#
# scp check_memory.py file to the instance and run the file
#
def memory_usage(dns):
    try:
        scp_check_memory = 'scp -i /home/keithmaher/Keiths_KeyPair.pem check_memory.py ec2-user@' + dns + ':/tmp'
        run_file = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@' + dns + ' python3 /tmp/check_memory.py'

        run(scp_check_memory, check=True, shell=True)
        run(run_file, check=True, shell=True)

    except CalledProcessError:
        message('something is Wrong')
