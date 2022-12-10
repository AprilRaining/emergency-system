import sqlite3
import json
from datetime import datetime

def admin_login():
    while True:
        password = input("Input the password of admin:")
        if str(password) == "12345":
            print(f'\nWelcome to the system, Admin.')
            return
        else:
            print("Wrong password! Check your input please.")


def volunteer_login():
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        while True:
            name = input("Input your username:")
            password = input("Input the password of volunteer:")

            result = c.execute(f"select volunteerID, accountStatus from volunteer where username = '{name}' and password = '{password}'").fetchall()
            if len(result) > 0:
                if result[0][1] == 0:
                    print("Your account has been deactivated, contact the administrator.\n")
                    return -1
                elif result[0][1] == -1:
                    print("Account doesn't exist.")
                    return -1
                else:
                    return result[0][0]
            else:
                print("Wrong username or password! Check your input please.")


def check_week():
    current_week = datetime.isocalendar(datetime.now())[1]
    try:
        with open("conf.json") as f:
            json_file = json.load(f)
        if (json_file["LastLoginWeek"] != 0) and (json_file["LastLoginWeek"] != current_week):
            with sqlite3.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                vol_res = c.execute("select volunteerID, preference from volunteer").fetchall()
                volunteer_list = {x[0]: json.loads(x[1]) for x in vol_res}
                # print(volunteer_list)
                for v, pre in volunteer_list.items():
                    tem_sql = "UPDATE volunteer SET "
                    for col, val in pre.items():
                        if col == "workShift":
                            tem_sql += (f"{col} = '" + str(val.split()[0]) + "' ,")
                        else:
                            tem_sql += f"{col} = {val},"
                    tem_sql = tem_sql[:-1]
                    tem_sql += f" WHERE volunteerID = {v}"
                    # print(tem_sql)
                    c.execute(tem_sql)
                    conn.commit()

            with sqlite3.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute("update refugee set request = 0")
                conn.commit()
                c.execute("update task set status = 'inactive' where status = 'active'")
                conn.commit()
            print("The data of volunteers' schedule has been updated.")

        if json_file["LastLoginWeek"] != current_week:
            json_file["LastLoginWeek"] = current_week
            with open("conf.json", "w") as f:
                json.dump(json_file, f)

    except FileNotFoundError:
        print("The conf file is not exist, please create it now and restart the system!")
        exit()
    except Exception as e:
        exit(e)


def check_plan():
    try:
        with sqlite3.connect('info_files/emergency_system.db') as conn:
            c = conn.cursor()
            c.execute("update plan set status = 2 where endDate < DATE()")
            conn.commit()
    except Exception as e:
        print("Wrong connection to the database.")
        print(e)
