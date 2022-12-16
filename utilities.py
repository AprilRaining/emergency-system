import json

import refugee_exception as exc
from TableDisplayer import *


def admin_login():
    while True:
        print("--------------------------------------------------------------------------")
        prYellow("\t\t\t\tADMIN LOGIN\n")
        password = input(u"\U0001F539" + "Input the password of admin:")
        if str(password) == "12345":
            print("\n", u'\u2705', 'Welcome to the system, Admin!.')
            prYellow("\nPlease select your options below: \n")
            return
        else:
            warn("Wrong password! Check your input please.")


def volunteer_login():
    print("--------------------------------------------------------------------------")
    prYellow("\t\t\t\tVOLUNTEER LOGIN\n")
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        while True:
            name = input(u"\U0001F539" + "Input your username:")
            password = input(
                u"\U0001F539" + "Input the password of volunteer:")

            result = c.execute(f"select volunteerID, accountStatus from volunteer where username = '{name}' "
                               f"and password = '{password}'").fetchall()
            if len(result) > 0:
                if result[0][1] == 0:
                    warn(
                        "Your account has been deactivated, contact the administrator.\n")
                    return -1
                else:
                    print("\n", u'\u2705', 'Welcome to the system, Volunteer!.')
                    prYellow("\nPlease select your options below: \n")
                    return result[0][0]
            else:
                vol_res = c.execute(f"select * from deleted_vol_account where username = '{name}' "
                                    f"and password = '{password}'").fetchall()
                if len(vol_res) > 0:
                    warn("Account doesn't exist.")
                    return -1
                else:
                    warn("Wrong username or password! Check your input please.")


def check_week():
    current_week = datetime.datetime.isocalendar(datetime.datetime.now())[1]
    try:
        with open("conf.json") as f:
            json_file = json.load(f)
        if (json_file["LastLoginWeek"] != 0) and (json_file["LastLoginWeek"] != current_week):
            with sqlite3.connect('emergency_system.db') as conn:
                c = conn.cursor()
                vol_res = c.execute(
                    "select volunteerID, preference from volunteer").fetchall()
                volunteer_list = {x[0]: json.loads(x[1]) for x in vol_res}
                # print(volunteer_list)
                for v, pre in volunteer_list.items():
                    tem_sql = "UPDATE volunteer SET "
                    for col, val in pre.items():
                        if col == "workShift":
                            tem_sql += (f"{col} = '" +
                                        str(val.split()[0]) + "' ,")
                        else:
                            tem_sql += f"{col} = {val},"
                    tem_sql = tem_sql[:-1]
                    tem_sql += f" WHERE volunteerID = {v}"
                    # print(tem_sql)
                    c.execute(tem_sql)
                    conn.commit()

            with sqlite3.connect('emergency_system.db') as conn:
                c = conn.cursor()
                c.execute("update refugee set request = 0")
                conn.commit()
                c.execute(
                    "update task set status = 'inactive' where status = 'active'")
                conn.commit()
            print("The data of volunteers' schedule has been updated.")

        if json_file["LastLoginWeek"] != current_week:
            json_file["LastLoginWeek"] = current_week
            with open("conf.json", "w") as f:
                json.dump(json_file, f)

    except FileNotFoundError:
        print_log(
            "The conf file is not exist, please create it now and restart the system!")
        exit()
    except Exception as e:
        exit(e)


def check_plan():
    try:
        with sqlite3.connect('emergency_system.db') as conn:
            c = conn.cursor()
            c.execute("update plan set status = 1 where planID in "
                      "(select planID from plan where startDate <= DATE() and status = 0)")
            conn.commit()
    except Exception as e:
        print_log("Wrong connection to the database.")
        print(e)


def yn_valid(question):
    while True:
        try:
            user_input = input(f"{question}")
            if user_input != 'Yes' and user_input != 'No':
                raise exc.wrong_yn_input
        except exc.wrong_yn_input:
            print_log("Your input is invalid. Please enter either 'Yes' or 'No'")
        except Exception as e:
            print(e)
        else:
            return user_input


def select_sqlite(table, IDs):
    IDsBackUp = IDs
    while True:
        TableDisplayer.match(table)(IDs)
        if not IDs:
            IDs = IDsBackUp
            TableDisplayer.match(table)(IDs)
        print("\n", u"\U0001F531" +
              '[Hint]Input 0 to search by other keys e.g area, status')
        IDs.append(0)
        ID = Get.option_in_list(
            IDs, u"\U0001F539" + f'Please input the {table}ID to choose a {table}: ')
        if ID == 0:
            IDs = search_sqlite(table)
        else:
            return ID
