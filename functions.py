#!/usr/bin/env python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# http://pypi.python.org/pypi/psutil/

import time
import datetime
import sys
import boto3
from subprocess import run
import webbrowser
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')



def message(text):
    print("* * * * * * * * * * * * * * * * *")
    print(text)
    print("* * * * * * * * * * * * * * * * *")




def copy_and_check(id):
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-id',
        'Values': [id]}])

    for instance in running_instances:
        message("Instance pending...")
        message("Waiting for it to run...")
        instance.wait_until_running()
        message("Configuring last few items...")
        time.sleep(2)

    for instance in running_instances:
        time.sleep(2)
        state = instance.state['Name']
        name = instance.id
        dns = instance.public_dns_name
        message("Connecting to: " + name)
        message("DNS : " + dns)
        message("State : " + state)

        run("ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@"+dns+" sudo yum install python37 -y", shell=True)
        run("scp -i /home/keithmaher/Keiths_KeyPair.pem check_webserver.py ec2-user@"+dns+":/tmp", shell=True)
        run("ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@"+dns+" python3 /tmp/check_webserver.py", shell=True)
        return dns



def create_bucket(micro):
    bucket_name = 'witcloudassignmentone2019'+micro
    try:
        response = s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        message(response)
        return bucket_name
    except Exception as error:
        message(error)


def upload_img(bucket_nameIn):
    bucket_name = bucket_nameIn
    object_name = 'image.jpg'

    try:
        response = s3.Object(bucket_name, object_name).put(ACL='public-read', ContentType='image/jpeg',Body=open(object_name, 'rb'))
        message(response)
    except Exception as error:
        message(error)


def create_new_home_page(bucket_nameIn, dns):

    bucket_name = bucket_nameIn
    object_name = 'image.jpg'

    try:
        url = "https://s3-eu-west-1.amazonaws.com/"+bucket_name+"/"+object_name
        tag = "<!DOCTYPE html><html><body><img src='" + url + "'></body></html>"
        f = open("index.html", "w")
        f.write(tag)
        f.close()

        run("ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@"+dns+ " sudo touch /var/www/html/index.html", shell=True)
        run("ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@"+dns+ " sudo chmod 777 /var/www/html/index.html", shell=True)
        run("scp -i /home/keithmaher/Keiths_KeyPair.pem index.html ec2-user@"+dns+ ":/var/www/html/", shell=True)
        webbrowser.get('firefox').open_new_tab(url)

    except Exception as error:
        message(error)