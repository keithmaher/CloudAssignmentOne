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
from subprocess import *
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
        message("Instance DNS : " + dns)
        message("Instance State : " + state)

        try:
            ssh = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@'+dns+' sudo yum install python37 -y'
            scp = 'scp -i /home/keithmaher/Keiths_KeyPair.pem check_webserver.py ec2-user@'+dns+':/tmp'
            upload = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@'+dns+' python3 /tmp/check_webserver.py'

            run(ssh, check=True, shell=True)
            run(scp, check=True, shell=True)
            run(upload, check=True, shell=True)

        except CalledProcessError:
            message('something is Wrong')
            message('Trying again')
            run(ssh, shell=True)
            run(scp, shell=True)
            run(upload, shell=True)

        return dns


def create_bucket(bucket_name_input, micro):
    bucket_name = bucket_name_input+'-'+micro

    try:
        response = s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        message(response)
        return bucket_name
    except Exception as error:
        message(error)


def upload_img(bucket_name_in):
    bucket_name = bucket_name_in
    object_name = 'image.jpg'

    try:
        response = s3.Object(bucket_name, object_name).put(ACL='public-read', ContentType='image/jpeg',Body=open(object_name, 'rb'))
        message(response)
    except Exception as error:
        message(error)


def create_new_home_page(bucket_name_in, dns):

    bucket_name = bucket_name_in
    object_name = 'image.jpg'

    try:
        url = "https://s3-eu-west-1.amazonaws.com/"+bucket_name+"/"+object_name
        tag = "<!DOCTYPE html><html><head><title>Assignment One</title></head><body><h1>Assignment One</h1><p>Image displaying from</p><p><a href='"+url+"' target='_blank'>"+url+"</a></p><hr><br><img src='"+url+"' height='500px' width='500px'></body></html>"
        index = open("index.html", "w")
        index.write(tag)
        index.close()

        touch_index = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@'+dns+' sudo touch /var/www/html/index.html'
        change_permissiona = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@'+dns+' sudo chmod 777 /var/www/html/index.html'
        scp_file = 'scp -i /home/keithmaher/Keiths_KeyPair.pem index.html ec2-user@'+dns+':/var/www/html/'
        run(touch_index, check=True, shell=True)
        run(change_permissiona, check=True, shell=True)
        run(scp_file, check=True, shell=True)

        webbrowser.get('firefox').open_new_tab(url)

    except CalledProcessError:
        message('something is Wrong')
        message('Trying again')
        run(touch_index, shell=True)
        run(change_permissiona, shell=True)
        run(scp_file, shell=True)


def download_jenkins(dns):

    try:
        scp = 'scp -i /home/keithmaher/Keiths_KeyPair.pem download_jenkins.py ec2-user@'+dns+':/tmp'
        upload = 'ssh -i /home/keithmaher/Keiths_KeyPair.pem ec2-user@'+dns+' python3 /tmp/download_jenkins.py'

        run(scp, check=True, shell=True)
        run(upload, check=True, shell=True)

    except CalledProcessError:
        message('something is Wrong')
        message('Trying again')
        run(scp, shell=True)
        run(upload, shell=True)

