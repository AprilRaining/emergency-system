import pandas as pd
import numpy as np
from refugee_input_option import *
from refugee_exception import *
from refugee_validation import *
from db_connect_ref import *
from refugee_utilities import *
from system_log import *
from print_table import *


class Refugee:

    def __init__(self, purpose, conn):
        if purpose == "Register":
            print("The form comprises of 4 main sections:\n1. Camp selection\n2. General information\n3. Medical condition\n4. Make a request\n")
        self.ref_row = []
        self.conn = conn

    def refugee_name(self):
        print("------------------------NAME----------------------------\n")
        self.fname, self.lastname = refugee_existence_check(self.conn)
        self.ref_row.extend([self.fname, self.lastname])
        print("\n")

    def refugee_birthdate(self):
        print("-----------------------BIRTHDAY-------------------------\n")
        # enter birthdate + validation
        self.birthdate = date_format_check("birthdate")
        self.ref_row.extend([self.birthdate])
        print("\n")

    def refugee_gender(self):
        print("------------------------GENDER--------------------------\n")
        gender_opt = refugee_input_option("Gender")
        gender_dict = input_matching("Gender")
        print(u"\U0001F539"+"Select refugee's gender")
        self.gender = gender_dict[int(numerical_input_check(gender_opt)[0])]
        self.ref_row.extend([self.gender])
        print("\n")

    def refugee_race(self):
        print("----------------------ETHNIC GROUP----------------------\n")
        race_opt = refugee_input_option("Ethnic Group")
        race_dict = input_matching("Ethnic Group")
        print(u"\U0001F539"+"Select refugee's ethnic group")
        self.race = race_dict[int(numerical_input_check(race_opt)[0])]
        if ("Others" in self.race):
            self.race = input(u"\U0001F539"+"Specify refugee's ethnic group: ")
        self.ref_row.extend([self.race])
        print("\n")

    def refugee_contact(self):
        print("------------------------CONTACT-------------------------\n")
        self.email = email_format_check()
        self.phone = input(u"\U0001F539"+"Enter refugee's phone number (if any): ")
        self.ref_row.extend([self.email, self.phone])
        print("\n")

    def refugee_family(self):
        print("---------------------FAMILY MEMBERS---------------------\n")
        self.members = input(
            u"\U0001F539"+"Enter all members' first name (e.g. Dan, John, Emily) or put '-' if no member: ")
        # add member's name
        self.ref_row.extend([self.members])
        print("\n")

    def assign_camp_ID(self,purpose='',campid=0):
        # camp validation + assigned for creat and edit case only
        print("\n"+u"\U0001F531"+"INSTRUCTION: Please assign the camp identification to the refugee.")
        print(
            "The detail below shows the availability of each camp as well as its related conditions: \n")
        (self.assigned_camp,selc_camp_df) = camp_capacity_check(self.conn,purpose,campid)

        # append camp number to the row
        self.ref_row.extend([self.assigned_camp])
        print(
            u'\u2705'+f"Refugee is successfully assigned to the camp number {self.assigned_camp}.\n")
        print(u"\U0001F538"+"Please see the camp detail below:\n")
        print_table(selc_camp_df.columns,selc_camp_df.to_numpy().tolist(),(25,25,70,70,70,40))
        

    def refugee_illnesses(self):

        print("------------- MEDICAL SECTION 1 : ILLNESSES --------------\n")
        ill_opt = refugee_input_option("Illnesses")
        ill_dict = input_matching("Illnesses")
        print(u"\U0001F539"+"Select refugee's personal illness (Allow multiple selection(e.g. 1,3,6))")
        # array of input
        ill_inpts = numerical_input_check(ill_opt)

        # convert numerical input to text
        self.ref_illness = []
        for v in ill_inpts:
            self.ref_illness.append(ill_dict[int(v)])

        for ind, il in enumerate(self.ref_illness):
            if "Allergies" in il:
                print("-------------ALLERGIES--------------\n")
                aller_opt = refugee_input_option("Allergies")
                aller_dict = input_matching("Allergies")
                print(u"\U0001F539"+"Select refugee's allergy conditions (Allow multiple selection(e.g. 2,4))")
                # array of input
                aller_inpts = numerical_input_check(aller_opt)
                # convert numerical input to text
                self.allergy_cond = []
                for v in aller_inpts:
                    self.allergy_cond.append(aller_dict[int(v)])

                for ind2, al in enumerate(self.allergy_cond):
                    if ("Food" in al):
                        self.food_allergy = input(
                            u"\U0001F539"+"Please specify the type of food that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.food_allergy+")"
                    elif ("Medication" in al):
                        self.medicine_allergy = input(
                            u"\U0001F539"+"Please specify the name of medicine that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.medicine_allergy+")"
                    elif ("Others" in al):
                        self.others_allergy = input(
                            u"\U0001F539"+"Please specify other allergies: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                            "("+self.others_allergy+")"

                self.ref_allergy = ", ".join(self.allergy_cond)
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.ref_allergy + ")"
            if ("Others" in il):
                #  other disease please specify
                print("---------------OTHERS---------------\n")
                self.other_disc = input(
                    u"\U0001F539"+"Please specify other refugee's disease: ")
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.other_disc + ")"
        self.ref_illness = ",".join(self.ref_illness)
        # add illness to row
        self.ref_row.extend([self.ref_illness])
        print("\n")

    def refugee_surgery(self):
        print("---------------MEDICAL SECTION 2 : SURGERY--------------\n")
        self.has_surgery = yn_valid(u"\U0001F539"+
            "Does refugee has the history of surgery? (Yes/No): ")
        if (self.has_surgery == "Yes"):
            self.surgery = input(u"\U0001F539"+"Enter refugee's surgery record: ")
        else:
            self.surgery = "None"
        self.ref_row.extend([self.surgery])
        print("\n")

    def refugee_smoking(self):
        print("------------MEDICAL SECTION 3 : SMOKING HABIT------------\n")
        self.smoker = yn_valid(u"\U0001F539"+"Does refugee smoke? (Yes/No): ")
        self.ref_row.extend([self.smoker])
        print("\n")

    def refugee_alcoholic(self):
        print("----------MEDICAL SECTION 4 : ALCOHOL CONSUMPTION----------\n")
        self.is_alcoholic = yn_valid(u"\U0001F539"+"Is refugee an alcoholic? (Yes/No): ")
        # add medical cond to row
        self.ref_row.extend([self.is_alcoholic])
        print("\n")

    def ref_request(self, purpose, req_edit_id=0):
        # df for use
        refugee_df = get_refugee_dataframe(self.conn)
        df_vol_sch = ""
        # Request manipulation system
        self.req_form_coll = []
        # case 1: create/add new req
        if purpose == "create" or purpose == "add":
            print(u"\U0001F531"+'''INSTRUCTION: Refugee can make request(s) for available volunteers 
            to provide a special care that matches with his/her needs. 
            However, we recommend adding no more than 3 requests per week.\n''')
            self.has_req = "Yes" if purpose == "add" else yn_valid(
                u"\U0001F539"+f"Would the refugee like to {purpose} any special requests? (Yes/No): ")
            if (self.has_req == "No"):
                self.ref_row.append("0")
                return self.req_form_coll
            else:
                req_counter = 1
                while True:
                    # select task
                    req_opt = refugee_input_option("Task Request")
                    print(
                        u"\U0001F539"+"Select 1 special request that a refugee would like to receive from a volunteer.\n")
                    req_inpt = single_input_check(req_opt)
                    req_dict = input_matching("Task Request")
                    self.req_task = req_dict[int(req_inpt[0])]
                    print("---------------------------------------------------------------------------")
                    # show volunteer schedule FYI
                    print(u"\U0001F531"+"[Hint]Please see our volunteer schedule below for your information.\nWe recommend selecting volunteer who is available at the date and time of refugee's request.\n")
                    if req_counter == 1:
                        if purpose == "add":
                            self.assigned_camp = int(refugee_df.loc[refugee_df["refugeeID"] == req_edit_id, "campID"].values[0])
                        df_vol_sch = get_volunteer_schedule_df(
                            self.conn, self.assigned_camp)
                    if df_vol_sch.empty:
                        # for testing
                        warn("No volunteer in the camp! Please add volunteer to the camp first.")
                        self.ref_row.append("0")
                        return
                    else:
                        print_table(df_vol_sch.columns,df_vol_sch.to_numpy().tolist(),(18,25,25,16,20,30,30,30,30,30,30,30))
                    print("---------------------------------------------------------------------------")
                    # select date
                    dates = get_date_list()
                    c = 1
                    today_date = str(datetime.date.today())
                    today_ind = dates.index(today_date)
                    for i in dates:
                        if dates.index(i) >= int(today_ind):
                            dn = pd.Timestamp(i).day_name()
                            print("[ "+str(c)+".]", dn, i)
                            c += 1
                    # check volunteer availability
                    has_free_vol = False
                    for ind in df_vol_sch.index:
                        vol_row = df_vol_sch.iloc[ind]
                        vol_row_info = vol_row.to_numpy()
                        if "free" in vol_row_info[len(vol_row_info)-(c-1):len(vol_row_info)]:
                            has_free_vol = True
                    if has_free_vol == False:
                        if purpose == "add":
                            warn("You cannot add more requests because the volunteer schedule cannot accommodate more requests.\n Note: If you have just added new requests prior to this, they will be lost. Please start again!")
                        else:
                            warn("You cannot make a request because there is no available volunteers from today to the end of this week.\nPlease try again next week!")
                        self.ref_row.append("0")
                        return
                    print(
                        "\n"+"Select your request's day for this week from options above\n")
                    self.req_date = date_format_check(
                        "request", today_date, dates[-1])
                    d = pd.Timestamp(self.req_date)
                    self.day_name = d.day_name()

                    print("--------------------------------------------------------------------------\n")
                    # show recommended volunteer
                    df_match_vol = df_vol_sch.loc[df_vol_sch[self.day_name] == "free", :]
                    if df_match_vol.empty:
                        warn(
                            "There is no volunteer available on your selected date. Please try again!")
                    else:
                        # select workshift
                        print(
                            u"\U0001F539"+"Select 1 shift time that refugee's would like to receive a service.")
                        shift_opt = refugee_input_option("Shift Time")
                        shift_inpt = single_input_check(shift_opt)
                        shift_dict = input_matching("Shift Time")
                        self.req_shift = shift_dict[int(shift_inpt[0])]
                        print("--------------------------------------------------------------------------")
                        # select volunteer
                        # query data from volunteer db which meet condition above
                        vol_query = f'''SELECT volunteerID,fName,lName,workShift FROM volunteer WHERE workShift = "{self.req_shift}" AND accountStatus = 1 AND campID = {self.assigned_camp} AND {self.day_name} = 0'''
                        pd_sql = pd.read_sql_query(vol_query, self.conn)
                        time.sleep(1.0)
                        vol_df = pd.DataFrame(
                            pd_sql, columns=['volunteerID', 'fName', 'lName', 'workShift'])
                        if vol_df.empty:
                            warn(
                                "There's no volunteer available for your selected date and work shift.\nWe recommend checking our volunteer schedule below and try again!\n")
                            print_table(df_vol_sch.columns,df_vol_sch.to_numpy().tolist(),(18,25,25,16,20,30,30,30,30,30,30,30))
                        else:
                            print(
                               u"\U0001F539"+"Please see the list of available volunteers who match refugee's request:\n")
                            print_table(vol_df.columns,vol_df.to_numpy().tolist(),(20,40,40,40))
                            # list : vol ID to help with multiple request case
                            self.vol_ID = volunteer_ID_req_check(vol_df)
                            print(
                               u'\u2705'+f"The request is successfully assigned to volunteer ID: {self.vol_ID}")
                            # alter dataframe display
                            df_vol_sch.loc[df_vol_sch["volunteerID"] ==
                                           self.vol_ID, self.day_name] = "booked"
                            print("--------------------------------------------------------------------------")
                            # to be assigned with task ID
                            if req_counter == 1 and purpose == "create":
                                self.ref_row.append("-1")
                            # assign 1 request to collector: list of dict
                            self.req_form_coll.append({"task": self.req_task, "date": self.req_date, "day": self.day_name,
                                                       "workshift": self.req_shift, "volunteer": self.vol_ID})
                            req_counter += 1
                            # allow adding multiple request, if no more -> end loop
                            end_req = yn_valid(
                                u"\U0001F539"+"Would refugee like to add more requests? (Yes/No): ")
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
                                   "taskID", "refugeeID", "volunteerID", "taskInfo", "week", "requestDate", "workShift", "status"])
            print(
                "\nPlease see details below for the existing tasks assoiated with refugee's request:\n")
            print_table(df_task.columns,df_task.to_numpy().tolist(),(20,20,20,40,40,40,40,40))
            task_edit = input(
                u"\U0001F539"+"Enter all task IDs which refugee would like to make change to: ")
            task_edit_arr = []
            if "," in task_edit:
                task_edit_arr.extend(task_edit.split(","))
            else:
                task_edit_arr.append(task_edit)
            # print("edit_task", task_edit_arr)
            # loop through selected task ID to edit
            task_count = 1
            for t in task_edit_arr:
                vol_id = df_task.loc[df_task["taskID"]
                                     == int(t), "volunteerID"].values[0]
                old_start_date = df_task.loc[df_task["taskID"] == int(
                    t), "requestDate"].values[0]
                old_start_day = pd.Timestamp(old_start_date).day_name()
                print("\n"+
                   u"\U0001F531"+f"\nINSTRUCTION: You are allowed to change only request's date and work shift related to volunteer ID: {vol_id}.\n")
                print(f"\n-----EDITING TASK ID: [{t}]-----\n")
                while True:
                    # show  volunteer schedule
                    print(u"\U0001F531"+"[Hint]Please see the volunteer schedule below for your information.\n")
                    if task_count == 1:
                        df_vol_sch = get_volunteer_schedule_df(
                            conn = self.conn, volunteer_ID = vol_id)
                    print_table(df_vol_sch.columns,df_vol_sch.to_numpy().tolist(),(18,25,25,16,20,30,30,30,30,30,30,30))
                    print("\n")
                    # select new date
                    dates = get_date_list()
                    c = 1
                    today_date = str(datetime.date.today())
                    today_ind = dates.index(today_date)
                    for i in dates:
                        if dates.index(i) >= int(today_ind):
                            dn = pd.Timestamp(i).day_name()
                            print("[ "+str(c)+".]", dn, i)
                            c += 1
                    # check volunteer availability
                    has_free_vol = False
                    for ind in df_vol_sch.index:
                        vol_row = df_vol_sch.iloc[ind]
                        vol_row_info = vol_row.to_numpy()
                        if "free" in vol_row_info[len(vol_row_info)-(c-1):len(vol_row_info)]:
                            has_free_vol = True
                    if has_free_vol == False:
                        warn("You cannot change your request date because the volunteers are fully booked from today to the end of this week.\nPlease try again next week!")
                        self.ref_row.append("0")
                        return
                    print("\n"+u"\U0001F539"+"Please select the new request's date from options above: ")
                    self.req_date = date_format_check(
                        "request", today_date, dates[-1])
                    d = pd.Timestamp(self.req_date)
                    self.day_name = d.day_name()
                    print("--------------------------------------------------------------------------")
                    # select new work shift
                    print(u"\U0001F539"+"Please select new shift time from the options below: ")
                    shift_opt = refugee_input_option("Shift Time")
                    shift_inpt = single_input_check(shift_opt)
                    shift_dict = input_matching("Shift Time")
                    self.req_shift = shift_dict[int(shift_inpt[0])]
                    print("--------------------------------------------------------------------------")
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
                        task_upd = f'''UPDATE task SET week={week_num}, requestDate = "{self.req_date}", workShift = "{self.req_shift}" WHERE taskID = {int(t)}'''
                        cur.execute(task_upd)
                        self.conn.commit()
                        time.sleep(1.0)
                        # update old day to 0 and new day to task ID
                        vol_upd = f'''UPDATE volunteer SET {old_start_day} = 0, {self.day_name} = {int(t)} WHERE volunteerID = {vol_id}'''
                        cur.execute(vol_upd)
                        self.conn.commit()
                        time.sleep(0.6)
                        print(
                           u'\u2705'+f"You have made change to refugee's request date and work shift of task ID: {int(t)}.")
                        print("--------------------------------------------------------------------------\n")
                        # alter dataframe display
                        df_vol_sch.loc[df_vol_sch["volunteerID"] ==
                                           vol_id, self.day_name] = "booked"
                        df_vol_sch.loc[df_vol_sch["volunteerID"] ==
                                           vol_id, old_start_day] = "free"
                        break
                task_count +=1

    def add_refugee_to_db(self):
        # add status
        self.ref_row.append("active")
        # convert list to tuple
        self.ref_row_new = tuple(self.ref_row)
        # insert new refugee to db
        prGreen("..........Adding new refugee to the system............\n")
        refugee_id = insert_refdb_row(self.conn, self.ref_row_new)
        return refugee_id

    # FINAL: Registration form
    def refugee_registration_form(self):
        # df for use
        refugee_df = get_refugee_dataframe(self.conn)
        # assign_camp_ID
        prCyan("\n--------------------------------------------------------------------------")
        prLightPurple("----------------------ASSIGNING CAMP IDENTIFICATION-----------------------")
        prCyan("--------------------------------------------------------------------------\n")
        self.assign_camp_ID("create")

        # general info
        prCyan("\n--------------------------------------------------------------------------")
        prLightPurple("-----------------------REFUGEE'S GENERAL INFORMATION----------------------")
        prCyan("--------------------------------------------------------------------------\n")
        self.refugee_name()
        self.refugee_birthdate()
        self.refugee_gender()
        self.refugee_race()
        self.refugee_contact()
        self.refugee_family()

        # medical condition
        prCyan("\n--------------------------------------------------------------------------")
        prLightPurple("-------------------------REFUGEE'S MEDICAL PROFILE------------------------")
        prCyan("--------------------------------------------------------------------------\n")
        self.refugee_illnesses()
        self.refugee_surgery()
        self.refugee_smoking()
        self.refugee_alcoholic()
        # default request
        self.ref_row.append("0")

        # add to database
        refugeeID = self.add_refugee_to_db()
        print(u"\U0001F538"+f"New refugee ID created: [{refugeeID}]\n")
        print("\n",u'\u2705'+"New refugee is successfully registered to the system!\n")

        # request: return array of requests
        prCyan("\n--------------------------------------------------------------------------")
        prLightPurple("-----------------------------REFUGEE'S REQUEST----------------------------")
        prCyan("--------------------------------------------------------------------------\n")
        req_list = self.ref_request("create")
        # if the system quit before finished
        if req_list == None:
            return
        print("\n--------------------------------------------------------------------------\n")

        # CREATE case: update refugee, task, and volunteer table: can handle multiple req.
        req_id = task_ref_vol_db(
            self.conn, req_list, refugeeID, refugee_df, "create")
