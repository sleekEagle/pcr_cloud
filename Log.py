# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:40:02 2020

@author: sleekEagle

This logs errors/other strings form the PCR_cloud code
"""
import os
import datetime 
import file_system_tasks
from datetime import date
import logging


def get_log_path():
    today = date.today()
    log_file=str(today)+'.log'
    log_dir=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/sys_logs/'
    log_path=log_dir+log_file
    return log_path

def reset_logger():
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
def set_logger(path):
    logging.basicConfig(filename=path, filemode='a', 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
def write_warning(message):
    logging.warning(message)

def write_error(message):
    logging.error(message)

def write_info(message):
    logging.info(message)


def get_s3_log_path():
    s3_log_file=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/s3_log.txt'
    return s3_log_file

def get_rds_log_path():
    rds_log_file=file_system_tasks.get_project_dir(-3)+'generated_data/cloud_logs/rds_log.txt'
    return rds_log_file

def log_s3(entry):
    current_time = datetime.datetime.now()  
    s3_log_file=get_s3_log_path()
    if not os.path.exists(s3_log_file):
        os.makedirs(os.path.dirname(s3_log_file))
    with open(s3_log_file, "a") as file_object:
        log_entry=str(current_time)+','+entry+'\n'
        file_object.write(log_entry)
        