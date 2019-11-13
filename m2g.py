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




#read m2g fields paramenters from file
with open('/home/sleek_eagle/research/PCR_cloud/parameters.json', 'r') as f:
    param = json.load(f)[0]
columns = param['param']['m2g_fields']
column_list=columns.split(',')


#read the log file
path = '/home/sleek_eagle/research/PCR_cloud/data/2019-10-19_MonitorLog.txt'
f = open(path, 'r')
lines = f.readlines()
f.close()



host="pcr-database.c6cya7u6ocd9.us-east-2.rds.amazonaws.com"
port=3306
dbname="pcr_data"
user="admin"
password="poloBolo1234"



def get_sorted_file_names():
    path='/home/sleek_eagle/research/PCR_cloud/data/m2g_logs/'
    file_names = [f for f in listdir(path) if isfile(join(path, f))]
    file_names.sort(reverse=False)
    return file_names

def setup():
    set_env.read_param()
    host="pcr-database.c6cya7u6ocd9.us-east-2.rds.amazonaws.com"
    port=3306
    dbname="pcr_data"
    user="admin"
    password="poloBolo1234"
    global conn
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    global dep_id
    try:
        dep_id=set_env.get_env('dep_id')
    except:
        print('env var not found..')
        

#get the last enrey of the table which came from this deployment
def get_last_entry():   
    #query
    try:
        conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
        cursor=conn.cursor() 
        sqlquery="SELECT * FROM M2G WHERE M2G.dep_id=\"" + str(dep_id) +  "\" AND (M2G.ts IS NOT NULL) ORDER BY -p_key LIMIT 1"
        cursor.execute(sqlquery)
        row=cursor.fetchall()  
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()
        return row

line='2019-10-19 17:51:13.808000,laptop,discMemeory,True,[\'M2FED.Monitor@gmail.com\'],[DiscCheckThread] popo is OK.'
#add raw to table
def insert_raw(line):
    fields=line.split(',')
    values=''
    for i in range(len(fields)):
        fields[i]=fields[i].replace('\'','')
        #fields[i]=fields[i].replace('[','').replace(']','').replace('\'','')
        fields[i] = "\"" + fields[i] + "\""
        fields[i]
        values+=fields[i] + ","
    values=values[0:-1]
    query='insert into M2G (' + columns + ') values (' + values + ');'
    try:
        conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
        cursor=conn.cursor() 
        cursor.execute(query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()
        
#get log file name form db_date
def get_file_name_fromdb_date(db_date):
    last_db_date='2019-10-19 17:50:41.090000'
    date=last_db_date.split(' ')[0]
    name=date+"_MonitorLog.txt"
    return name


last_db_raw=get_last_entry()
last_db_ts=last_db_raw[0][2]
last_db_date=last_db_ts.split(' ')[0]
file_name=get_file_name_fromdb_date(last_db_date)

    
    
path = '/home/sleek_eagle/research/PCR_cloud/tmp.txt'
f = open(path, 'r')
lines = f.readlines()    
query=lines[0][0:-1]
cursorObject=conn.cursor() 
cursorObject.execute(query)

file_names=get_sorted_file_names()
for file in file_names:
    if(file < file_name):
        continue
    #do stuff


conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
cursor=conn.cursor() 
sqlquery="SELECT * FROM M2G WHERE (M2G.dep_id=\"" + str(dep_id) +  "\") AND (M2G.ts IS NOT NULL) ORDER BY -p_key LIMIT 100"
cursor.execute(sqlquery)
row=cursor.fetchall()  
row

conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
cursorObject=conn.cursor() 
sqlquery="""SELECT * FROM M2G WHERE (M2G.dep_id='boeoooo') AND (ts IS NOT NULL) ORDER BY -p_key LIMIT 100"""
sqlquery="SELECT * FROM pcr_data.M2G WHERE M2G.dep_id='boeoooo'"
cursorObject.execute(sqlquery)
row=cursor.fetchall()  
row

conn.commit()
cursorObject.close()
row=cursorObject.fetchall()  




