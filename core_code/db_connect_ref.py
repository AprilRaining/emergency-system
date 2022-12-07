import sqlite3
import time
import pandas as pd
from system_log import *


def connect_db():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("info_files/emergency_system.db", timeout=1000.0)
    except Exception as e:
        print_log(str(e))

    return conn


def insert_refdb_row(conn, refugee_row):
    query = ''' INSERT INTO refugee(campID,fName,lName,birthdate,gender,ethnicGroup,email,phone,familyMemberName,illness,surgery,smoking,alcoholic,request,status)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(query, refugee_row)
    conn.commit()
    time.sleep(8.0)
    cur.close()
    return cur.lastrowid


def update_refdb_attr(conn, refugeeID, attr, refugee_attr):
    # update item in row one at a time
    # print(refugee_attr,attr)
    cur = conn.cursor()
    query = f''' UPDATE refugee
                SET "{attr}" = "{refugee_attr}" 
                WHERE refugeeID = {refugeeID} '''
    cur.execute(query)
    conn.commit()
    time.sleep(2.0)
    cur.close()

def delete_ref_by_id(conn,refugeeID):
    del_query = f'''DELETE FROM refugee WHERE refugeeID = {refugeeID}'''
    cur = conn.cursor()
    cur.execute(del_query)
    conn.commit()
    cur.close()

def clear_request_schedule(conn,df_task_by_ref):
    # in case there're many request
    task_ID_arr = df_task_by_ref["taskID"].tolist()
    for tid in task_ID_arr:
        date = pd.Timestamp(
        str(df_task_by_ref.loc[df_task_by_ref["taskID"] == tid, "startDate"].values[0]))
        dn = date.day_name()
        # set volunteer related to refugee schedule to 0
        vol_id = df_task_by_ref.loc[df_task_by_ref["taskID"]== tid, "volunteerID"].values[0]
        vol_upd1 = f'''UPDATE volunteer SET {dn} = 0 WHERE volunteerID = {vol_id}'''
        cur = conn.cursor()
        cur.execute(vol_upd1)
        conn.commit()
        time.sleep(4.0)


def get_refugee_dataframe(conn):
    # select from refugee table
    query = '''SELECT * FROM refugee'''
    pd_select = pd.read_sql_query(query,conn)
    df_refugee = pd.DataFrame(pd_select, columns=["refugeeID","campID","fName","lName","birthdate","gender","ethnicGroup","email","phone","familyMemberName","illness","surgery","smoking","alcoholic","request","status"])
    time.sleep(1.0)
    return df_refugee

def select_task_by_ref_id(conn,refugeeID):
    task_query = f'''SELECT * FROM task WHERE refugeeID = {refugeeID} and status = "active"'''
    pd_task = pd.read_sql_query(task_query,conn)
    df_task_ref_id = pd.DataFrame(pd_task,columns=["taskID","refugeeID","volunteerID","taskInfo","week","startDate","workShift","status"])
    time.sleep(1.0)
    return df_task_ref_id