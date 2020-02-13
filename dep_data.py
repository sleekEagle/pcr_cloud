# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:51:49 2020

@author: M2FED_LAPTOP
"""
import sqlite3
import pymysql
import set_env

'''************************************
*************************************
cloud database funcitons
**************************************
*************************************'''
def connect_cloud():
    set_env.read_param()
    global dep_id,conn_cloud,host,port,dbname,user,password,dep_id,columns
    conn_cloud=-1
    try:
        host=set_env.get_env('rds_host')
        port=int(set_env.get_env('rds_port'))
        dbname=set_env.get_env('rds_db_name')
        user=set_env.get_env('rds_user')
        password=set_env.get_env('rds_password')
        dep_id=set_env.get_env('dep_id')
    except Exception as e:
        print(e)
    try:
        conn_cloud = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
        if(not (type(conn_cloud) == pymysql.connections.Connection)):
            raise Exception("counld not obtain propoer connection to RDS...")
    except Exception as e:
        print(e)

#cloud operations

        

 
def get_table_names(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    return cursorObj.fetchall()

def get_local_columns(con,table_name):
    cursorObj = con.cursor()
    cursorObj.execute("PRAGMA table_info(DEPLOYMENT_DATA)")
    columns=cursorObj.fetchall()
    return columns

def get_cloud_columns(con,table_name):
    cursor = con.cursor()
    cursor.execute("SHOW COLUMNS from " + table_name)
    columns=cursor.fetchall()
    return columns   
 
def get_all_rows(cursor,table_name):
    cursor.execute("SELECT * FROM "+table_name)
    cols=cursor.fetchall() 
    return cols

def upload_dep_data_table():
    table_name='DEPLOYMENT_DATA'
    connect_cloud()
    project_path=set_env.get_project_dir(-3)[:-1]
    con = sqlite3.connect(project_path+"/"+'/DeploymentInformation.db')
    cursor_cloud = conn_cloud.cursor()
    
    cursorObj = con.cursor()
    rows=get_all_rows(cursorObj,"DEPLOYMENT_DATA")
    local_cols=get_local_columns(con,"DEPLOYMENT_DATA")
    local_cols=[str(col[1]) for col in local_cols]
    
    cloud_cols=get_cloud_columns(conn_cloud,"DEPLOYMENT_DATA")
    cloud_cols=[col[0] for col in cloud_cols]
    
    cursorObj.execute('SELECT * from  DEPLOYMENT_DATA')
    rows=cursorObj.fetchall()
    
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
        cursor_cloud.execute("INSERT INTO "+table_name+" (" + str_cols + ") values (" + str_row + ")")
        conn_cloud.commit()
    cursor_cloud.close()
    
 
def get_dep_id(project_dir):
    dep_id=-1
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
    return dep_id




