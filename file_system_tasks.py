#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:17:04 2019
@author: sleek_eagle
"""

import json
import home
import csv
import sys
import platform

'''
this code reads paramenters from parameters.json 
and adds them as environment variables.
Call this code once you change aby parameters from parameters.json
'''

def get_project_dir(level_up=-1):
    os=platform.system()
    current_dir=-1
    try:
        path=home.__file__
        if(os=='Linux'):
            l=path.split('/')
        elif(os=='Windows'):
            l=path.split('\\')
        else:
            raise Exception("current OS is unsupported!")
        current_dir='/'.join(l[:level_up])
        current_dir+='/'
    except:
        print('cannot read project dir in get_project_dir of file_system_tasks.py')
    return current_dir

#read parameters e.g. credentials from file and get this as a dictionary 
def get_parameters(parameter_file):
    ext=parameter_file.split('.')[1]
    param=-1
    project_home=get_project_dir(-4)
    parameter_path=project_home + parameter_file
    if(ext=='txt'):
        with open(parameter_path, "r") as f:
            dict_reader = csv.DictReader(f)
            param = list(dict_reader)[0]
    if(ext=='json'):    
        with open(parameter_path, 'r') as f:
            param = json.load(f)[0]
    return param
