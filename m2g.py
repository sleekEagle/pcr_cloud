#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:52:22 2019

@author: sleek_eagle
"""
import json
import os
import set_env
from os import listdir
from os.path import isfile, join
import pymysql
import re

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
        columns=set_env.get_env('m2g_fields')
    except Exception as e:
        print(e)
    try:
        conn_cloud = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
        if(not (type(conn_cloud) == pymysql.connections.Connection)):
            raise Exception("counld not obtain propoer connection to RDS...")
    except Exception as e:
        print(e)


#read the log file
def read_file(f):
    set_env.read_param()
    try:
        path=set_env.get_project_dir(-3)+set_env.get_env('m2g_log_dir')+'/'

    except Exception as e:
        print(e)
    
    f = open(path+f, 'r')
    lines = f.readlines()
    f.close()
    return lines

def get_sorted_file_names():
    set_env.read_param()
    try:
        root_dir=set_env.get_project_dir(-3)
        path=root_dir+set_env.get_env('m2g_log_dir')
    except Exception as e:
        print(e)
    try:
        file_names = [f for f in listdir(path) if isfile(join(path, f))]
        file_names.sort(reverse=False)
    except Exception as e:
        print(e)
        return -1
    return file_names


#get the last enrey of the table which came from this deployment
def get_last_entry():   
    #query
    try:
        connect_cloud()
        cursor=conn_cloud.cursor() 
        sqlquery="SELECT * FROM M2G"
        sqlquery="SELECT * FROM M2G WHERE M2G.dep_id=\"" + str(dep_id) +  "\" AND (M2G.ts IS NOT NULL) ORDER BY -p_key LIMIT 1"
        cursor.execute(sqlquery)
        row=cursor.fetchall()  
    except Exception as e:
        print(e)
    finally:
        conn_cloud.commit()
        conn_cloud.close()
        return row

#line='2019-10-19 17:51:13.808000,laptop,discMemeory,True,[\'M2FED.Monitor@gmail.com\'],[DiscCheckThread] popo is OK.'
#add raw to table
def insert_raw(line):
    connect_cloud()
    fields=line.split(',')
    values=''
    for i in range(len(fields)):
        fields[i]=fields[i].replace('\'','')
        #fields[i]=fields[i].replace('[','').replace(']','').replace('\'','')
        fields[i] = "\"" + fields[i] + "\""
        fields[i]
        values+=fields[i] + ","
    values=values[0:-1]
    values+="," + "\"" + dep_id + "\""
    query='insert into M2G (' + columns + ') values (' + values + ');'
    res=-1
    try:
        cursor=conn_cloud.cursor() 
        res=cursor.execute(query)
    except Exception as e:
        print(e)
    finally:
        conn_cloud.commit()
        conn_cloud.close()
        return res
        
#get log file name form db_date
def get_file_name_fromdb_date(db_ts):
    date=db_ts.split(' ')[0]
    name=date+"_MonitorLog.txt"
    return name

def get_ts(line):
    return line.split(',')[0]

def upload_missing_entries():
    file_names=get_sorted_file_names()
    last_db_raw=get_last_entry()
    last_db_ts="-1"
    file_name=file_names[0]
    if(len(last_db_raw) > 0):
        last_db_ts=last_db_raw[0][2]
        file_name=get_file_name_fromdb_date(last_db_ts)
    for f in file_names:
        if(f<file_name):
            continue
        lines=read_file(f)
        print(lines[0])
        for line in lines:
            ts=get_ts(line)
            print(ts)
            if(ts > last_db_ts):
                res=insert_raw(line)
                print(res)






