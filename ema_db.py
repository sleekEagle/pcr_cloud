# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:58:53 2019

@author: M2FED_LAPTOP
"""

import file_system_tasks
import dep_data


'''************************************
*************************************
local database funcitons
**************************************
*************************************'''
        
def set_local_updated(conn,table_name,primary_key_name,primary_key):
    cursor_local=conn.cursor()   
    cursor_local.execute("UPDATE " + table_name +" SET uploaded=1 WHERE "+primary_key_name+"=\""+primary_key+"\"")
    conn.commit()
    
    
def get_local_next_unuploaded_pkey(local_connection,table_name,pkey):
    p_key=-1
    try:
        res=local_connection.get_rows_with_value(pkey,table_name,'Uploaded','0')
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

def get_local_all_tables(cursor):
    cursor.execute("SHOW TABLES")    
    tables = cursor.fetchall()
    return tables


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

    
def insert_row_to_cloud(local_connection,rds_connection,table_name,row,dep_id):
    res=-1
    try:
        local_cols=local_connection.get_column_names(table_name)    
        local_cols=get_col_list_from_tuple(local_cols)
        local_cols=str(local_cols)[1:-1].replace("'", "")
        local_cols+=',dep_id'
    
        local_row=list(row)
        local_row_str=str([str(l) for l in local_row])[1:-1]
        local_row_str+=(',\''+str(dep_id)+'\'')
        
        res=rds_connection.insert_row(table_name,local_cols,local_row_str)
        
    except Exception as e:
        print(e)
    finally:
        return res


def upload_all_rows(local_connection,rds_connection,table_name):
    dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
    try:
        rows=local_connection.get_all_rows(table_name)
        for row in rows:
            insert_row_to_cloud(local_connection,rds_connection,table_name,row,dep_id)
        print('done')
        
    except Exception as e:
        print(e)
        return -1
    return 0
    
    


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
def upload_fixed_tables(local_connection,rds_connection):
    res=upload_all_rows(local_connection,rds_connection,'ema_phones')
    return res

#upload all missing data for ema_data table
def upoload_missing_data_ts(rds_connection,local_connection,table_name):
    try:
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
        start_date=dep_data.get_start_date()

        print('uploading data. '+table_name)
        
        cloud_unique_ts_list=rds_connection.get_unique_row_list(table_name,'ts',dep_id)
        local_uniqie_ts_list=local_connection.get_unique_row_list(table_name,'ts')
        local_uniqie_ts_list=[ts for ts in local_uniqie_ts_list if str(ts)[0:15]>start_date]    
        cloud_unique_ts_list.sort()
        if(len(cloud_unique_ts_list)>2):
            final_cloud_ts=cloud_unique_ts_list[-2]
            selected_local_unique_ts_list=[ts for ts in local_uniqie_ts_list if (ts>final_cloud_ts)]
        else:
            selected_local_unique_ts_list=local_uniqie_ts_list
        for ts in selected_local_unique_ts_list:
            print(ts)
            ts_upload=False
            if(ts in cloud_unique_ts_list):
                
                num_cloud=rds_connection.get_num_rows_with_value(table_name,'ts',ts,dep_id)
                num_local=local_connection.get_num_rows_with_value(table_name,'ts',ts)
                
                if(num_local>num_cloud):
                    ts_upload=True
            else:
                ts_upload=True
            if(ts_upload):
                #delete_rows_with_value(conn_cloud,cursor_cloud,table_name,col_name,ts)
                #upload all rows with this ts
                rows=local_connection.get_rows_with_value(-1,table_name,'ts',ts) 
                print('uploading '+str(len(rows))+' rows')
                for i,row in enumerate(rows):
                    res=insert_row_to_cloud(local_connection,rds_connection,table_name,row,dep_id)
                    if(res==-1):
                        print('did not upload...')
        print('finished uploading data.')
    except Exception as e:
        print(e)

        
def upload_unuploaded_rows(rds_connection,local_connection,table_name):
    dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
    cloud_pkey_name=rds_connection.get_primary_key_name(table_name)
    cloud_columns=rds_connection.get_column_names(table_name)
    local_columns=local_connection.get_column_names(table_name)
    local_columns=[item[0] for item in local_columns]
    local_pkey_name=local_connection.get_primary_key_name(table_name)
    next_unuploaded_pkey=get_local_next_unuploaded_pkey(local_connection,table_name,local_pkey_name)
    
    while(not(next_unuploaded_pkey==-1)):
        col_names="dep_id"
        val_list="\'"+str(dep_id)+"\',"
        for column in cloud_columns:
            if((column[0]==cloud_pkey_name) or (column[0]=='dep_id') or not(column[0] in local_columns)):
                continue
            col_names+=(','+column[0])
            val=local_connection.get_rows_with_value(column[0],table_name,local_pkey_name,next_unuploaded_pkey)
            val=val[0][0]
            val=str(val).replace("'","''")
            val_list+="\'"+val+"\',"
        val_list=val_list[:-1]
         
        res=rds_connection.insert_row(table_name,col_names,val_list)
        if(res==1):
            res=local_connection.set_column(table_name,local_pkey_name,next_unuploaded_pkey,'Uploaded','1')
        next_unuploaded_pkey=get_local_next_unuploaded_pkey(local_connection,table_name,local_pkey_name)
        
    print("No (more) data to upload")    

    
        

        