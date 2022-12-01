from myfunctionlib import *
from refugee_exception import *
from refugee_validation import *
from refugee_input_option import *
from refugee_info_edit import *
from refugee import Refugee
import pandas as pd


class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __init__(self):
        """
        To Do:
        1. Process Login when construct a new admin
        2. Show the menu
        3. Maybe for first login require the volunteer to edit their personal information first.
        :return:
        """
        self.menu = menu(self.__class__.__name__)
        self.volunteerID = None

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    self.manage_personal_information()
                case 2:
                    self.manage_camp_file()
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

    def create_emergency_refugee_file(self):
        conn = connect_db()
        while True:
            # create instance of refugee
            new_ref = Refugee("Register", conn)
            # register new refugee
            new_ref.refugee_registration_form()
            cont_proc = input(
                "Would you like to continue registering more refugees?(Yes/No): ")
            if cont_proc == "No":
                sys.exit()

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
        print("The refugee's information is successfully updated.")

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
        print("The refugee's information is successfully deactivated.")

    def reopen_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        conn = connect_db()
        refugee_df = get_refugee_dataframe(conn)
        ref_df_by_id = refugee_validity_check_by_ID("activate", refugee_df, conn)
        # update datebase: refugee[status] to active
        update_refdb_attr(conn, ref_df_by_id, "status", "active")
        print("--------------------------------------------------")
        print("The refugee's information is successfully activated.")

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
        confirm_del = input(
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
            print("The refugee's information is successfully deleted.")


v1 = Volunteer()
# v1.create_emergency_refugee_file()
v1.edit_emergency_refugee_file()
# v1.delete_emergency_refugee_file()
# v1.close_emergency_refugee_file()
# v1.reopen_emergency_refugee_file()
