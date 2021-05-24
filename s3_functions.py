#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:06:23 2019

@author: sleek_eagle
"""
import boto3
import file_system_tasks
import os
import Log
import hashlib
import file_system_tasks
import dep_data

#initialize bucket and return it
def get_bucket():
    credentials=file_system_tasks.get_parameters('s3_credentials.txt')
    key_id=credentials['Access key ID']
    secret_key=credentials['Secret access key']
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
        log_entry='in list_items of s3_functions exception='+str(e)
        Log.log_s3(log_entry)
        return -1
    return obj_list

#number of all items in the bucket
def get_item_num():
    try:
        l=len(list(pcr_storage.objects.all()))
    except Exception as e:
        print(e)
        log_entry='in get_item_num of s3_functions exception='+str(e)
        Log.log_s3(log_entry)
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
            
def md5_checksum(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            m.update(data)
   
    return m.hexdigest() 


def etag_checksum(filename, chunk_size=8 * 1024 * 1024):
    md5s = []
    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(chunk_size), b''):
            md5s.append(hashlib.md5(data).digest())
    m = hashlib.md5(b"".join(md5s))
    print('{}-{}'.format(m.hexdigest(), len(md5s)))
    return '{}-{}'.format(m.hexdigest(), len(md5s))

def etag_compare(filename, etag):
    et = etag[1:-1] # strip quotes
    #print('et',et)
    if '-' in et and et == etag_checksum(filename):
        return True
    if '-' not in et and et == md5_checksum(filename):
        return True
    return False     
#key='5414/generated_audios_to_upload/2021-03-09-02-14-50.wav'
#obj=pcr_storage.Object(key=key)

#client=boto3.client('s3')
#obj=client.head_object(Bucket='pcr-storage',Key=key)
#filename='D:/Patient-Caregiver-Relationship/Patient-Caregiver-Relationship/generated_data/generated_audios_to_upload/2021-03-09-02-14-50.wav'

def is_checksum_ok(file_name,key):
    try:
        obj = s3.Object(bucket_name='pcr-storage', key=key) 
        etag=obj.e_tag
        checksum_ok=etag_compare(file_name, etag)
        return checksum_ok
    except:
        Log.log_s3('exception obtaining etag from cloud ' + file_name)
        return -1

#put object into bucket
def upload_file(file_name,dir_name,is_progress=False):
    name=file_name.split('/')[-1]
    try:
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
        key=str(dep_id)+'/'+str(dir_name)+'/'+str(name)
        if(is_progress):
            res=pcr_storage.upload_file(Filename=file_name,Key=key,Callback=ProgressPercentage(file_name))
        else:
            res=pcr_storage.upload_file(Filename=file_name,Key=key)
        short_file=file_name.split('/')[-1]
        Log.log_s3('uploaded ' + dir_name+'/'+short_file)
        #compare checksums
        #print('checking checksum....')
        same=is_checksum_ok(file_name,key)
        if(not same):
            log_entry='checksum failed after uploading '+dir_name+'/'+short_file + ' in upload_file of s3_functions exception='+str(e)
            Log.log_s3(log_entry)
            #delete the file in cloud
            response = pcr_storage.delete_objects(Delete={'Objects': [{'Key': key}]})
            return -1
        else:
            Log.log_s3('checksum success ' + dir_name+'/'+short_file)
            return 0
    except Exception as e:
        print(str(e))
        short_file=file_name.split('/')[-1]
        log_entry='exception uploading '+dir_name+'/'+short_file + ' in upload_file of s3_functions exception='+str(e)
        Log.log_s3(log_entry)
        return -1

#check if a local and cloud file have the same md5
def are_files_same(cloud_file,local_file):
    #create temp file
    target_file=set_env.get_project_dir(-1)+'tmp.txt'
    download_file(target_file,cloud_file)
    cloud_md5=get_md5(target_file)
    local_md5=get_md5(local_file)
    return (cloud_md5==local_md5)

    

def download_file(target_file,cloud_file):
    try:
        pcr_storage.download_file(Key=cloud_file,Filename=target_file)
    except Exception as e:
        print(str(e))
        log_entry='in download_file of s3_functions exception='+str(e)
        Log.log_s3(log_entry)

def get_md5(file_name):
    with open(file_name) as f:
        data = f.read()    
        md5hash = hashlib.md5(data.encode('utf-8')).hexdigest()
    return md5hash
    
       
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