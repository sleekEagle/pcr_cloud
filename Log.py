# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:40:02 2020

@author: sleekEagle

This logs errors/other strings form the PCR_cloud code
"""
import os
import datetime 

def get_s3_log_path():
    s3_log_file=set_env.get_project_dir(-3)+'generated_data/cloud_logs/s3_log.txt'
    return s3_log_file

def get_rds_log_path():
    rds_log_file=set_env.get_project_dir(-3)+'generated_data/cloud_logs/rds_log.txt'
    return rds_log_file

def log_s3(entry,file_name):
    current_time = datetime.datetime.now()  
    s3_log_file=get_s3_log_path()
    os.makedirs(os.path.dirname(s3_log_file), exist_ok=True)
    with open(s3_log_file, "a") as file_object:
        log_entry=str(current_time)+','+entry+'\n'
        file_object.write(log_entry)
        

import set_env      