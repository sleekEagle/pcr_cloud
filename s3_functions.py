#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:06:23 2019

@author: sleek_eagle
"""
import boto3
import set_env
import os


#initialize bucket and return it
def get_bucket():
    key_id=set_env.get_env('aws_access_key_id')
    secret_key=set_env.get_env('aws_secret_access_key')
    s3 = boto3.resource(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
    )
    global pcr_storage
    pcr_storage=s3.Bucket('pcr-storage')
    
#list all items in the bucket
def list_items():
    obj_list=[]
    try:
        all_objects=pcr_storage.objects.all()
        for obj in all_objects:
            obj_list.append(obj.key)
    except Exception as e:
        print(e)
        return -1
    return obj_list

#list all items in the bucket
def get_item_num():
    try:
        l=len(list(pcr_storage.objects.all()))
    except Exception as e:
        print(e)
        return -1
    return l

import sys
import threading

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush() 
            
#put object into bucket
def upload_file(file_name,dir_name,is_progress=False):
    name=file_name.split('/')[-1]
    try:
        dep_id=set_env.get_env('dep_id')
        if(is_progress):
            res=pcr_storage.upload_file(Filename=file_name,Key=dep_id+'/'+dir_name+'/'+name,Callback=ProgressPercentage(file_name))
        else:
            res=pcr_storage.upload_file(Filename=file_name,Key=dep_id+'/'+dir_name+'/'+name)

    except Exception as e:
        print(str(e))
        
def download_file(target_file,cloud_file):
    try:
        pcr_storage.download_file(Key=cloud_file,Filename=target_file)
    except Exception as e:
        print(str(e))
        
def unique(list1):
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

def get_depids():
    set_env.read_param()
    get_bucket()            
    items=list_items()
    dirs=[str(item.split('/')[0]) for item in items]
    dirs=unique(dirs)
    ids=",".join(dirs)
    return ids