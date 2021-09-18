# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:40:02 2020

@author: sleekEagle

This logs errors/other strings form the PCR_cloud code
"""
import file_system_tasks
import time

def get_log_path():
        log_dir=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/'
        log_file=log_dir+str(time.strftime("%d-%m-%Y"))+'.log'
        return log_file

