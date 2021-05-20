# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:51:49 2020

@author: M2FED_LAPTOP
"""
import sqlite3
import os
import s3_functions as s3
from zipfile import ZipFile 
import file_system_tasks
import datetime
        
def get_table_names(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    return cursorObj.fetchall()

def get_local_columns(con,table_name):
    cursorObj = con.cursor()
    cursorObj.execute("PRAGMA table_info(DEPLOYMENT_DATA)")
    columns=cursorObj.fetchall()
    return columns

def upload_dep_data_table(rds_connection):
    project_path=file_system_tasks.get_project_dir(-3)[:-1]
    try:
        local_con = sqlite3.connect(project_path+"/"+'/DeploymentInformation.db')
    except:
        print('cannot connect to local DB')
        return -1
    try:
        rows=rds_connection.get_all_rows("DEPLOYMENT_DATA")
        local_cols=get_local_columns(local_con,"DEPLOYMENT_DATA")
        local_cols=[str(col[1]) for col in local_cols]
        
        cloud_cols=rds_connection.get_column_names("DEPLOYMENT_DATA")
        cloud_cols=[col[0] for col in cloud_cols]
        
        cursorObj = local_con.cursor()
        cursorObj.execute('SELECT * from  DEPLOYMENT_DATA')
        rows=cursorObj.fetchall()
    except:
        print('Error when reading from databases. upload_dep_data_table() in dep_data.py')
        return -1
    
    str_cols=""
    for i,col in enumerate(local_cols):
        if(col in cloud_cols):
            str_cols+=(col+",")
    str_cols=str_cols[:-1]
    
    for row in rows:
        str_row=""
        for i,item in enumerate(row):
            if(local_cols[i] in cloud_cols):
                str_row+=("\'"+str(item)+"\',")
        str_row=str_row[:-1]
        res=rds_connection.insert_row('DEPLOYMENT_DATA',str_cols,str_row)
        if(res!=1):
            print('error inserting row')
    
 
def get_dep_id(project_dir):
    dep_id=str(datetime.datetime.now())
    try:
        con = sqlite3.connect(project_dir+"/"+'/DeploymentInformation.db')
        cursorObj = con.cursor()
        
        table_name='DEPLOYMENT_DATA'
        cursorObj.execute("SELECT * FROM "+table_name+" WHERE STATUS='Running' ORDER BY START_TIME DESC")
        rows=cursorObj.fetchall()
        last_dep_row=rows[0]
        dep_id=int(last_dep_row[0])
    except Exception as e:
        print(e)
        print("Could not read deployment ID from DeploymentInformation.db")
    return dep_id

 
def get_start_time(project_dir):
    try:
        con = sqlite3.connect(project_dir+"/"+'/DeploymentInformation.db')
        cursorObj = con.cursor()
        
        table_name='DEPLOYMENT_DATA'
        cursorObj.execute("SELECT * FROM "+table_name+" WHERE STATUS='Running' ORDER BY START_TIME DESC")
        rows=cursorObj.fetchall()
        last_dep_row=rows[0]
        start_time=int(last_dep_row[5])
    except Exception as e:
        print(e)
        print("Could not read deployment ID from DeploymentInformation.db")
    return start_time

def get_start_date():
    start_date=-1
    try:
        project_dir=file_system_tasks.get_project_dir(-3)
        start_time=get_start_time(project_dir)/1000.0
        start_date=datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d')
    except:
        print('exception when getting start date')
    return start_date


def get_all_file_paths(directory): 
    # initializing empty file paths list 
    file_paths = [] 
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath)
    # returning all file paths 
    return file_paths    

def upload_zip_file():
    project_dir=file_system_tasks.get_project_dir(level_up=-4)
    parent_dir=file_system_tasks.get_project_dir(level_up=-5)
    out_file=parent_dir+project_dir.split('/')[-2]+".zip"
    print("creating .zip file....")
    
    file_paths = get_all_file_paths(project_dir) 
    # writing files to a zipfile 
    with ZipFile(out_file,'w',allowZip64 = True) as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(file)
    
    #shutil.make_archive(out_file, 'zip', project_dir,verbose=True)
    print("done")
    s3.get_bucket()
    print("uploading .zip file to cloud")
    s3.upload_file(out_file,"project_dir",is_progress=True)
    print("done")