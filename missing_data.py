# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:15:27 2020

@author: sleek_eagle
"""

'''
this code compares the files in local with those in the cloud
then it creates a report on what's in cloud and whats not
'''

import dep_data
import file_system_tasks
import s3_upload
import os
import time
import datetime
import m2g

def insert_missing_data(rds_connection,local_connection,table_name,missing_table_name):
    res=-1
    try:
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))   
        cloud_count=rds_connection.get_num_rows(table_name,dep_id)
        local_count=local_connection.get_num_rows(table_name)
        col_names='dep_id,ts,local_count,cloud_count'
        ts=str(datetime.datetime.fromtimestamp(time.time()))
        values="\'"+str(dep_id)+"\'," +"\'"+ str(ts)+"\'," + "\'"+str(local_count)+"\',"+"\'"+str(cloud_count)+"\'"
        res=rds_connection.insert_row(missing_table_name,col_names,values) 
    except:
        print('Exception in insert_missing_data')
    return res

def insert_missing_M2G(rds_connection):
    res=-1
    try:
        file_names=m2g.get_sorted_file_names()
        local_count=0
        if(isinstance(file_names,list)):
            for file in file_names:
                lines=m2g.read_file(file)
                local_count+=len(lines)
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))   
        cloud_count=rds_connection.get_num_rows('M2G',dep_id)
        col_names='dep_id,ts,local_count,cloud_count'
        ts=str(datetime.datetime.fromtimestamp(time.time()))
        values="\'"+str(dep_id)+"\'," +"\'"+ str(ts)+"\'," + "\'"+str(local_count)+"\',"+"\'"+str(cloud_count)+"\'"
        res=rds_connection.insert_row('missing_M2G',col_names,values) 
    except:
        print('Exception in insert_missing_M2G')
    return res
        
        
def insert_missing_files_row(rds_connection):
    res=-1
    try:
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
        local_files=s3_upload.get_local_files()
        cloud_files=s3_upload.get_s3_files()
        missing_files=s3_upload.list_diff(local_files,cloud_files)
        col_names='dep_id,ts,local_count,cloud_count,missing'
        ts=str(datetime.datetime.fromtimestamp(time.time()))
        values="\'"+str(dep_id)+"\'," +"\'"+ str(ts)+"\'," + "\'"+str(len(local_files))+"\',"+"\'"+str(len(cloud_files))+"\',"+"\'"+str(len(missing_files))+"\'"
        res=rds_connection.insert_row('missing_files',col_names,values)
    except:
        print('exception when inserting to missing_files')
    return res


#report file 

def create_report_file():
    report_file=file_system_tasks.get_project_dir(-3)+'generated_data/report.txt'
    local_files=s3_upload.get_local_files()
    cloud_files=s3_upload.get_s3_files()
    
    report=[]
    for file in local_files:
        splt=file.split('/')[-2:]
        local_file=splt[0]+'/'+splt[1]
        in_cloud=local_file in cloud_files
        report.append(local_file+' - ' + str(in_cloud))
    
    #remove the file
    if(os.path.exists(report_file)):
        os.remove(report_file)
    #write new data to file     
    with open(report_file, 'w') as f:
        for item in report:
            f.write("%s\n" % item)
