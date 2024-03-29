# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:40:02 2020

@author: sleekEagle

This logs errors/other strings form the PCR_cloud code
"""
import file_system_tasks
import time
import os
import datetime

def get_log_path():
        now = datetime.datetime.now()
        log_dir=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/'
        log_file=log_dir+str(now.strftime("%Y-%m-%d"))+'.log'
        return log_file
    
def get_missing_data_log_path():
        now = datetime.datetime.now()
        log_dir=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/missing_data/'
        log_file=log_dir+str(now.strftime("%Y-%m-%d"))+'.log'
        return log_file
    
def write_log_entry(path,log_list,title):
    dir_name='/'.join(path.split('/')[0:-1])
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    with open(path, "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(title+'\n')
        file_object.write('date      ,num_local,num_cloud'+'\n')
        for item in log_list:
            file_object.write(str(item)[1:-1]+'\n')
        


