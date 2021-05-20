# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:58:53 2019

@author: M2FED_LAPTOP
"""

import pymysql
import set_env
import csv
import dep_data

'''************************************
*************************************
cloud database funcitons
**************************************
*************************************'''
def connect_cloud():
    global dep_id,conn_cloud,endpoint,port,database_name,username,password
    conn_cloud=-1
    try:
        dep_id=dep_data.get_dep_id(set_env.get_project_dir(-3))
        param_dict=set_env.get_parameters('RDS_credentials.txt')
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
        return 0
        if(not (type(conn_cloud) == pymysql.connections.Connection)):
            raise Exception("counld not obtain proper connection to RDS...")
    except Exception as e:
        print(e)
        return -1


'''************************************
*************************************
local database funcitons
**************************************
*************************************'''

def connect_local():
    global conn_local
    conn_local=-1
    try:
        conn_local=pymysql.connect('localhost','root','','ema')
    except Exception as e:
        print(e)
        
def set_local_updated(conn,table_name,primary_key_name,primary_key):
    cursor_local=conn.cursor()   
    cursor_local.execute("UPDATE " + table_name +" SET uploaded=1 WHERE "+primary_key_name+"=\""+primary_key+"\"")
    conn.commit()

    
    
def get_local_next_unuploaded_pkey(conn,table_name,pkey):
    p_key=-1
    try:
        conn.execute("SELECT " +pkey+ " FROM " + table_name +" WHERE uploaded=0 LIMIT 1")
        res=conn.fetchall() 
        p_key=res[0][0]
    except Exception as e:
        print(e)
    return p_key

def get_local_next_unuploaded_row(conn,table_name):
    try:
        conn.execute("SELECT * FROM " + table_name + " WHERE Uploaded=0 LIMIT 1")
        res=conn.fetchall() 
    except Exception as e:
        print(e)
    return res
        

'''************************************
*************************************
common database funcitons
**************************************
*************************************'''
def get_all_rows(cursor,table_name):
    cursor.execute("SELECT * FROM "+table_name)
    cols=cursor.fetchall() 
    return cols
    
def get_columns(cursor,table_name):
    cursor.execute("SHOW COLUMNS from " + table_name)
    columns=cursor.fetchall()
    return columns   

def get_local_all_tables(cursor):
    cursor.execute("SHOW TABLES")    
    tables = cursor.fetchall()
    return tables

def get_primary_key_name(cursor,table_name):
    cursor.execute("SHOW KEYS FROM " + table_name +" WHERE Key_name = 'PRIMARY'")
    res=cursor.fetchall()
    return res[0][4]

def get_row(cursor,table_name,primary_key):
    cursor.execute("SELECT * FROM " + table_name +" where ema_phones.phoneid = \""+primary_key+"\"")
    res=cursor.fetchall() 
    return res[0]  

#return column which has the given primary key
def get_row_col(cursor,table_name,primary_key_name,primary_key_value,col_name):
    cursor.execute("SELECT "+col_name+" FROM " + table_name +" where " + primary_key_name + " = \""+str(primary_key_value)+"\"")
    res=cursor.fetchall() 
    return res[0][0]

def get_row_num(cursor,table_name):
    cursor.execute("SELECT COUNT(*) FROM " + table_name)
    res=cursor.fetchall() 
    return res[0][0]

def add_uploaded_column(cursor,table_name):
    try:
        cursor.execute("ALTER TABLE " + table_name + " ADD COLUMN uploaded INT NOT NULL")
    except Exception as e:
        print(e)
    
def get_col_list_from_tuple(cols):
    col_names=[]
    for col_name in cols:
        col_names.append(col_name[0])
    return col_names

    
def insert_row_to_cloud(table_name,row):
    res=-1
    try:
        connect_local()
        with conn_local.cursor() as cursor:
            local_cols=get_columns(cursor,table_name)    
            local_cols=get_col_list_from_tuple(local_cols)
            local_cols=str(local_cols)[1:-1].replace("'", "")
            local_cols+=',dep_id'
        
            local_row=list(row)
            local_row_str=str([str(l) for l in local_row])[1:-1]
            local_row_str+=(',\''+dep_id+'\'')
            
        connect_cloud()
        with conn_cloud.cursor() as cursor:
            res=cursor.execute("INSERT INTO "+table_name+" (" + local_cols + ") values (" + local_row_str + ")")
            conn_cloud.commit()
    except Exception as e:
        print(e)
    finally:
        conn_cloud.close()
        conn_local.close()
        return res


def upload_all_rows(table_name):
    try:
        connect_local()
        connect_cloud()
        if((type(conn_local)==pymysql.connections.Connection) and(type(conn_cloud)==pymysql.connections.Connection)):
            cursor_local=conn_local.cursor() 
            rows=get_all_rows(cursor_local,table_name)
            conn_cloud.close()
            conn_local.close()
            print(len(rows))
            for row in rows:
                insert_row_to_cloud(table_name,row)
            print('done')
        else:
            print("couldn't connect to databases......:(")
    except Exception as e:
        print(e)
    
    
def get_unique_ts_list(cursor,table_name):
    #cursor.execute("SELECT DISTINCT ts FROM "+table_name+" WHERE dep_id=\""+str(dep_id)+"\" AND (ts IS NOT NULL) ORDER BY -ts LIMIT 1")
    cursor.execute("SELECT DISTINCT ts FROM "+table_name+" WHERE dep_id=\""+str(dep_id)+"\" ORDER BY -ts")
    ts=cursor.fetchall() 
    ts_list=[str(item[0]) for item in ts]
    return ts_list

def get_local_unique_ts_list(cursor,table_name):
    #cursor.execute("SELECT DISTINCT ts FROM "+table_name+" WHERE dep_id=\""+str(dep_id)+"\" AND (ts IS NOT NULL) ORDER BY -ts LIMIT 1")
    cursor.execute("SELECT DISTINCT ts FROM "+table_name+" ORDER BY -ts")
    ts=cursor.fetchall() 
    ts_list=[str(item[0]) for item in ts]
    return ts_list


def get_rows_with_value(cursor,table_name,col_name,value):
    cursor.execute("SELECT * FROM "+table_name+" WHERE "+col_name +"=\""+value+"\"")
    rows=cursor.fetchall()
    return rows

def get_num_rows_with_value(cursor,table_name,col_name,value):
    cursor.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+col_name +"=\""+value+"\"")
    count=cursor.fetchall()[0][0]
    return count


def delete_rows_with_value(connection,cursor,table_name,col_name,value):
    cursor.execute("DELETE FROM "+table_name+" WHERE "+col_name +"=\""+value+"\"")
    connection.commit()






'''************************************
*************************************
functionalities
**************************************
*************************************'''

#upload ema_phones and ema_recommendation. This is a one time job for each deployment
def upload_fixed_tables():
    upload_all_rows('ema_phones')

#upload all missing data for ema_data table
def upoload_missing_data_ts(table_name):
    connect_local()
    connect_cloud()
    if((type(conn_local)==pymysql.connections.Connection) and(type(conn_cloud)==pymysql.connections.Connection)):
        try:
            print('uploading data....')
            cursor_local=conn_local.cursor() 
            cursor_cloud=conn_cloud.cursor() 
            
            cloud_unique_ts_list=get_unique_ts_list(cursor_cloud,table_name)
            local_uniqie_ts_list=get_local_unique_ts_list(cursor_local,table_name)
            
            conn_cloud.close()
            conn_local.close()
            
            for ts in local_uniqie_ts_list:
                ts_upload=False
                if(ts in cloud_unique_ts_list):
                    connect_local()
                    connect_cloud()
                    cursor_local=conn_local.cursor() 
                    cursor_cloud=conn_cloud.cursor() 
                    
                    num_local=get_num_rows_with_value(cursor_local,table_name,'ts',ts)
                    num_cloud=get_num_rows_with_value(cursor_cloud,table_name,'ts',ts)
                    
                    conn_cloud.close()
                    conn_local.close()
                    
                    if(num_local>num_cloud):
                        ts_upload=True
                else:
                    ts_upload=True
                if(ts_upload):
                    print(ts)
                    #delete all rows with this ts
                    col_name='ts'
                    print(ts)
                    connect_local()
                    connect_cloud()
                    cursor_local=conn_local.cursor() 
                    cursor_cloud=conn_cloud.cursor() 
                    
                    delete_rows_with_value(conn_cloud,cursor_cloud,table_name,col_name,ts)
                    #upload all rows with this ts
                    rows=get_rows_with_value(cursor_local,table_name,col_name,ts) 
                    
                    conn_cloud.close()
                    conn_local.close()
                    
                    for i,row in enumerate(rows):
                        res=insert_row_to_cloud(table_name,row)
                        if(res==-1):
                            print('did not upload...')
                        if(i%100==0):
                            print(str(i) + " out of  " + str(len(rows)) + " is done")
               
            print('finished uploading data.')
        except Exception as e:
            print(e)
    else:
        print("couldn't connect to databses....... :(")
        
def upload_unuploaded_raws(table_name):
    connect_local()
    connect_cloud()
    cursor_local=conn_local.cursor() 
    cursor_cloud=conn_cloud.cursor()
    
    cloud_pkey_name=get_primary_key_name(cursor_cloud,table_name)
    cloud_columns=get_columns(cursor_cloud,table_name)
    local_columns=get_columns(cursor_local,table_name)
    local_columns=[item[0] for item in local_columns]
    local_pkey_name=get_primary_key_name(cursor_local,table_name)
    next_unuploaded_pkey=get_local_next_unuploaded_pkey(cursor_local,table_name,local_pkey_name)
    while(not(next_unuploaded_pkey==-1)):
        col_names="dep_id"
        val_list="\'"+str(dep_id)+"\',"
        for column in cloud_columns:
            if((column[0]==cloud_pkey_name) or (column[0]=='dep_id') or not(column[0] in local_columns)):
                continue
            col_names+=(','+column[0])
            val=get_row_col(cursor_local,table_name,local_pkey_name,next_unuploaded_pkey,column[0])
            val_list+="\'"+str(val)+"\',"
        val_list=val_list[:-1]
            
        cursor_cloud.execute("INSERT INTO "+table_name+" (" + col_names + ") values (" + val_list + ")")
        conn_cloud.commit()
        set_local_updated(conn_local,table_name,local_pkey_name,str(next_unuploaded_pkey))
        print('uploaded 1 row...')
        next_unuploaded_pkey=get_local_next_unuploaded_pkey(cursor_local,table_name,local_pkey_name)
        
    print("No (more) data to upload")
    cursor_local.close()
    cursor_cloud.close()
    




 

    


    




    
        

        