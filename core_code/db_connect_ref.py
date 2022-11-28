import sqlite3
import time
import pandas as pd


def connect_db(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=1000.0 )
    except Exception as e:
        print("Cannot connect to database")
        print(e)

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

def get_refugee_dataframe(conn):
    # select from refugee table
    query = '''SELECT * FROM refugee'''
    pd_select = pd.read_sql_query(query,conn)
    df_refugee = pd.DataFrame(pd_select, columns=["refugeeID","campID","fName","lName","birthdate","gender","ethnicGroup","email","phone","familyMemberName","illness","surgery","smoking","alcoholic","request","status"])
    time.sleep(1.0)
    return df_refugee

def select_task_by_ref_id(conn,refugeeID):
    task_query = f'''SELECT * FROM task WHERE refugeeID = {refugeeID}'''
    pd_task = pd.read_sql_query(task_query,conn)
    df_task = pd.DataFrame(pd_task,columns=["taskID","refugeeID","volunteerID","taskInfo","startDate","workShift"])
    time.sleep(1.0)
    return df_task