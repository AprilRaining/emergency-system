from myfunctionlib import *
from exception.refugee_exception import *
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
                    self.delete_emergency_refugee_file()
                case 0:
                    return

    def create_emergency_refugee_file(self):
        refugee_df = pd.read_csv('info_files/refugee.csv')
        camp_df = pd.read_csv('info_files/camp.csv')
        
        while True:
            # create instance of refugee
            new_ref = Refugee("Register")
            # register new refugee
            new_ref.refugee_registration_form(refugee_df,camp_df)
            cont_proc = input("Would you like to continue registering more refugees?(Yes/No): ")
            if cont_proc == "No":
                sys.exit()


    def edit_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        refugee_df = pd.read_csv('info_files/refugee.csv')
        camp_df = pd.read_csv('info_files/camp.csv')
        ref_df_by_id = refugee_validity_check_by_ID("edit",refugee_df)
        print("-------------------------------------------")
        print("Select a database field that you would like to edit")
        edit_opt = refugee_input_option("Edit")
        edit_arr = numerical_input_check(edit_opt)
        # print("arr",edit_arr)
        print("\n-------------------INFO EDITION-------------------")
        for e in edit_arr:
            edited_fields = refugee_info_edit(int(e),refugee_df,camp_df,refugee_df.loc[ref_df_by_id, 'camp_ID'])
            # print("field",edited_fields)
            edited_dice = input_matching("Edit")
            col_name_arr = edited_dice[int(e)]
            # print("col",col_name_arr)
            for i in range(len(col_name_arr)):
                refugee_df.at[ref_df_by_id,col_name_arr[i]] = edited_fields[i]
            
        # update database
        with open('info_files/refugee.csv', 'w') as f:
            refugee_df.to_csv(f,index=False)
        print("-------------------------------------------")
        print("The refugee's information is successfully updated.")

    def close_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        refugee_df = pd.read_csv('info_files/refugee.csv')
        ref_df_by_id = refugee_validity_check_by_ID("deactivate",refugee_df)
        print("-------------------------------------------")
        # deactivate the refugee with specified ID and add to file
        inactive_ref = refugee_df.loc[refugee_df["refugee_ID"] == ref_df_by_id]
        with open('info_files/inactive_refugee.csv', 'a') as f:
            inactive_ref.to_csv(f, header=False,index=False)
        # move refugee out of the camp
        camp_df = pd.read_csv('info_files/camp.csv')
        # print("check",camp_df)
        ref_inac = Refugee("close")
        ref_inac.assign_camp_ID(camp_df,"close",refugee_df.loc[refugee_df["refugee_ID"] == ref_df_by_id,"camp_ID"].values[0])
        # delete data from active refugee file
        refugee_df.drop(refugee_df.index[(refugee_df["refugee_ID"] == ref_df_by_id)],axis=0,inplace=True)
        # update database
        with open('info_files/refugee.csv', 'w') as f:
            refugee_df.to_csv(f, index=False)
        print("The refugee's information is successfully deactivated.")

    def reopen_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        inac_refugee_df = pd.read_csv('info_files/inactive_refugee.csv')
        ref_df_by_id = refugee_validity_check_by_ID("activate",inac_refugee_df)
        print("-------------------------------------------")
        # activate the refugee with specified ID and add to file
        inactive_ref = inac_refugee_df.loc[inac_refugee_df["refugee_ID"] == ref_df_by_id]
        with open('info_files/refugee.csv', 'a') as f:
            inactive_ref.to_csv(f, header=False,index=False)
        # add refugee to camp file
        camp_df = pd.read_csv('info_files/camp.csv')
        ref_ac = Refugee("reopen")
        ref_ac.assign_camp_ID(camp_df,"reopen",inac_refugee_df.loc[inac_refugee_df["refugee_ID"] == ref_df_by_id,"camp_ID"].values[0])
        # delete data from inactive refugee file
        inac_refugee_df.drop(inac_refugee_df.index[(inac_refugee_df["refugee_ID"] == ref_df_by_id)],axis=0,inplace=True)
        # update database
        with open('info_files/inactive_refugee.csv', 'w') as f:
            inac_refugee_df.to_csv(f,index=False)
        print("The refugee's information is successfully activated.")
        

    def delete_emergency_refugee_file(self):
        print("Welcome to refugee information system")
        print("-------------------------------------------")
        refugee_df = pd.read_csv('info_files/refugee.csv')
        ref_df_by_id = refugee_validity_check_by_ID("delete",refugee_df)
        print("-------------------------------------------")
        # move refugee out of the camp
        camp_df = pd.read_csv('info_files/camp.csv')
        ref_del = Refugee("delete")
        ref_del.assign_camp_ID(camp_df,"close",refugee_df.loc[refugee_df["refugee_ID"] == ref_df_by_id,"camp_ID"].values[0])
        # delete the refugee with specified ID
        refugee_df.drop(refugee_df.index[(refugee_df["refugee_ID"] == ref_df_by_id)],axis=0,inplace=True)
        # update database
        with open('info_files/refugee.csv', 'w') as f:
            refugee_df.to_csv(f, index=False)
        print("The refugee's information is successfully deleted.")

        
        
v1 = Volunteer()
# v1.create_emergency_refugee_file()
# v1.edit_emergency_refugee_file()
# v1.delete_emergency_refugee_file()
# v1.close_emergency_refugee_file()
# v1.reopen_emergency_refugee_file()