import sqlite3
import time
import pandas as pd
from system_log import *
import json


def connect_db():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("emergency_system.db", timeout=1000.0)
    except Exception as e:
        print_log(str(e))

    return conn


def insert_refdb_row(conn, refugee_row):
    query = ''' INSERT INTO refugee(campID,fName,lName,birthdate,gender,ethnicGroup,email,phone,familyMemberName,illness,surgery,smoking,alcoholic,request,status)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(query, refugee_row)
    conn.commit()
    time.sleep(1.2)
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
    time.sleep(1.3)
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
        str(df_task_by_ref.loc[df_task_by_ref["taskID"] == tid, "requestDate"].values[0]))
        dn = date.day_name()
        # set volunteer related to refugee schedule to 0
        cur = conn.cursor()
        vol_id = df_task_by_ref.loc[df_task_by_ref["taskID"]== tid, "volunteerID"].values[0]
        vol_upd1 = f'''UPDATE volunteer SET {dn} = 0 WHERE volunteerID = {vol_id}'''
        cur.execute(vol_upd1)
        conn.commit()
        time.sleep(0.8)          
        # set task to inactive
        task_upd = f'''UPDATE task SET status = "inactive" WHERE volunteerID = {vol_id}'''
        cur.execute(task_upd)
        conn.commit()
        time.sleep(0.8)

# def clear_vol_ref_schedule(conn,vol_ID):
#     clear_query = f'''SELECT task.refugeeID,task.taskID,task.volunteerID,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer JOIN task ON volunteer.volunteerID = task.volunteerID WHERE volunteer.volunteerID={vol_ID}'''
#     clear_pd = pd.read_sql_query(clear_query,conn)
#     # to be used to clear refugee req: only ref related to this volunteer
#     clear_ref = clear_pd.loc[:,["refugeeID","taskID"]]
#     print("clear ref",clear_ref)
#     ref_df = get_refugee_dataframe(conn)
#     ref_data_row = ref_df.shape[0]
#     clear_ref_date_row = clear_ref.shape[0]
#     for i in range(ref_data_row):
#         for j in range(clear_ref_date_row):
#             if ref_df.loc[i,"refugeeID"] == clear_ref.loc[j,"refugeeID"]:
#                 if "," in ref_df.loc[i,"request"]:
#                     req_ref = ref_df.loc[i,"request"].split(",")
#                     print("req",req_ref)
#                     if clear_ref.loc[j,"taskID"] in req_ref:
#                         req_ref.remove(clear_ref.loc[j,"taskID"])
#                         new_req_ref = ",".join(req_ref)
#                         # remove request
#                         update_refdb_attr(conn,clear_ref.loc[j,"refugeeID"],"request",new_req_ref)
#                 else:
#                     if ref_df.loc[i,"request"] == clear_ref.loc[j,"taskID"]:
#                         # set request to 0
#                         update_refdb_attr(conn,clear_ref.loc[j,"refugeeID"],"request","0")


def display_open_camp_option(conn,condition):
    # refugee can only be assigned to the same plan as volunteer
    camp_query = ''
    if condition == "refugee":
        with open("user_session.json") as f:
            vol_login = json.load(f)
        vol_planID = vol_login["planID"]
        camp_query = f'''SELECT camp.planID,camp.campID,type,area,COUNT(refugeeID) as no_of_refugees,capacity FROM camp
                            LEFT JOIN refugee ON camp.campID = refugee.campID JOIN plan ON camp.planID=plan.planID WHERE plan.status=1
                            AND plan.planID = {vol_planID} GROUP BY camp.campID'''
    else:
        # volunteer
        camp_query = f'''SELECT camp.planID,camp.campID,type,area,COUNT(refugeeID) as no_of_refugees,capacity FROM camp
                            LEFT JOIN refugee ON camp.campID = refugee.campID JOIN plan ON camp.planID=plan.planID WHERE plan.status=1
                            GROUP BY camp.campID'''

    pd_camp = pd.read_sql_query(camp_query, conn)
    camp_df = pd.DataFrame(pd_camp, columns=['planID','campID','type','area','no_of_refugees', 'capacity'])
    camp_df = camp_df.drop(camp_df[camp_df['campID'] == 0].index)
    return camp_df

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
    df_task_ref_id = pd.DataFrame(pd_task,columns=["taskID","refugeeID","volunteerID","taskInfo","week","requestDate","workShift","status"])
    time.sleep(1.0)
    return df_task_ref_id

def get_volunteer_schedule_df(conn,campID=0,volunteer_ID = 0, purpose=''):
     # select from volunteer table which match the camp of refugee
    col_names = []
    query = ""
    if purpose == "Display":
        col_names = ["VolunteerID", "First Name", "Last Name",'CampID','Work Shift','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
        if campID == 0 and volunteer_ID != 0:
            query =  f'''SELECT volunteerID,fName,lName,campID,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer WHERE volunteerID={volunteer_ID}''' 
        elif campID != 0 and volunteer_ID == 0:
            query =  f'''SELECT volunteerID,fName,lName,campID,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer WHERE campID={campID}'''
        elif campID == 0 and volunteer_ID == 0:
            query =  f'''SELECT volunteerID,fName,lName,campID,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer'''
    elif purpose == "Status":
        query =  f'''SELECT volunteerID,fName,lName,campID,accountStatus,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer'''
    else:
        if volunteer_ID != 0 and campID==0:
            query =  f'''SELECT volunteerID,fName,lName,campID,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer WHERE volunteerID={volunteer_ID}'''
        else:
            query = f'''SELECT volunteerID,fName,lName,campID,workShift,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday FROM volunteer WHERE campID = {campID}'''

        col_names = ['VolunteerID', 'First Name', 'Last Name','CampID','Work Shift','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    
    pd_select = pd.read_sql_query(query,conn)

    # df_vol = pd.DataFrame(pd_select, columns=col_names)
    time.sleep(1.0)
    df_vol_sch = pd_select.copy(deep=True)
    col_list = list(df_vol_sch.columns[5:])
    data_row = df_vol_sch.shape[0]
    if purpose == "Status":
        col_list = list(df_vol_sch.columns[6:])
        for ind in df_vol_sch.index:
            if df_vol_sch["accountStatus"][ind] == 0:
                df_vol_sch.at[ind,"accountStatus"] = "Inactive"
            else:
                df_vol_sch.at[ind,"accountStatus"] = "Active"

    # Day schedule
    for c in col_list:
        for ind in df_vol_sch.index:
            if df_vol_sch[c][ind] == 0:
                df_vol_sch.at[ind,c] = u"\U00002705"
            elif df_vol_sch[c][ind] == -1 :
                df_vol_sch.at[ind,c] = u"\U0000274C"
            else:
                # task ID
                df_vol_sch.at[ind,c] = u"\U0001F4D1"

    return df_vol_sch


