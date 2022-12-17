from refugee_exception import *
from refugee_validation import *
from db_connect_ref import *
import datetime
import progress_bar as pb


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

def get_current_shift_time():
    shift = ''
    now = datetime.datetime.now()
    morning_shift_1 = now.replace(hour=6, minute=0, second=0, microsecond=0)
    morning_shift_2 = now.replace(hour=14, minute=0, second=0, microsecond=0)
    afternoon_shift_1 = now.replace(hour=14, minute=0, second=0, microsecond=0)
    afternoon_shift_2 =now.replace(hour=22, minute=0, second=0, microsecond=0)
    night_shift_1 = now.replace(hour=22, minute=0, second=0, microsecond=0)
    night_shift_2 = now.replace(hour=6, minute=0, second=0, microsecond=0)
    if now >= morning_shift_1 and now < morning_shift_2:
        shift = "Morning"
    elif now >= afternoon_shift_1 and now < afternoon_shift_2:
        shift = "Afternoon"
    elif now >= night_shift_1 and now < night_shift_2:
        shift = "Night"
    return shift

def check_today_shift_conflict(current_shift,volunteer_shift):
    has_conflict = False
    if volunteer_shift == "Morning":
        if current_shift == "Afternoon" or current_shift == "Night":
            has_conflict = True
    elif volunteer_shift == "Afternoon":
        if current_shift == "Night":
            has_conflict = True
    return has_conflict

def get_week_number(date):
    # split date
    y, m, d = tuple(date.split("-"))
    # get day of week as an integer
    week_num = datetime.date(int(y), int(m), int(d)).isocalendar()[1]
    return week_num

def search_refugee(column, keyword, conn):
    result = []
    if type(keyword) == type(''):
        keyword = "'%{}%'".format(keyword)
    search_query = "SELECT * FROM refugee WHERE {} LIKE {}".format(column, keyword)
    # print(search_query)
    pd_search = pd.read_sql_query(search_query,conn)
    df_search = pd.DataFrame(pd_search, columns=["refugeeID","campID","fName","lName","birthdate","gender","ethnicGroup","email",
                "phone","familyMemberName","illness","surgery","smoking","alcoholic","request","status"])
    return df_search


def task_ref_vol_db(conn, req_list, refugeeID, refugee_df, purpose):
    '''
    Used for create and add request only
    1.insert new row to task table
    2.update volunteer available days
    3.update refugee's request => contain added taskID
    '''
    req_id_mul = ""
    if req_list != []:
        prGreen("\n.............Refugee's requests processing.............")
        cur = conn.cursor()
        task_id = []
        if purpose == "create":
            print("\n"+u"\u2757"+"Note: This usually takes around 15-20 seconds to add multiple requests.\n")
        pb.progress_bar(0,len(req_list),"")
        for ind,req in enumerate(req_list):
            # insert data to task table: multiple insertion
            week_num = get_week_number(req["date"])
            task_insert = (refugeeID, req["volunteer"], req["task"], week_num,
                           req["date"], req["workshift"],"active")
            ins_task_query = f'''INSERT INTO task(refugeeID,volunteerID,taskInfo,week,requestDate,workShift,status) VALUES {task_insert}'''
            cur.execute(ins_task_query)
            conn.commit()
            time.sleep(2.8)
            task_id.append(cur.lastrowid)
            # update volunteer available day by task_ID
            upd_vol_query = f'''UPDATE volunteer SET "{req["day"]}" = {cur.lastrowid} WHERE volunteerID = {req["volunteer"]}'''
            cur.execute(upd_vol_query)
            conn.commit()
            time.sleep(1.4)
            pb.progress_bar(ind+1,len(req_list),"")

        # update request column in refugee table: insert ex. 1,2,3
        if purpose == "add":
            # database refugee will be updated in edit feature
            orig_req_id = str(
                refugee_df.loc[refugee_df["refugeeID"] == refugeeID, "request"].values[0])
            if (orig_req_id == "0" or orig_req_id == "-1"):
                # overwrite
                req_id_mul = ','.join([str(i) for i in task_id])
            else:
                # concat with existing req
                req_id_mul = orig_req_id + "," + \
                    ','.join([str(i) for i in task_id])
        else:
            # part of creating new refugee
            req_id_mul = ','.join([str(i) for i in task_id])
            upd_ref_query = f''' UPDATE refugee SET request = "{req_id_mul}" WHERE refugeeID = {refugeeID}'''
            cur.execute(upd_ref_query)
            time.sleep(1.2)
            conn.commit()
            cur.close()
        print("\n\n",u'\u2705'+"New volunteer request is added to the schedule!\n")


    return req_id_mul
