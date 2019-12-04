# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:58:53 2019

@author: M2FED_LAPTOP
"""

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


'''************************************
*************************************
local database funcitons
**************************************
*************************************'''

def connect_local():
    global con_local
    con_local=pymysql.connect('localhost','root','','ema')
    
def get_columns(cursor,table_name):
    cursor.execute("SHOW COLUMNS from " + table_name)
    columns=cursor.fetchall()
    return columns   

def get_local_all_tables():
    cursor_local.execute("SHOW TABLES")    
    tables = cursor_local.fetchall()
    return tables

def get_primary_key_name(cursor,table_name):
    cursor.execute("SHOW KEYS FROM " + table_name +" WHERE Key_name = 'PRIMARY'")
    res=cursor.fetchall()
    return res[0][4]

def get_local_row(table_name,primary_key):
    cursor_local.execute("SELECT * FROM " + table_name +" where ema_phones.phoneid = \""+primary_key+"\"")
    res=cursor_local.fetchall() 
    return res[0]  

col_name='port'
def get_row_col(cursor,table_name,primary_key,col_name):
    cursor.execute("SELECT "+col_name+" FROM " + table_name +" where ema_phones.phoneid = \""+primary_key+"\"")
    res=cursor.fetchall() 
    return res[0][0]

def get_local_row_num(table_name):
    cursor_local.execute("SELECT COUNT(*) FROM " + table_name)
    res=cursor_local.fetchall() 
    return res[0][0]

def local_add_uploaded_column(table_name):
    try:
        cursor_local.execute("ALTER TABLE " + table_name + " ADD COLUMN uploaded INT NOT NULL")
    except Exception as e:
        print(e)

def set_local_updated(cursor_local,table_name,primary_key_name,primary_key):
    cursor_local=con_local.cursor()   
    cursor_local.execute("UPDATE " + table_name +" SET uploaded=1 WHERE "+primary_key_name+"=\""+primary_key+"\"")
    con_local.commit()    

def get_local_next_unuploaded_pkey(cursor_local,table_name,pkey):
    p_key=-1
    try:
        cursor_local.execute("SELECT " +pkey+ " FROM " + table_name +" WHERE uploaded=0 LIMIT 1")
        res=cursor_local.fetchall() 
        p_key=res[0][0]
    except Exception as e:
        print(e)
    return p_key
    
def upload_unuploaded_raws(table_name):
    connect_local()
    connect_cloud()
    cursor_local=con_local.cursor() 
    cursor_cloud=conn_cloud.cursor()
    
    cloud_pkey_name=get_primary_key_name(cursor_cloud,table_name)
    cloud_columns=get_columns(cursor_cloud,table_name)
    local_pkey_name=get_primary_key_name(cursor_local,table_name)
    unuploaded_pkey=get_local_next_unuploaded_pkey(cursor_local,table_name,local_pkey_name)
    while(unuploaded_pkey>-1):
        col_names="dep_id"
        val_list="\'"+str(dep_id)+"\'"
        for column in cloud_columns:
            if((column[0]==cloud_pkey_name) or (column[0]=='dep_id')):
                continue
            col_names+=(','+column[0])
            val=get_row_col(cursor_local,table_name,unuploaded_pkey,column[0])
            val_list+=(",\'"+str(val)+"\'")
            
        cursor_cloud.execute("INSERT iNTO "+table_name+" (" + col_names + ") values (" + val_list + ")")
        conn_cloud.commit()
        set_local_updated(cursor_local,table_name,local_pkey_name,unuploaded_pkey)
        print('uploaded 1 row...')
        unuploaded_pkey=get_local_next_unuploaded_pkey(cursor_local,table_name,local_pkey_name)
    print("No (more) data to upload")
    cursor_local.close()
    cursor_cloud.close()

def upload_tables():
    upload_unuploaded_raws('ema_phones')

    




    
        

        