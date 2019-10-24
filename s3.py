#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:06:23 2019

@author: sleek_eagle
"""
import boto3

DEP_NAME='dep_1'
DIR_TYPES = ['audio','features','classifications']


#initialize bucket and return it
def get_bucket():
    s3 = boto3.resource(
        's3',
        aws_access_key_id='blah',
        aws_secret_access_key='blah',
    )
    global pcr_storage
    pcr_storage=s3.Bucket('pcr-storage')

#list all items in the bucket
def list_items(bucket):
    obj_list=[]
    for obj in pcr_storage.objects.all():
        obj_list.append(obj.key)
    return obj_list

#put object into bucket
def upload_file(file_name,file_type):
    if(not(file_type in DIR_TYPES)):
            print('Incorrect file type. Applicable types are : \n 1. audio \n 2. features \n 3. classifications')
            return -1
    name=file_name.split('/')[-1]
    try:
        res=pcr_storage.upload_file(Filename=file_name,Key=DEP_NAME+'/'+file_type+'/'+name)
        print(res)
    except Exception as e:
        print(str(e))
        
def download_file(target_file,cloud_file):
    try:
        pcr_storage.download_file(Key=cloud_file,Filename=target_file)
    except Exception as e:
        print(str(e))

    


