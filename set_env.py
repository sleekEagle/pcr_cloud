#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:17:04 2019

@author: sleek_eagle
"""

import json
import os
from os import listdir
from os.path import isfile, join
import dep_data
import csv

'''
this code reads paramenters from parameters.json 
and adds them as environment variables.
Call this code once you change aby parameters from parameters.json
'''

def get_project_dir(level_up=-1):
    path=dep_data.__file__
    l=path.split('\\')
    current_dir='/'.join(l[:level_up])
    current_dir+='/'
    return current_dir

def get_credentials():
    try:
        paroject_home=get_project_dir(-4)
        credential_file=paroject_home+'credentials.txt'
        a_csv_file = open(credential_file, "r")
        dict_reader = csv.DictReader(a_csv_file)
        ordered_dict_from_csv = list(dict_reader)[0]
        dict_from_csv = dict(ordered_dict_from_csv)
        id=dict_from_csv['Access key ID']
        secret=dict_from_csv['Secret access key']
    except:
        print('Cannot read creadentials file.')
    return id,secret


#find the parameter.json file by searching in the parent directory
def find_parameter_file():
    current_dir=get_project_dir()
    for dirpath,_,filenames in os.walk(current_dir):
        for f in filenames:
            full_path= os.path.abspath(os.path.join(dirpath, f))
            if("parameters.json" in full_path):
                return full_path
    return -1
           
#read paramenters from file
def read_param():
    json_file=find_parameter_file()
    is_read_ok=True
    if(type(json_file)==str):
        try:
            with open(json_file, 'r') as f:
                param = json.load(f)[0]
            env_vars = param['env_var']
            #write parameters to environment variables
            for key,value in env_vars.items():
                os.environ[key]=str(value)
        except Exception as e:
            print(e)
            print("Exception when reading parameters file")
            is_read_ok=False
    else:
        is_read_ok=False
        raise Exception("cannot find a parameters.json file in the parent directory...")
    #set dep_id environ variable
    dep_id=dep_data.get_dep_id(get_project_dir(-3))
    os.environ['dep_id']=str(dep_id)
    
    #read creadentials
    try:
        id,secret=get_credentials()
        os.environ['aws_access_key_id']=id
        os.environ['aws_secret_access_key']=secret
    except:
        is_read_ok=False
        print('exception when reading creadentials')
    return is_read_ok
        
        
        
def get_env(name):
    return os.environ[name]


def set_var(key,value):
    try:
        os.environ[key]=str(value)
        return 0
    except Exception as e:
        print(e)
        return -1
    

