#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:44:36 2019

@author: sleek_eagle
"""

import s3_functions as s3
import os
from os import walk
from os import listdir
from os.path import isfile, join
import set_env




def get_paths(items):
    paths=[]    
    for item in items:
        s=''
        for n in item:
            s+=n+'/'
        paths.append(s[0:-1])
    return paths

def get_s3_files():
    s3.get_bucket()
    dep_id=set_env.get_env('dep_id')
    all_objects = s3.list_items()  
    
    dep_items=[]
    for name in all_objects:
        ar=name.split('/')
        if(len(ar) > 2 and len(ar[-1]) > 0):    
            if(ar[0] == dep_id):
                dep_items.append(ar[1:])
    cloud_files=get_paths(dep_items)
    return cloud_files

def get_local_files():
    paths=set_env.get_env('s3_upload_dirs').split(',')
    file_list=[] 
    for path in paths:
        files = [(path + "/" + f) for f in listdir(path) if isfile(join(path, f))]
        file_list+=files
    return file_list

def list_diff(local_files, cloud_files): 
    upload_list=[]
    for local_file in local_files:
        ar=local_file.split('/')
        file_name = ar[-2] + "/" + ar[-1]
        if(not (file_name in cloud_files)):
            upload_list.append(local_file)
    return upload_list


def upload_file_not_in_cloud():
    s3.get_bucket()
    local_files=get_local_files()
    cloud_files=get_s3_files()
    not_uploaded=list_diff(local_files,cloud_files)
    for file in not_uploaded:
        print(file)
        dir_name=file.split('/')[-2]
        s3.upload_file(file,dir_name)
    






















