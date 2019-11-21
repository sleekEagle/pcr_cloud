#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:17:04 2019

@author: sleek_eagle
"""

import json
import os

'''
this code reads paramenters from parameters.json 
and adds them as environment variables.
Call this code once you change aby parameters from parameters.json
'''
#read paramenters from file
def read_param():
    with open('../parameters.json', 'r') as f:
        param = json.load(f)[0]
    env_vars = param['env_var']
    #write parameters to environment variables
    
    for key,value in env_vars.items():
        os.environ[key]=str(value)
        
def get_env(name):
    return os.environ[name]
    

    

    
    
