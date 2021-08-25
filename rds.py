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
        conn_cloud = pymysql.connect(host=endpoint, user=username,port=port,passwd=password, db=database_name)
        return conn_cloud
        if(not (type(conn_cloud) == pymysql.connections.Connection)):
            raise Exception("counld not obtain proper connection to RDS...")
    except Exception as e:
        print(e)
        return -1
    return conn_cloud

def connect_local():
    conn_local=-1
    try:
        conn_local=pymysql.connect(host='localhost',user='root',passwd='',db='ema')
        return conn_local
    except Exception as e:
        print(e)
        return -1
 #count the number of rows where column col_name = value
    def get_num_rows_with_value(self,table_name,col_name,value,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +"=\""+str(value)+"\" AND dep_id=\""+str(dep_id)+"\"")
            count=cursor.fetchall()[0][0]
            return count        
class RDS:
    def __init__(self):
        print('initializing RDS connection...')
        self.conn=connect_cloud()
        if(not isinstance(self.conn,pymysql.connections.Connection)):
            raise Exception('could not connect to RDS database')
        else:
            print('RDS connection established')
            
    def insert_row(self,table_name,col_names,values):
        with self.conn.cursor() as cursor:
            res=cursor.execute("INSERT INTO "+table_name+" (" + col_names + ") values (" + str(values) + ")")
            self.conn.commit()
            return res
   
    #get the last enrey of the table (in cloud) which came from this deployment
    def get_last_entry(self,table_name,dep_id):   
        with self.conn.cursor() as cursor:
            sqlquery="SELECT * FROM "+str(table_name)
            sqlquery="SELECT * FROM "+str(table_name)+" WHERE "+str(table_name)+".dep_id=\"" + str(dep_id) +  "\" AND ("+str(table_name)+".ts IS NOT NULL) ORDER BY -p_key LIMIT 1"
            cursor.execute(sqlquery)
            row=cursor.fetchall()
            return row
        
    def get_column_names(self,table_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SHOW COLUMNS from " + table_name)
            columns=cursor.fetchall()
            return columns   
     
    def get_all_rows(self,table_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM "+table_name)
            cols=cursor.fetchall() 
            return cols
    
    #get al the unisue values in a column
    def get_unique_row_list(self,table_name,col_name,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT "+str(col_name)+ " FROM "+table_name+" WHERE dep_id=\""+str(dep_id)+"\" ORDER BY -ts")
            ts=cursor.fetchall() 
            ts_list=[str(item[0]) for item in ts]
            return ts_list
        
    #count the number of rows where column col_name = value
    def get_num_rows_with_value(self,table_name,col_name,value,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +"=\""+str(value)+"\" AND dep_id=\""+str(dep_id)+"\"")
            count=cursor.fetchall()[0][0]
            return count
    
    #count the number of rows where column col_name > value
    def get_num_rows_greaterthan_value(self,table_name,col_name,value,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +">\""+str(value)+"\" AND dep_id=\""+str(dep_id)+"\"")
            count=cursor.fetchall()[0][0]
            return count
        
    #count all rows
    def get_num_rows(self,table_name,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE dep_id=\""+str(dep_id)+"\"")
            count=cursor.fetchall()[0][0]
            return count
        
    #get the rows where col_name=value
    def get_rows_with_value(self,table_name,col_name,value,dep_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM "+table_name+" WHERE "+col_name +"=\""+str(value)+"\" AND dep_id=\""+str(dep_id)+"\"")
            rows=cursor.fetchall()
            return rows
        
    def get_primary_key_name(self,table_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SHOW KEYS FROM " + table_name +" WHERE Key_name = 'PRIMARY'")
            res=cursor.fetchall()
            return res[0][4]
        
    #updatea column of a row with a given value. Identify column via primary key
    def set_column(self,table_name,primary_key_name,primary_key,col_name,value):
        with self.conn.cursor() as cursor:
            res=cursor.execute("UPDATE " + table_name +" SET "+str(col_name)+"="+str(value)+" WHERE "+primary_key_name+"=\""+str(primary_key)+"\"")
            self.conn.commit()
            return res
        

#local databse class inherits from cloud database class
class Local(RDS):
    def __init__(self):
        print('initializing local db connection...')
        self.conn=connect_local()
        if(not isinstance(self.conn,pymysql.connections.Connection)):
            raise Exception('could not connect to local database server')
        else:
            print('local database connection established')
            
    def get_num_rows_with_value(self,table_name,col_name,value):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +"=\""+str(value)+"\"")
            count=cursor.fetchall()[0][0]
            return count
        
    def get_unique_row_list(self,table_name,col_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT "+str(col_name)+ " FROM "+table_name)
            ts=cursor.fetchall() 
            ts_list=[str(item[0]) for item in ts]
            return ts_list
    
    #get the rows where col_name=value
    def get_rows_with_value(self,required_col,table_name,col_name,value):
        with self.conn.cursor() as cursor:
            if(required_col==-1):
                cursor.execute("SELECT * FROM "+table_name+" WHERE "+col_name +"=\""+str(value)+"\"")
            else:
                cursor.execute("SELECT "+str(required_col)+" FROM "+table_name+" WHERE "+str(col_name) +"=\""+str(value)+"\"")
            rows=cursor.fetchall()
            return rows
    #count the number of rows where column col_name > value
    def get_num_rows_greaterthan_value(self,table_name,col_name,value):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +">\""+str(value)+"\"")
            count=cursor.fetchall()[0][0]
            return count
     #count all rows
    def get_num_rows(self,table_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM "+table_name)
            count=cursor.fetchall()[0][0]
            return count
           