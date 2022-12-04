import pandas as pd
import numpy as np
from refugee_input_option import *
from refugee_exception import *
from refugee_validation import *
from db_connect_ref import *
from refugee_utilities import *
from system_log import *


class Refugee:

    def __init__(self, purpose, conn):
        if purpose == "Register":
            print("\nWelcome to Refugee Registration System")
            print("--------------------------------------------\n")
            print("The form comprises of 4 main sections:\n1. Camp selection\n2. General information\n3. Medical condition\n4. Make a request")
        self.ref_row = []
        self.conn = conn

    def refugee_name(self):
        self.fname, self.lastname = refugee_existence_check(self.conn)
        self.ref_row.extend([self.fname, self.lastname])
        print("-------------------------------------------")

    def refugee_birthdate(self):
        # enter birthdate + validation
        self.birthdate = date_format_check("birthdate")
        self.ref_row.extend([self.birthdate])
        print("-------------------------------------------")

    def refugee_gender(self):
        gender_opt = refugee_input_option("Gender")
        gender_dict = input_matching("Gender")
        print("Select refugee's gender")
        self.gender = gender_dict[int(numerical_input_check(gender_opt)[0])]
        self.ref_row.extend([self.gender])
        print("-------------------------------------------")

    def refugee_race(self):
        race_opt = refugee_input_option("Ethnic Group")
        race_dict = input_matching("Ethnic Group")
        print("Select refugee's ethnic group")
        self.race = race_dict[int(numerical_input_check(race_opt)[0])]
        if ("Others" in self.race):
            self.race = input("Specify refugee's ethnic group: ")
        self.ref_row.extend([self.race])
        print("-------------------------------------------")

    def refugee_contact(self):
        self.email = email_format_check()
        self.phone = input("Enter refugee's phone number (if any): ")
        self.ref_row.extend([self.email, self.phone])
        print("-------------------------------------------")

    def refugee_family(self):
        self.members = input(
            "Enter all members' first name (e.g. Dan, John, Emily) or put '-' if no member: ")
        # add member's name
        self.ref_row.extend([self.members])

    def assign_camp_ID(self):
        # camp validation + assigned for creat and edit case only
        print("\nINSTRUCTION: Please assign the camp identification to the refugee.")
        print(
            "The detail below shows the availability of each camp as well as its related conditions: ")
        self.assigned_camp = camp_capacity_check(self.conn)
        # request

        # append camp number to the row
        self.ref_row.extend([self.assigned_camp])
        print(
            f"Refugee is successfully assigned to the camp number {self.assigned_camp}.")

    def refugee_illnesses(self):

        print("------------- MEDICAL SECTION 1 : ILLNESSES --------------")
        ill_opt = refugee_input_option("Illnesses")
        ill_dict = input_matching("Illnesses")
        print("Select refugee's personal illness")
        # array of input
        ill_inpts = numerical_input_check(ill_opt)

        # convert numerical input to text
        self.ref_illness = []
        for v in ill_inpts:
            self.ref_illness.append(ill_dict[int(v)])

        for ind, il in enumerate(self.ref_illness):
            if "Allergies" in il:
                print("-------------ALLERGIES--------------")
                aller_opt = refugee_input_option("Allergies")
                aller_dict = input_matching("Allergies")
                print("Select refugee's allergy conditions")
                # array of input
                aller_inpts = numerical_input_check(aller_opt)
                # convert numerical input to text
                self.allergy_cond = []
                for v in aller_inpts:
                    self.allergy_cond.append(aller_dict[int(v)])

                for ind2, al in enumerate(self.allergy_cond):
                    if ("Food" in al):
                        self.food_allergy = input(
                            "Please specify the type of food that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.food_allergy+")"
                    elif ("Medication" in al):
                        self.medicine_allergy = input(
                            "Please specify the name of medicine that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.medicine_allergy+")"
                    elif ("Others" in al):
                        self.others_allergy = input(
                            "Please specify other allergies: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.others_allergy+")"

                self.ref_allergy = ", ".join(self.allergy_cond)
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.ref_allergy + ")"
            if ("Others" in il):
                #  other disease please specify
                print("---------------OTHERS---------------")
                self.other_disc = input(
                    "Please specify other refugee's disease: ")
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.other_disc + ")"
        self.ref_illness = ",".join(self.ref_illness)
        # add illness to row
        self.ref_row.extend([self.ref_illness])

    def refugee_surgery(self):
        print("---------------MEDICAL SECTION 2 : SURGERY--------------")
        self.has_surgery = input(
            "Does refugee has the history of surgery? (Yes/No): ")
        if (self.has_surgery == "Yes"):
            self.surgery = input("Enter refugee's surgery record: ")
        else:
            self.surgery = "None"
        self.ref_row.extend([self.surgery])

    def refugee_smoking(self):
        print("---------------MEDICAL SECTION 3 : SMOKING HABIT--------------")
        self.smoker = input("Does refugee smoke? (Yes/No): ")
        self.ref_row.extend([self.smoker])

    def refugee_alcoholic(self):
        print("---------------MEDICAL SECTION 4 : ALCOHOL CONSUMPTION--------------")
        self.is_alcoholic = input("Is refugee an alcoholic? (Yes/No): ")
        # add medical cond to row
        self.ref_row.extend([self.is_alcoholic])

    def ref_request(self, purpose, req_edit_id=0):
        # df for use
        refugee_df = get_refugee_dataframe(self.conn)
        # Request manipulation system
        self.req_form_coll = []
        # case 1: create/add new req
        if purpose == "create" or purpose == "add":
            self.has_req = "Yes" if purpose == "add" else input(
                f"Would the refugee like to {purpose} any special requests? (Yes/No): ")
            if (self.has_req == "No"):
                self.ref_row.append("0")
                return self.req_form_coll
            else:
                req_counter = 1
                while True:
                    print("--------------------------------------------")
                    # select task
                    req_opt = refugee_input_option("Task Request")
                    print(
                        "Select 1 special request that a refugee would like to receive from a volunteer.")
                    req_inpt = numerical_input_check(req_opt)
                    req_dict = input_matching("Task Request")
                    self.req_task = req_dict[int(req_inpt[0])]
                    print("--------------------------------------------")
                    # select date
                    dates = get_date_list()
                    print(
                        "Select the request's start date from options below:\n")
                    c = 1
                    for i in dates:
                        dn = pd.Timestamp(i).day_name()
                        print(str(c)+".", dn, i)
                        c += 1
                    self.req_date = date_format_check(
                        "request", dates[0], dates[-1])
                    d = pd.Timestamp(self.req_date)
                    self.day_name = d.day_name()
                    print("-------------------------------------------")
                    # select workshift
                    print(
                        "Select 1 shift time that refugee's would like to receive a service.")
                    shift_opt = refugee_input_option("Shift Time")
                    shift_inpt = numerical_input_check(shift_opt)
                    shift_dict = input_matching("Shift Time")
                    self.req_shift = shift_dict[int(shift_inpt[0])]
                    print("-------------------------------------------")
                    # select volunteer
                    # query data from volunteer db which meet condition above
                    if purpose == "add":
                        self.assigned_camp = int(
                            refugee_df.loc[refugee_df["refugeeID"] == req_edit_id, "campID"].values[0])
                    vol_query = f'''SELECT volunteerID,fName,lName,workShift FROM volunteer WHERE workShift = "{self.req_shift}" AND accountStatus = 1 AND campID = {self.assigned_camp} AND {self.day_name} = 0'''
                    pd_sql = pd.read_sql_query(vol_query, self.conn)
                    vol_df = pd.DataFrame(
                        pd_sql, columns=['volunteerID', 'fName', 'lName', 'workShift'])
                    if vol_df.empty:
                        warn(
                            "There's no volunteer available for your selected date and work shift.\nPlease try again!\n")
                    else:
                        print(
                            "Please see the list of available volunteers who match refugee's request:\n")
                        print(vol_df)
                        # list : vol ID to help with multiple request case
                        self.vol_ID = volunteer_ID_req_check(vol_df)
                        print(
                            f"The request is successfully assigned to volunteer ID: {self.vol_ID}")
                        print("-------------------------------------------")
                        # to be assigned with task ID
                        if req_counter == 1 and purpose == "create":
                            self.ref_row.append("-1")
                        # assign 1 request to collector: list of dict
                        self.req_form_coll.append({"task": self.req_task, "date": self.req_date, "day": self.day_name,
                                                   "workshift": self.req_shift, "volunteer": self.vol_ID})
                        req_counter += 1
                        # allow adding multiple request, if no more -> end loop
                        end_req = input(
                            "Would refugee like to add more requests? (Yes/No): ")
                        if end_req == "No":
                            if purpose == "add":
                                # add to databases
                                req_ids = task_ref_vol_db(
                                    self.conn, self.req_form_coll, req_edit_id, refugee_df, "add")
                                self.ref_row.append(req_ids)
                            return self.req_form_coll

        elif purpose == "edit":
            # case 2: edit existing request
            req_id = str(
                refugee_df.loc[refugee_df["refugeeID"] == req_edit_id, "request"].values[0])
            self.ref_row.append(req_id)
            # show task table
            task_query = f'''SELECT * FROM task WHERE refugeeID = {req_edit_id} and status = "active"'''
            pd_task = pd.read_sql_query(task_query, self.conn)
            df_task = pd.DataFrame(pd_task, columns=[
                                   "taskID", "refugeeID", "volunteerID", "taskInfo", "week", "startDate", "workShift", "status"])
            print(
                "\nPlease see details below for the existing tasks assoiated with refugee's request:\n")
            print(df_task)
            task_edit = input(
                "Enter all task IDs which refugee would like to make change to: ")
            task_edit_arr = []
            if "," in task_edit:
                task_edit_arr.extend(task_edit.split(","))
            else:
                task_edit_arr.append(task_edit)
            # print("edit_task", task_edit_arr)
            # loop through selected task ID to edit
            for t in task_edit_arr:
                vol_id = df_task.loc[df_task["taskID"]
                                     == int(t), "volunteerID"].values[0]
                old_start_date = df_task.loc[df_task["taskID"] == int(
                    t), "startDate"].values[0]
                old_start_day = pd.Timestamp(old_start_date).day_name()
                print(
                    f"Note: You are allowed to change only request's date and work shift related to volunteer ID: {vol_id}.\n")
                print(f"\n-----EDITING TASK ID: [{t}]-----")
                while True:
                    # select new date
                    dates = get_date_list()
                    print("Please select the new request's date from options below: ")
                    c = 1
                    for i in dates:
                        dn = pd.Timestamp(i).day_name()
                        print(str(c)+".", dn, i)
                        c += 1
                    self.req_date = date_format_check(
                        "request", dates[0], dates[-1])
                    d = pd.Timestamp(self.req_date)
                    self.day_name = d.day_name()
                    print("-------------------------------------------")
                    # select new work shift
                    print("Please select new shift time from the options below: ")
                    shift_opt = refugee_input_option("Shift Time")
                    shift_inpt = numerical_input_check(shift_opt)
                    shift_dict = input_matching("Shift Time")
                    self.req_shift = shift_dict[int(shift_inpt[0])]
                    print("-------------------------------------------")
                    # check if volunteer is available
                    vol_query = f'''SELECT volunteerID,fName,lName,workShift FROM volunteer WHERE volunteerID = {vol_id} AND workShift = "{self.req_shift}" AND {self.day_name} = 0'''
                    pd_vol = pd.read_sql_query(vol_query, self.conn)
                    vol_df = pd.DataFrame(
                        pd_vol, columns=['volunteerID', 'fName', 'lName', 'workShift'])
                    if vol_df.empty:
                        warn(
                            "The volunteer is not available on the new selected date and shift!")
                    else:
                        # volunteer is available: update data in task table and volunteer table
                        cur = self.conn.cursor()
                        week_num = get_week_number(self.req_date)
                        task_upd = f'''UPDATE task SET week={week_num}, startDate = "{self.req_date}", workShift = "{self.req_shift}" WHERE taskID = {int(t)}'''
                        cur.execute(task_upd)
                        self.conn.commit()
                        time.sleep(2.0)
                        vol_upd = f'''UPDATE volunteer SET {old_start_day} = 0, {self.day_name} = {int(t)} WHERE volunteerID = {vol_id}'''
                        cur.execute(vol_upd)
                        self.conn.commit()
                        time.sleep(2.0)
                        print(
                            f"You have made change to refugee's request date and work shift of task ID: {int(t)}.")
                        print("-------------------------------------------\n")
                        break

    def add_refugee_to_db(self):
        # add status
        self.ref_row.append("active")
        # convert list to tuple
        self.ref_row_new = tuple(self.ref_row)
        # insert new refugee to db
        refugee_id = insert_refdb_row(self.conn, self.ref_row_new)
        return refugee_id

    # FINAL: Registration form
    def refugee_registration_form(self):
        # df for use
        refugee_df = get_refugee_dataframe(self.conn)
        # assign_camp_ID
        print("\n-------------------------------------------")
        print("ASSIGNING CAMP IDENTIFICATION")
        print("-------------------------------------------")
        self.assign_camp_ID()

        # general info
        print("\n-------------------------------------------")
        print("REFUGEE'S GENERAL INFORMATION")
        print("-------------------------------------------")
        self.refugee_name()
        self.refugee_birthdate()
        self.refugee_gender()
        self.refugee_race()
        self.refugee_contact()
        self.refugee_family()

        # medical condition
        print("\n-------------------------------------------")
        print("REFUGEE'S MEDICAL PROFILE")
        print("-------------------------------------------")
        self.refugee_illnesses()
        self.refugee_surgery()
        self.refugee_smoking()
        self.refugee_alcoholic()

        # request: return array of requests
        print("\n-------------------------------------------")
        print("REFUGEE'S REQUEST")
        print("-------------------------------------------")
        req_list = self.ref_request("create")
        print("-------------------------------------------")

        # add to database
        refugeeID = self.add_refugee_to_db()

        # CREATE case: update refugee, task, and volunteer table: can handle multiple req.
        task_ref_vol_db(self.conn, req_list, refugeeID, refugee_df, "create")
        print("New refugee is registered to the system. Thank you!")
