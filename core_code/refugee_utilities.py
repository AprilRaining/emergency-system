from refugee_exception import *
from refugee_validation import *
from db_connect_ref import *
import datetime

def get_date_list():
    theday = datetime.date.today()
    # print("today", theday)
    # start the week on Monday
    weekday = theday.isoweekday() - 1
    # print("weekday", weekday)
    start = theday - datetime.timedelta(days=weekday)
    # print("start", start)
    dates = [start + datetime.timedelta(days=d) for d in range(7)]
    # print("date", date)
    dates = [str(d) for d in dates]
    return dates

def task_ref_vol_db(conn,req_list,refugeeID, refugee_df, purpose):
    '''
    Used for create and add request only
    1.insert new row to task table
    2.update volunteer available days
    3.update refugee's request => contain added taskID
    '''
    if req_list != []:
        cur = conn.cursor()
        task_id = []
        if purpose == "create":
            print("Adding new refugee to the system................")
            print("Note: This usually takes around 1-2 minutes.")
        for req in req_list:
            print("Adding refugee's request................")
            # insert data to task table: multiple insertion
            task_insert = (refugeeID, req["volunteer"], req["task"],
                            req["date"], req["workshift"])
            ins_task_query = f'''INSERT INTO task(refugeeID,volunteerID,taskInfo,startDate,workShift) VALUES {task_insert}'''
            cur.execute(ins_task_query)
            conn.commit()
            time.sleep(12.0)
            task_id.append(cur.lastrowid)
            # update volunteer available day by task_ID
            upd_vol_query = f'''UPDATE volunteer SET "{req["day"]}" = {cur.lastrowid} WHERE volunteerID = {req["volunteer"]}'''
            cur.execute(upd_vol_query)
            conn.commit()
            time.sleep(8.0)

        # update request column in refugee table: insert ex. 1,2,3
        if purpose == "add":
            # database refugee will be updated in edit feature
            orig_req_id = str(refugee_df.loc[refugee_df["refugeeID"] == refugeeID, "request"].values[0])
            if(orig_req_id == "0" or orig_req_id == "-1"):
                # overwrite
                req_id_mul = ','.join([str(i) for i in task_id])
            else:
                # concat with existing req
                req_id_mul = orig_req_id + "," + ','.join([str(i) for i in task_id])
        else:
            # part of creating new refugee
            req_id_mul = ','.join([str(i) for i in task_id])
            upd_ref_query = f''' UPDATE refugee SET request = "{req_id_mul}" WHERE refugeeID = {refugeeID}'''
            cur.execute(upd_ref_query)
            time.sleep(5.0)
            conn.commit()
            cur.close()
    return req_id_mul