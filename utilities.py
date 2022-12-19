import json
from system_log import *
import TableDisplayer
import datetime
import refugee_exception as exc
from TableDisplayer import *


def admin_login():
    while True:
        print("--------------------------------------------------------------------------")
        prYellow("\t\t\t\tADMIN LOGIN\n")
        username = Get.string(u"\U0001F539" + "Input the username of admin:")
        password = Get.string(u"\U0001F539" + "Input the password of admin:")
        if str(username) == "admin" and str(password) == "111":
            print("\n", u'\u2705', 'Welcome to the system, Admin!.')
            prYellow("\nPlease select your options below: \n")
            return
        else:
            warn("Wrong username or password! Check your input please.")


def volunteer_login():
    print("--------------------------------------------------------------------------")
    prYellow("\t\t\t\tVOLUNTEER LOGIN\n")
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        while True:
            name = Get.string(u"\U0001F539" + "Input your username:")
            password = Get.string(
                u"\U0001F539" + "Input the password of volunteer:")
            name_res = c.execute(f"select * from volunteer where username = '{name}'").fetchall()
            if not name_res:
                warn("Account do not exist!")
                continue

            result = c.execute(f"select volunteerID, accountStatus, volunteer.campID, camp.planID from volunteer join camp on volunteer.campID = camp.campID where username = '{name}' "
                               f"and password = '{password}'").fetchall()
            if len(result) > 0:
                if result[0][1] == 0:
                    warn(
                        "Your account has been deactivated, please contact the administrator.")
                    input('Input any key to continue: ')
                    return [-1]
                else:
                    # keep user session
                    volunteer_current = {"volunteerID": result[0][0], "campID": result[0][2],
                                         "planID": result[0][3], "login_time": str(datetime.datetime.today())}
                    with open("user_session.json", "w") as f:
                        json.dump(volunteer_current, f)

                    result = list(result[0])
                    result.append(
                        c.execute(f'select planID from camp where campID = {result[2]}').fetchall()[0][0])
                    print("\n", u'\u2705', 'Welcome to the system, Volunteer!.')
                    prYellow("\nPlease select your options below: \n")
                    return result
            else:
                warn("Wrong password! Check your input please.")




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


def select_sqlite(table, IDs):
    IDsBackUp = IDs.copy()
    while True:
        if not IDs:
            prYellow('No result!')
            input('Input any key to continue!')
            IDs = IDsBackUp.copy()
        TableDisplayer.match(table)(IDs)
        print("\n", u"\U0001F531" +
              '[Hint]Input 0 to search by other keys e.g area, status')
        IDs.append(0)
        ID = Get.option_in_list(
            IDs, u"\U0001F539" + f'Please input the {table}ID to choose a {table}: ')
        if ID == 0:
            IDs = search_sqlite(table)
            continue
        else:
            return ID


def select_camps_from_plan(planIDs):
    if not planIDs:
        return
    else:
        while True:
            if not planIDs:
                planIDs = get_all_IDs('plan')
            TableDisplayer.plan(planIDs)
            print("\n", u"\U0001F531" +
                  '[Hint]Input 0 to search by other keys e.g area, status')
            option = input("\n" +
                           u"\U0001F539" + f"Input a plan ID to view more details or 'Q/q' to quit:")
            print("\n")
            if option != 'q' and option != 'Q':
                try:
                    option = int(option)
                except ValueError:
                    print_log("Please reenter a valid value.")
                else:
                    if option == 0:
                        planIDs = search_sqlite('plan')
                        continue
                    elif option not in planIDs:
                        print_log(
                            f'{option} is not a valid input. Please try again.')
                    else:
                        campIDs = get_linked_IDs('camp', 'plan', option)
                        if campIDs:
                            print("\n" + u"\U0001F538" +
                                  f"Camps in the plan ID {option}:")
                            TableDisplayer.camp(campIDs)
                            return campIDs
                        else:
                            print('No camps under this plan ' + u"\u203C")
                            return False
            else:
                return False


def select_info_from_camp(campIDs):
    if not campIDs:
        return
    else:
        while True:
            option = input("\n"
                           u"\U0001F539" + f"Input a camp ID to view more details or 'Q/q' to quit:")
            if option != 'q' and option != 'Q':
                try:
                    option = int(option)
                except ValueError:
                    print_log("Please reenter a valid value.")
                else:
                    if option not in campIDs:
                        print(
                            f'{option} is not a valid input. Please try again.')
                    else:
                        volunteerIDs = get_linked_IDs(
                            'volunteer', 'camp', option)
                        refugeeIDs = get_linked_IDs(
                            'refugee', 'camp', option)
                        if volunteerIDs:
                            print("\n" + u"\U0001F538" +
                                  f"Volunteers in the camp ID {option}:")
                            TableDisplayer.volunteer(volunteerIDs)
                        else:
                            print("\n" + 'No volunteer in this camp ' +
                                  u"\u203C" + "\n")
                        if refugeeIDs:
                            print("\n" + u"\U0001F538" +
                                  f"Refugees in the camp ID {option}:")
                            TableDisplayer.refugee(refugeeIDs)
                        else:
                            print('No refugee in this camp ' + u"\u203C")
                        back()
                        return
            else:
                return
