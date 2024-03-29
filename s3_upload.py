#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:44:36 2019

@author: sleek_eagle
"""

import s3_functions as s3
from os import listdir
from os.path import isfile, join
import file_system_tasks
import Log
import dep_data
import subprocess
import logging
from importlib import reload
reload(logging)

logging.basicConfig(level = logging.ERROR, 
                    filename =Log.get_log_path(),
                    format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')

#guide on how to trasfer files to s3 with aws cli
#C:\Users\Meerkat\Desktop\Patient-Caregiver-Relationship\Patient-Caregiver-Relationship\generated_data\audio_storage\generated_speaker_id

def aws_sync(dir_path,dep_id):
    dir_name=dir_path.split('\\')[-1]
    res=subprocess.run(["aws","s3","sync",dir_path,"s3://pcr-storage/"+str(dep_id)+"/"+str(dir_name)+"/"],
                        capture_output=True)
    return res
def upload_files():
    try:
        paths=file_system_tasks.get_parameters('parameters.json')['param']['s3_upload_dirs'].split(',')
        project_dir=file_system_tasks.get_project_dir(-3)[:-1]
        paths=[project_dir+path for path in paths]
        paths=[path.replace('/','\\') for path in paths]
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
    except Exception as e:
        print('Exception in reading files...' + str(e))
        logging.error('setting up the upload')
        
    
    for path in paths:
        print('uploading '+str(path))
        try:
            res=aws_sync(path,dep_id)
            if(res.returncode!=0):
                print('Exception in uploading data')
                logging.error('uploading data with AWS CLI')
        except:
            print('Exception in uploading data')
            logging.error('invoking AWS cli')
            


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
    dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
    all_objects = s3.list_items()  
    
    dep_items=[]
    for name in all_objects:
        ar=name.split('/')
        if(len(ar) > 2 and len(ar[-1]) > 0):    
            if(str(ar[0]) == str(dep_id)):
                dep_items.append(ar[1:])
    cloud_files=get_paths(dep_items)
    return cloud_files

def get_local_files():
    paths=file_system_tasks.get_parameters('parameters.json')['param']['s3_upload_dirs'].split(',')
    project_dir=file_system_tasks.get_project_dir(-3)[:-1]
    paths=[project_dir+path for path in paths]
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

#let dir_name=-1 to count all items belonging to a deployment
def count_cloud_items(dep_id,dir_name):
    s3.get_bucket()
    b=s3.pcr_storage
    if(dir_name==-1):
        objects = b.objects.filter(Prefix=dep_id+'/')
    else:
        objects = b.objects.filter(Prefix=dep_id+'/'+dir_name)
    count=0
    for o in objects:
        count+=1
    return count

def upload_file_not_in_cloud():
    not_uploaded=-1
    s3.get_bucket()
    b=s3.pcr_storage
    if (b.name=='pcr-storage'):
        Log.log_s3('bucket resource found')
        Log.log_s3('Checking for files to upload (file-wise status will be printed below).....')
        local_files=get_local_files()
        cloud_files=get_s3_files()
        not_uploaded=list_diff(local_files,cloud_files)
        for file in not_uploaded:
            print(file)
            dir_name=file.split('/')[-2]
            file_name=file.split('/')[-1]
            #print('Uploading '+file_name)
            s3.upload_file(file,dir_name)
            #print('uploaded')
    else:
        Log.log_s3('bucket resource not found')
    return not_uploaded








