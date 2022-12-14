from datetime import datetime
import datetime
from myfunctionlib import *
from refugee_exception import *
from refugee_validation import *
from refugee_input_option import *
from refugee_info_edit import *
from refugee import Refugee
import pandas as pd
import sqlite3 as db
from get import *
import json
from options import *
import copy
from print_table import *


def connection_database(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print("Access system successfully!\n")
    except Exception as e:
        print("could not connect to the database")
        print(e)
    return conn


class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __init__(self, last_name=None, first_name=None, password=None, campID=None, workingShift=None, workingdays=None, volunteer_id=None):
        """
        To Do:
        1. Process Login when construct a new admin
        2. Show the menu
        3. Maybe for first login require the volunteer to edit their personal information first.
        :return:
        """
        self.menu = menu(self.__class__.__name__)
        self.last_name = last_name
        self.first_name = first_name
        self.password = password
        self.campID = campID
        self.workingShift = workingShift
        self.workingdays = workingdays
        self.volunteerID = volunteer_id

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1,"\n-->"):
                case 1:
                    self.manage_personal_information()
                    back()
                case 2:
                    self.manage_camp_file()
                    back()
                case 3:
                    self.manage_task()
                    back()
                case 0:
                    return

    def manage_personal_information(self):
        print("--------------------------------------------------------")
        print("\t\tVOLUNTEER PERSONAL INFO\n")
        while True:
            print("Please select what you want to do: \n")
            print(menu())
            match menu_choice_get(menu().count('\n') + 1,"\n-->"):
                case 1:
                    self.edit_my_information()
                case 2:
                    self.show_my_information()
                case 0:
                    return

    def edit_my_information(self):
        print("--------------------------------------------------------")
        print("\t\tEDIT VOLUNTEER INFO\n")
        while True:
            print(menu())
            match menu_choice_get(menu('edit_my_information').count('\n') + 1,"\n-->"):
                case 1:
                    self.edit_volunteers_name()
                case 2:
                    self.edit_password()
                case 3:
                    self.edit_working_perference()
                case 4:
                    self.edit_campid()
                case 0:
                    return

    def edit_volunteers_name(self):
        print("--------------------------------------------------------")
        print("\t\tEDIT VOLUNTEER NAME\n")
        conn = connection_database("info_files/emergency_system.db")
        cur = conn.cursor()
        while True:
            volunteer_input_id = self.volunteerID
            query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
            cur.execute(query_1)

            weekday = cur.fetchall()

            if len(weekday) == 0:
                warn("you input the wrong volunteerID please try again!")
                continue
            else:
                break
        first_name = input(u"\U0001F539"+"Please input your new first name: ")
        last_name = input(u"\U0001F539"+"Please input your new last name: ")
        self.last_name = last_name
        self.first_name = first_name

        query = f'''UPDATE volunteer SET fName='{first_name}',lName='{last_name}' WHERE volunteerID = {volunteer_input_id}'''
        cur.execute(query)
        conn.commit()
        cur.close()
        print(u'\u2705'+"Your new name have been changed to: " + first_name + " " + last_name, "\n")

    def edit_password(self):
        print("--------------------------------------------------------")
        print("\t\tEDIT VOLUNTEER PASSWORD\n")
        conn = connection_database("info_files/emergency_system.db")
        cur = conn.cursor()
        while True:
            volunteer_input_id = self.volunteerID
            query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
            cur.execute(query_1)

            weekday = cur.fetchall()

            if weekday == []:
                warn("You input the wrong volunteerID please try again:\n")
                continue
            else:
                break

        new_password = input(u"\U0001F539"+"Please input your new password: ")
        self.password = new_password
        query = f'''UPDATE volunteer SET password ='{new_password}' WHERE volunteerID = {volunteer_input_id}'''
        cur.execute(query)
        conn.commit()
        cur.close()
        print(u'\u2705'+"You have changed your password successfully!\n")

    def edit_working_perference(self):
        print("--------------------------------------------------------")
        print("\t\tEDIT VOLUNTEER WORKING TIME\n")
        conn = connection_database("info_files/emergency_system.db")
        cur = conn.cursor()

        preference = {'Monday': -1,
                      'Tuesday': -1,
                      'Wednesday': -1,
                      'Thursday': -1,
                      'Friday': -1,
                      'Saturday': -1,
                      'Sunday': -1,
                      'workShift': "Morning"}  # used to store the json information

        while True:
            volunteer_input_id = self.volunteerID
            query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
            cur.execute(query_1)

            weekday = cur.fetchall()

            if weekday == []:
                warn("You input the wrong volunteerID please try again:\n")
                continue
            else:
                break
        
        now = datetime.datetime.now()
        the_day = now.weekday()
        day_name = now.strftime("%A")
        print("Today is a weekday: " + day_name)

        for the_day in range(the_day, 6):
            judge = weekday[0][the_day]
            if judge > 0:
                warn("You cannot change your working shift because you still have unfinished work.")
                break
        else:
            if confirm("You can change your preference now, enter 'Yes' to continue"):

                print("Please select your preferred day to work:\n"
                      "[ 1.] Monday\n"
                      "[ 2.] Tuesday\n"
                      "[ 3.] Wednesday\n"
                      "[ 4.] Thursday\n"
                      "[ 5.] Friday\n"
                      "[ 6.] Saturday\n"
                      "[ 7.] Sunday\n")
                options = Get.listing(1, 8, u"\U0001F539" + "Please input your new working day(s) in a comma-separated format (e.g 1,2 or 5): ")

            else:
                return

            match = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
            for i in options:
                preference[match[i]] = 0

            preference_json = json.dumps(preference)
            print(u"\U0001F538"+"Your new working days now become:", [day for day,val in preference.items() if val == 0])
            query = f'''UPDATE volunteer SET preference='{preference_json}' WHERE volunteerID = {volunteer_input_id}'''
            cur.execute(query)
            conn.commit()

            print("\n"+u'\u2705'+"You successfully changed your next week working day!\n")
            print("Your current working shift is: " + preference['workShift'])
            print("Note: If you dont want to change the working shift, please select same option as the previous one! \n")

            options_shift = Options(['Morning', 'Afternoon', 'Night'], limited=True)
            print(options_shift)
            options_preference = options_shift.get_option(u"\U0001F539"+"Please choose your preferred workShift: ")
            match_preference = ['Morning', 'Afternoon', 'Night']
            preference['workShift'] = match_preference[options_preference]
            preference = json.dumps(preference)
            query = f'''UPDATE volunteer SET preference='{preference}' WHERE volunteerID = {volunteer_input_id}'''
            cur.execute(query)
            conn.commit()
            cur.close()
            print("\n"+u'\u2705'+"You have changed your preferred work shift successfully!\n")


    def edit_campid(self):
        print("--------------------------------------------------------")
        print("\t\tEDIT VOLUNTEER CAMP ID\n")
        conn = connection_database("info_files/emergency_system.db")
        cur = conn.cursor()

        while True:
            volunteer_input_id = self.volunteerID
            query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
            cur.execute(query_1)

            weekday = cur.fetchall()

            if weekday == []:
                warn("You input the wrong volunteerID please try again:\n")
                continue
            else:
                break

        now = datetime.datetime.now()
        the_day = now.weekday()
        day_name = now.strftime("%A")
        print("Today is a weekday: " + day_name)

        for the_day in range(the_day, 6):
            judge = weekday[0][the_day]
            if judge > 0:
                warn("You cannot change your campID because you still have unfinished work")
                break
        else:
            # cur.execute(f'''SELECT campID from volunteer where volunteerID = '{volunteer_input_id}''')
            # volunteer_campid=cur.fetchall()[0][0]
            # cur.execute(f'''select planID from camp where campID = {volunteer_campid}''')
            # plan_id=cur.fetchall()[0][0]
            # search("camp", "planID", plan_id)
            input_new_campid=input(u"\U0001F539"+"Please input your new campID: ")

            query_camp=f'''UPDATE volunteer SET campID='{input_new_campid}' WHERE volunteerID = {volunteer_input_id}'''
            self.campID=input_new_campid
            cur.execute(query_camp)
            conn.commit()
            cur.close()
            print("\n",u'\u2705'+"You have changed your campID successfully!\n")

    def show_my_information(self):
        print("--------------------------------------------------------")
        print("\t\tSHOW VOLUNTEER INFO\n")
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus,  
                              Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, workShift, 
                              preference FROM volunteer WHERE volunteerID = {self.volunteerID}''')
                info = list(c.fetchall()[0])
                person_info = copy.deepcopy(info[:6])
                status = person_info.pop()
                person_info.append("active" if status == 1 else "deactive")
            fd = pd.DataFrame([person_info],
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp ID",
                                       "Account status"])

            print(u"\U0001F538","Please see your personal information below: \n")
            print_table(fd.columns,fd.to_numpy().tolist(),(12,20,20,20,16,20))
            weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            schedule = {}
            for day, flag in enumerate(info[6:-2]):
                if flag == -1:
                    schedule[weekday[day]] = "unavailable"
                elif flag == 0:
                    schedule[weekday[day]] = "available"
                else:
                    schedule[weekday[day]] = f"taskID: {flag}"
            schedule["work_period"] = info[-2]
            info_df = pd.DataFrame(schedule, index=[0])
            print("\n",u"\U0001F538",f"Your current schedule for this week is:  \n")
            print_table(info_df.columns,info_df.to_numpy().tolist(),(20,20,20,20,20,20,20,20))

            preference = {}
            for day, flag in json.loads(info[-1]).items():
                if flag == -1:
                    preference[day] = "unavailable"
                elif flag == 0:
                    preference[day] = "available"
                elif day == "workShift":
                    preference["work_period"] = flag
                else:
                    preference[weekday[day]] = f"taskID: {flag}"
            pre_df = pd.DataFrame(preference, index=[0])
            print(u"\U0001F539"+ f"\nYour default schedule when first registered is: \n")
            print_table(pre_df.columns,pre_df.to_numpy().tolist(),(20,20,20,20,20,20,20,20))
        except:
            print("Wrong connection to the database.")
        pass

    def manage_camp_file(self):
        while True:
            print("Please select what you want to do: \n")
            print(menu())
            match menu_choice_get(menu().count('\n') + 1,"\n-->"):
                case 1:
                    self.create_emergency_refugee_file()
                case 2:
                    self.edit_emergency_refugee_file()
                case 3:
                    self.close_emergency_refugee_file()
                case 4:
                    self.reopen_emergency_refugee_file()
                case 5:
                    self.delete_emergency_refugee_file()
                case 0:
                    return

    @staticmethod
    def system_exit_check():
        cont_proc = yn_valid(
                "Would you like to exit the system?(Yes/No): ")
        if cont_proc == "Yes":
            return True
        else:
            return False

    def create_emergency_refugee_file(self):
        conn = connect_db()
        while True:
            # create instance of refugee
            new_ref = Refugee("Register", conn)
            # register new refugee
            new_ref.refugee_registration_form()
            if self.system_exit_check():
                return

    def edit_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("---------------------------------------------------")
        conn = connect_db()
        refugee_df = get_refugee_dataframe(conn)
        ref_df_by_id = refugee_validity_check_by_ID("edit", refugee_df, conn)
        print("---------------------------------------------------")
        print("Select a database field that you would like to edit: ")
        edit_opt = refugee_input_option("Edit")
        edit_arr = numerical_input_check(edit_opt)
        # print("arr",edit_arr)
        print("\n-------------------INFO EDITION-------------------")
        edited_dict = input_matching("Edit")
        for e in edit_arr:
            # array of ref_row
            edited_fields = refugee_info_edit(
                int(e), ref_df_by_id, refugee_df, conn)
            col_name_arr = edited_dict[int(e)]
            # print("field", edited_fields,"col", col_name_arr)
            for i in range(len(col_name_arr)):
                # update info in database
                update_refdb_attr(conn, ref_df_by_id,
                                  col_name_arr[i], edited_fields[i])

        print("---------------------------------------------------")
        print("The refugee's information is successfully updated.\n")
        self.system_exit_check()

    def close_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        conn = connect_db()
        refugee_df = get_refugee_dataframe(conn)
        ref_df_by_id = refugee_validity_check_by_ID("deactivate", refugee_df, conn)
        print("\nPlease see refugee details below.\nYou can activate this refugee account anytime.\n")
        print(refugee_df.loc[refugee_df["refugeeID"] == ref_df_by_id])
        # get req id
        ref_req = str(
            refugee_df.loc[refugee_df["refugeeID"] == ref_df_by_id, "request"].values[0])
        if ref_req != "0":
            # task
            df_task_ref_id = select_task_by_ref_id(conn, ref_df_by_id)
            # clear out volunteer schedule related to this refugee req
            print("deactivating refugee account.................")
            clear_request_schedule(conn,df_task_ref_id)
        # update status and request: refugee table => set status to inactive + set request to 0
        update_refdb_attr(conn, ref_df_by_id, "status", "inactive")
        update_refdb_attr(conn, ref_df_by_id, "request", "0")
        print("--------------------------------------------------")
        print("The refugee's information is successfully deactivated.\n")
        self.system_exit_check()

    def reopen_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        conn = connect_db()
        refugee_df = get_refugee_dataframe(conn)
        ref_df_by_id = refugee_validity_check_by_ID("activate", refugee_df, conn)
        # update datebase: refugee[status] to active
        update_refdb_attr(conn, ref_df_by_id, "status", "active")
        print("--------------------------------------------------")
        print("The refugee's information is successfully activated.\n")
        self.system_exit_check()

    def delete_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        conn = connect_db()
        refugee_df = get_refugee_dataframe(conn)
        ref_df_by_id = refugee_validity_check_by_ID("delete", refugee_df, conn)
        print("\nPlease see refugee details below before deleting.\n")
        print(refugee_df.loc[refugee_df["refugeeID"] == ref_df_by_id])
        # get req id
        ref_req = refugee_df.loc[refugee_df["refugeeID"]
                                 == ref_df_by_id, "request"].values[0]
        confirm_del = yn_valid(
            "Are you sure you want to delete this refugee from the system?(Yes/No): ")
        if confirm_del == "Yes":
            if ref_req != "0":
                # task
                df_task_ref_id = select_task_by_ref_id(conn, ref_df_by_id)
                # clear out volunteer schedule related to this refugee req
                print("deleting refugee information................")
                clear_request_schedule(conn,df_task_ref_id)
                # delete related task
                del_task = f'''DELETE FROM task WHERE refugeeID = {ref_df_by_id}'''
                cur = conn.cursor()
                cur.execute(del_task)
                conn.commit()
                time.sleep(3.0)

            # delete refugee
            delete_ref_by_id(conn, ref_df_by_id)
            print("--------------------------------------------------")
            print("The refugee's information is successfully deleted.\n")
        self.system_exit_check()


    def manage_task(self):
        print("--------------------------------------------------------")
        print("\t\tVOLUNTEER TASK MANAGEMENT\n")
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1, "\n-->"):
                case 1:
                    volunteer_id = input(u"\U0001F539"+"Enter volunteer ID: ")
                    self.view_my_schedule(volunteer_id)
                case 0:
                    return

    def view_my_schedule(self, ID):
        def get_current_weekday():
            monday = datetime.date.today()
            one_day = datetime.timedelta(days=1)
            while monday.weekday() != 0:
                monday -= one_day
            tuesday = monday + one_day
            wednesday = tuesday + one_day
            thursday = wednesday + one_day
            friday = thursday + one_day
            saturday = friday + one_day
            sunday = saturday + one_day

            return datetime.datetime.strftime(monday, "%Y-%m-%d"), datetime.datetime.strftime(tuesday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(wednesday, "%Y-%m-%d"), datetime.datetime.strftime(thursday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(friday, "%Y-%m-%d"), datetime.datetime.strftime(saturday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(sunday, "%Y-%m-%d")

        day_schedule = []

        def display_schedule(volunteer, day, date):
            try:
                with db.connect('info_files/emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT taskInfo, workShift FROM task WHERE volunteerID = (?) and requestDate = (?)''',
                              (volunteer, date))
                    task = c.fetchall()
                    task_arr = []
                    task_sch = []
                    for ind,t in enumerate(task):
                        task_arr.append(task[ind][3])
                        task_sch.append(task[ind][6])

                    task_info = ",".join(task_arr)
                    task_schedule = ",".join(task_sch)

                day_schedule = [day, u"\u26AA", u"\u26AA", u"\u26AA"]
                if task_schedule == 'Morning':
                    day_schedule = [day, task_info, u"\u26AA", u"\u26AA"]
                elif task_schedule == 'Afternoon':
                    day_schedule = [day, u"\u26AA", task_info, u"\u26AA"]
                elif task_schedule == 'Night':
                    day_schedule = [day, u"\u26AA", u"\u26AA", task_info]
            except IndexError:
                day_schedule = [day, u"\u26AA", u"\u26AA", u"\u26AA"]
            return day_schedule

        date_monday = get_current_weekday()[0]
        date_tuesday = get_current_weekday()[1]
        date_wednesday = get_current_weekday()[2]
        date_thursday = get_current_weekday()[3]
        date_friday = get_current_weekday()[4]
        date_saturday = get_current_weekday()[5]
        date_sunday = get_current_weekday()[6]

        d = []
        d.append(display_schedule(ID, 'Monday', date_monday))
        d.append(display_schedule(ID, 'Tuesday', date_tuesday))
        d.append(display_schedule(ID, 'Wednesday', date_wednesday))
        d.append(display_schedule(ID, 'Thursday', date_thursday))
        d.append(display_schedule(ID, 'Friday', date_friday))
        d.append(display_schedule(ID, 'Saturday', date_saturday))
        d.append(display_schedule(ID, 'Sunday', date_sunday))

        print("{:<15} {:<15} {:<15} {:<15}".format('Day', 'Morning(06:00 - 14:00)',
                                                   'Afternoon(14:00 - 22:00)', 'Night(22:00 - 06:00)'))

        for v in d:
            day, morning, afternoon, night = v
            print("{:<15} \t{:<22} {:<24} {:<15}".format(day, morning, afternoon, night))
        print("\n")





# v1 = Volunteer()
# v1.create_emergency_refugee_file()
# v1.edit_emergency_refugee_file()
# v1.delete_emergency_refugee_file()
# v1.close_emergency_refugee_file()
# v1.reopen_emergency_refugee_file()