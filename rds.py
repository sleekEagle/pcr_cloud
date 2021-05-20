# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:21:16 2021

@author: Retriever
"""

import pymysql
import file_system_tasks

def connect_cloud():
    conn_cloud=-1
    try:
        param_dict=file_system_tasks.get_parameters('RDS_credentials.txt')
        endpoint=param_dict['endpoint']
        port=int(param_dict['port'])
        database_name=param_dict['database_name']
        username=param_dict['username']
        password=param_dict['password']            
    except Exception as e:
        print(e)
        return -1
    try:
        conn_cloud = pymysql.connect(endpoint, user=username,port=port,passwd=password, db=database_name)
        return conn_cloud
        if(not (type(conn_cloud) == pymysql.connections.Connection)):
            raise Exception("counld not obtain proper connection to RDS...")
    except Exception as e:
        print(e)
        return -1
    return conn_cloud
    
class RDS:
    def __init__(self):
        print('initializing RDS connection...')
        self.conn_cloud=connect_cloud()
        if(not isinstance(self.conn_cloud,pymysql.connections.Connection)):
            raise Exception('could not connect to RDS database')
        else:
            print('RDS connection established')
            
    def insert_row(self,table_name,col_names,values):
        with self.conn_cloud.cursor() as cursor:
            res=cursor.execute("INSERT INTO "+table_name+" (" + col_names + ") values (" + values + ")")
            self.conn_cloud.commit()
            return res
   
    #get the last enrey of the table (in cloud) which came from this deployment
    def get_last_entry(self,table_name,dep_id):   
        with self.conn_cloud.cursor() as cursor:
            sqlquery="SELECT * FROM "+str(table_name)
            sqlquery="SELECT * FROM "+str(table_name)+" WHERE "+str(table_name)+".dep_id=\"" + str(dep_id) +  "\" AND ("+str(table_name)+".ts IS NOT NULL) ORDER BY -p_key LIMIT 1"
            cursor.execute(sqlquery)
            row=cursor.fetchall()
            return row
        
    def get_column_names(self,table_name):
        with self.conn_cloud.cursor() as cursor:
            cursor.execute("SHOW COLUMNS from " + table_name)
            columns=cursor.fetchall()
            return columns   
     
    def get_all_rows(self,table_name):
        with self.conn_cloud.cursor() as cursor:
            cursor.execute("SELECT * FROM "+table_name)
            cols=cursor.fetchall() 
            return cols
           
