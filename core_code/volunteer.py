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



class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __init__(self, volunteer_id=None):
        """
        To Do:
        1. Process Login when construct a new admin
        2. Show the menu
        3. Maybe for first login require the volunteer to edit their personal information first.
        :return:
        """
        self.menu = menu(self.__class__.__name__)
        self.volunteerID = volunteer_id

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    self.manage_personal_information()
                case 2:
                    self.manage_camp_file()
                case 3:
                    self.manage_task()
                case 0:
                    return

    def manage_personal_information(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.edit_my_information()
                case 2:
                    self.show_my_information()
                case 0:
                    return

    def edit_my_information(self):
        pass

    def show_my_information(self):
        pass

    def manage_camp_file(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
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
            return

    def create_emergency_refugee_file(self):
        conn = connect_db()
        while True:
            # create instance of refugee
            new_ref = Refugee("Register", conn)
            # register new refugee
            new_ref.refugee_registration_form()
            self.system_exit_check()

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
                time.sleep(5.0)

            # delete refugee
            delete_ref_by_id(conn, ref_df_by_id)
            print("--------------------------------------------------")
            print("The refugee's information is successfully deleted.\n")
        self.system_exit_check()


# v1 = Volunteer()
# v1.create_emergency_refugee_file()
# v1.edit_emergency_refugee_file()
# v1.delete_emergency_refugee_file()
# v1.close_emergency_refugee_file()
# v1.reopen_emergency_refugee_file()


    def manage_task(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    volunteer_id = input("Enter ur ID")
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

        def display_schedule(volunteer, day, date):
            try:
                with db.connect('info_files/emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM task WHERE volunteerID = (?) and startDate = (?)''', (volunteer, date))
                    task = c.fetchall()
                    task_info = task[0][3]
                    task_schedule = task[0][5]
                if task_schedule == 'morning':
                    day_schedule = [day, task_info, '/', '/']
                elif task_schedule == 'afternoon':
                    day_schedule = [day, '/', task_info, '/']
                elif task_schedule == 'night':
                    day_schedule = [day, '/', '/', task_info]
            except IndexError:
                day_schedule = [day, '/', '/', '/']
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
            print("{:<15} {:<22} {:<24} {:<15}".format(day, morning, afternoon, night))



