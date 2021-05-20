# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:11:22 2021

@author: Retriever
"""

import dep_data
import set_env
import time
import pymysql

table_name='heart_beat'    
col_names='dep_id,ts'

def insert_heart_beat(rds):
    if(not isinstance(rds.conn_cloud,pymysql.connections.Connection)):
        print('bad connection to RDS')
        return -1
        
    try:
        dep_id=dep_data.get_dep_id(set_env.get_project_dir(-3))
        ts=time.time()
        values=str(dep_id)+','+str(int(ts))
        res=rds.insert_row(table_name,col_names,values)   
    except:
        print('exception when inserting heart beat')
        return -1
    return res
    
