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

'''
this code reads paramenters from parameters.json 
and adds them as environment variables.
Call this code once you change aby parameters from parameters.json
'''

#find the parameter.json file by searching in the parent directory
def find_parameter_file():
    current_dir=os.getcwd() 
    for dirpath,_,filenames in os.walk(current_dir):
        for f in filenames:
            full_path= os.path.abspath(os.path.join(dirpath, f))
            if("parameters.json" in full_path):
                return full_path
    return -1
           
#read paramenters from file
def read_param():
    json_file=find_parameter_file()
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
    else:
        raise Exception("cannot find a parameters.json file in the parent directory...")
        
        
def get_env(name):
    return os.environ[name]
    

