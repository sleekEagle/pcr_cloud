#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:52:22 2019

@author: sleek_eagle
"""
import file_system_tasks
from os import listdir
from os.path import isfile, join
import dep_data
import datetime


dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
col_names=file_system_tasks.get_parameters('parameters.json')['param']['m2g_fields']

#read the log file
def read_file(f):
    try:
        root_dir=file_system_tasks.get_project_dir(-3)
        path=root_dir[0:-1]+file_system_tasks.get_parameters('parameters.json')['param']['m2g_log_dir']+'/'
    except Exception as e:
        print(e)
    with open(path+f, 'r') as file:
        lines = file.readlines()
    return lines


def get_sorted_file_names():
    try:
        root_dir=file_system_tasks.get_project_dir(-3)
        path=root_dir[0:-1]+file_system_tasks.get_parameters('parameters.json')['param']['m2g_log_dir']
    except Exception as e:
        print(e)
    try:
        file_names = [f for f in listdir(path) if isfile(join(path, f))]
        file_names.sort(reverse=False)
    except Exception as e:
        print(e)
        return -1
    return file_names


def insert_row(rds_connection,col_names,dep_id,line):
    values=line.rstrip("\n").replace("'","")+','+str(dep_id)
    varlist=values.split(',')
    s=""
    for v in varlist:
        s+="'"+str(v)+"'"+','
    s=s[0:-1]
    res=rds_connection.insert_row('M2G',col_names,s)
    return res

def get_ts(line):
    return line.split(',')[0]


def upload_missing_entries(rds_connection):
    file_names=get_sorted_file_names()
    dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
    if(isinstance(file_names,list) and len(file_names)>0):
        last_db_raw=rds_connection.get_last_entry('M2G',dep_id)
        last_db_ts=last_db_raw[0][1]
        last_db_date=str(last_db_ts)[0:10]
        
        if(isinstance(last_db_raw,tuple)):
            start_date=dep_data.get_start_date()
            max_date=max(start_date,last_db_date)
            #select file names which were created after the start date of deployment
            file_names=[f for f in file_names if f[0:10]>=max_date]
            if(len(last_db_raw) > 0):
                last_uploaded_file=str(last_db_ts)[0:10]+"_MonitorLog.txt"
            for f in file_names:
                if(f<last_uploaded_file):
                    continue
                lines=read_file(f)
                if(isinstance(lines,list)):
                    for line in lines:
                        ts=get_ts(line)
                        if(ts > str(last_db_ts)):
                            try:
                                res=insert_row(rds_connection,col_names,dep_id,line)
                            except:
                                print('exception when inserting row')
                