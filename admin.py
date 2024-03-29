from accountInput import *
from db_connect_ref import *
from manageEmergencyPlan import *
from system_log import *


class Admin:
    """
        This is the admin class for admin program.
    """

    def __init__(self):
        """
        TO DO:
        1. Process Login when construct a new admin
        2. Show the menu
        :return:
        """
        # Process Login. If fail more than 5 times. Exit
        # Get Menu
        self.menu = menu(self.__class__.__name__)

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1, "\n-->"):
                case 1:
                    manage_emergency_plan = ManageEmergencyPlan()
                    manage_emergency_plan.sub_main()
                case 2:
                    self.manage_account()
                case 0:
                    return

    def manage_account(self):
        print("--------------------------------------------------------------------------")
        prPurple("\t\t\tVOLUNTEER ACCOUNTS MANAGEMENT\n")
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1, "\n-->"):
                case 1:
                    self.reactive_volunteer_account()
                    back()
                case 2:
                    self.deactive_volunteer_account()
                    back()
                case 3:
                    self.creat_a_volunteer_account()
                    back()
                case 4:
                    self.display_volunteer_account()
                case 5:
                    self.delete_account()
                    back()
                case 0:
                    return

    def reactive_volunteer_account(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tREACTIVATE VOLUNTEER ACCOUNT\n")
        print(u"\U0001F531" +
              "Please see volunteer details below for your information: \n")
        conn1 = connect_db()
        vol_df = get_volunteer_schedule_df(conn1, purpose="Status")
        print_table(vol_df.columns, vol_df.to_numpy().tolist(),
                    (25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35))
        print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
              " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")

        ID = Get.int(u"\U0001F539"+'Enter the volunteer ID:')

        try:
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(
                    f'''SELECT accountStatus FROM volunteer WHERE volunteerID = (?)''', (ID,))
                status = c.fetchall()[0][0]
                time.sleep(1.0)
            if status == 1:
                print("This account is already active. No need to activate.")
                print("-------------------------------------")
            else:
                c.execute(
                    f'''UPDATE volunteer SET accountStatus = 1 WHERE volunteerID = (?)''', (ID,))
                conn.commit()
                newCampID = AccountCreation.get_camp_id()
                c.execute(
                    f'''UPDATE volunteer SET campID = {newCampID} WHERE volunteerID = {ID}''')
                conn.commit()
                print("\n" +
                      u'\u2705', "Volunteer with ID {}'s account is now reactivated.".format(ID))
        except IndexError:
            print_log("{} is an invalid ID".format(ID))
        except:
            print_log("Wrong connection to the database.")

    def deactive_volunteer_account(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tDEACTIVATE VOLUNTEER ACCOUNT\n")
        print(u"\U0001F531" +
              "Please see volunteer details below for your information: \n")
        conn1 = connect_db()
        vol_df = get_volunteer_schedule_df(conn1, purpose="Status")
        print_table(vol_df.columns, vol_df.to_numpy().tolist(),
                    (25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35))
        print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
              " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
        ID = Get.int(u"\U0001F539"+'Enter the volunteer ID:')
        try:
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(
                    f'''SELECT accountStatus FROM volunteer WHERE volunteerID = (?)''', (ID,))
                status = c.fetchall()[0][0]
                # time.sleep(1.0)
            if status == 0:
                warn("This account is currently inactive.")
                print("-------------------------------------")
            else:
                if confirm(u"\U0001F539"+f"Do you want to deactivate this account ID {ID}?"):
                    day_col = list(vol_df.columns[6:])
                    vol_df_byID = vol_df.loc[vol_df["volunteerID"] == ID, :]
                    has_req = False
                    for d in day_col:
                        for ind in vol_df_byID.index:
                            if vol_df_byID[d][ind] == u"\U0001F4D1":
                                has_req = True
                    if has_req == False:
                        c.execute(
                            f'''UPDATE volunteer SET accountStatus = 0 WHERE volunteerID = (?)''', (ID,))
                        conn.commit()
                        c.execute(
                            f'''UPDATE volunteer SET campID = 0 WHERE volunteerID = (?)''', (ID,))
                        conn.commit()
                        print("\n" +
                              u'\u2705', "Volunteer with ID {}'s account is now inactive.".format(ID))
                    else:
                        print("\n")
                        print_table(vol_df_byID.columns, vol_df_byID.to_numpy().tolist(
                        ), (25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35))
                        print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
                              " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
                        warn(
                            "You cannot deactivate this volunteer account because there is still a task request from the refugee.")
                        return

                else:
                    return
        except IndexError:
            print_log("{} is an invalid ID".format(ID))
        except:
            print_log("Wrong connection to the database.")

    def creat_a_volunteer_account(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tCREATE VOLUNTEER ACCOUNT\n")
        new_volunteer = []

        fname = Get.string(u"\U0001F539" + 'Enter the first name:')
        lname = Get.string(u"\U0001F539" + 'Enter the last name:')
        username = AccountCreation.get_username()
        password = Get.string(u"\U0001F539" + 'Enter the password:')
        campID = AccountCreation.get_camp_id()
        planID = get_planID(campID)
        preference = AccountCreation.get_week_preference()
        workshift = AccountCreation.get_work_shift()

        show_dict = {"First Name": fname, "Last Name": lname, "Username": username, "Password": password,
                     'PlanID': planID, "CampID": campID, "Preference": preference, "Workshift": workshift}
        while True:
            print("\n"+u"\U0001F531" +
                  "This is the new volunteer account's information.\n")
            for key, value in show_dict.items():
                if key == "Preference":
                    day_coll = ["Monday", "Tuesday", "Wednesday",
                                "Thursday", "Friday", "Saturday", "Sunday"]
                    avai_val = []
                    val_dict = value
                    for k, v in val_dict.items():
                        if v == -1:
                            avai_val.append("Unavailable")
                        elif v == 0:
                            avai_val.append("Available")
                    pref_df = pd.DataFrame(
                        {"Day": day_coll, "Availability": avai_val})
                    print(u"\U0001F4C6", 'Weekly schedule: \n')
                    print_table(pref_df.columns,
                                pref_df.to_numpy().tolist(), (20, 20))
                else:
                    print(u"\U0001F538" + key, ': ', value)
            check = input(
                u"\U0001F539" + "If the information is right, please press Y/y, or N/n to correct: ")
            if check == "Y" or check == "y":
                break
            elif check == "N" or check == "n":
                while True:
                    opt_second = Options([
                        'First Name',
                        'Last Name',
                        'Username',
                        'Password',
                        'CampID',
                        'Preference',
                        'Workshift'
                    ])
                    print(opt_second)
                    opt = opt_second.get_option(
                        "Please input what you want to correct from this list: ")
                    input_second = opt_second.values[opt - 1]
                    if input_second in show_dict.keys():
                        if input_second == "First Name":
                            show_dict["First Name"] = Get.string(
                                u"\U0001F539" + 'Enter the first name:')
                        elif input_second == "Last Name":
                            show_dict["Last Name"] = Get.string(
                                u"\U0001F539" + 'Enter the last name:')
                        elif input_second == "Username":
                            show_dict["Username"] = AccountCreation.get_username()
                        elif input_second == "Password":
                            show_dict["Password"] = Get.string(
                                u"\U0001F539" + 'Enter the password:')
                        elif input_second == "CampID":
                            show_dict["CampID"] = AccountCreation.get_camp_id()
                            show_dict["PlanID"] = get_planID(
                                show_dict["CampID"])
                        elif input_second == "Preference":
                            show_dict["Preference"] = AccountCreation.get_week_preference(
                            )
                        elif input_second == "Workshift":
                            show_dict["Workshift"] = AccountCreation.get_work_shift()
                        break
                    else:
                        warn("Wrong Input. Please try again!")
            else:
                warn("Illegal input!. Please input Y/y or N/n:\n")

        preference = show_dict["Preference"]
        preference["workShift"] = show_dict["Workshift"]
        json_preference = json.dumps(preference)

        new_volunteer.append(show_dict["First Name"])
        new_volunteer.append(show_dict["Last Name"])
        new_volunteer.append(show_dict["Username"])
        new_volunteer.append(show_dict["Password"])
        new_volunteer.append(show_dict["CampID"])
        new_volunteer.append(json_preference)
        new_volunteer.append(1)
        for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "workShift"]:
            new_volunteer.append(preference[i])

        with db.connect('emergency_system.db') as conn:
            c = conn.cursor()
            sql = '''INSERT INTO volunteer 
            (fName, lName, username, password, campID, preference, accountStatus, 
            Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, workShift) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

            # status default 1 !!!!!!!!!!
            c.execute(sql, new_volunteer)
            conn.commit()
            time.sleep(0.8)
            vol_df = get_volunteer_schedule_df(conn, purpose="Display")
            vol_id = vol_df['volunteerID'].iloc[-1]
            print("\n"+u"\U0001F538"+f"New volunteer ID : [{vol_id}]\n")
            print(u'\u2705', "New volunteer account is successfully created!")

    def display_volunteer_account(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tDISPLAY VOLUNTEER ACCOUNT\n")
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1, "\n-->"):
                case 1:
                    self.display_account_byID()
                    back()
                case 2:
                    self.display_account_byCamp()
                    back()
                case 3:
                    self.display_all_account()
                    back()
                case 0:
                    return

    def display_account_byID(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tDISPLAY BY VOLUNTEER ID\n")
        ID = Get.option_in_list(get_all_IDs(
            'volunteer'), u"\U0001F539" + 'Enter the volunteer ID:')
        try:
            sch = ""
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                sch = get_volunteer_schedule_df(
                    conn, campID=0, volunteer_ID=ID, purpose="Display")
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                volunteerID = (?)''', (ID,))
            fd = pd.DataFrame(list(c.fetchall()),
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "CampID",
                                       "Account status"])
            if fd.empty:
                warn(f"\nThere is no account based on the volunteerID: {ID}")
            else:
                print(
                    f"\nPlease see the information about volunteer with ID {ID} below: \n")
                prCyan(u"\U0001F538"+"---GENERAL INFORMATION---\n")
                print_table(fd.columns, fd.to_numpy().tolist(),
                            (12, 20, 20, 18, 12, 15))
                print("\nStatus: 0 = Inactive\t1 = Active\n")
                prCyan("\n"+u"\U0001F538" +
                       "---VOLUNTEER AVAILABILITY SCHEDULE---\n")
                print_table(sch.columns, sch.to_numpy().tolist(),
                            (12, 15, 15, 15, 15, 18, 18, 18, 18, 18, 18, 18))
                print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
                      " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
        except IndexError:
            print_log("{} is an invalid ID".format(ID))

    def display_account_byCamp(self):
        ID = Get.option_in_list(get_all_IDs(
            'camp'), u"\U0001F539" + 'Enter the Camp ID:')
        try:
            sch = []
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                sch = get_volunteer_schedule_df(
                    conn, campID=ID, volunteer_ID=0, purpose="Display")
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                        campID = (?)''', (ID,))
            fd = pd.DataFrame(list(c.fetchall()),
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp ID",
                                       "Account status"])
            if fd.empty:
                print(f"There is no account based in the camp {ID}.")
            else:
                print(
                    f"Please see the information about volunteers in camp ID {ID} below: \n")
                prCyan(u"\U0001F538"+"---GENERAL INFORMATION---\n")
                print_table(fd.columns, fd.to_numpy().tolist(),
                            (12, 20, 20, 18, 12, 15))
                print("\nStatus: 0 = Inactive\t1 = Active\n")
                prCyan("\n"+u"\U0001F538" +
                       "---VOLUNTEER AVAILABILITY SCHEDULE---\n")
                print_table(sch.columns, sch.to_numpy().tolist(),
                            (12, 15, 15, 15, 15, 18, 18, 18, 18, 18, 18, 18))
                print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
                      " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
        except:
            print_log("Wrong connection to the database.")

    def display_all_account(self):
        try:
            sch = []
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                sch = get_volunteer_schedule_df(
                    conn, campID=0, volunteer_ID=0, purpose="Display")
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                                1''')
            fd = pd.DataFrame(list(c.fetchall()),
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp ID",
                                       "Account status"])
            if fd.empty:
                print(
                    f"There is no volunteer account in the system! Recruit some volunteers please.")
            else:
                print("Please see all volunteers information below: \n")
                prCyan(u"\U0001F538"+"---GENERAL INFORMATION---\n")
                print_table(fd.columns, fd.to_numpy().tolist(),
                            (12, 20, 20, 18, 12, 15))
                print("\nStatus: 0 = Inactive\t1 = Active\n")
                prCyan("\n"+u"\U0001F538" +
                       "---VOLUNTEER AVAILABILITY SCHEDULE---\n")
                print_table(sch.columns, sch.to_numpy().tolist(),
                            (12, 15, 15, 15, 15, 18, 18, 18, 18, 18, 18, 18))
                print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
                      " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
        except:
            print_log("Wrong connection to the database")

    def delete_account(self):
        print("--------------------------------------------------------------------------")
        prLightPurple("\t\t\tDELETE VOLUNTEER ACCOUNT\n")
        print(u"\U0001F531" +
              "Please see volunteer details below for your information: \n")
        conn1 = connect_db()
        vol_df = get_volunteer_schedule_df(conn1, purpose="Status")
        print_table(vol_df.columns, vol_df.to_numpy().tolist(),
                    (25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35))
        print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
              " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
        ID = Get.int(
            u"\U0001F539"+'Enter the volunteer ID you would like to delete:')
        print("\n")
        try:
            with db.connect('emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus, password FROM volunteer 
                            WHERE volunteerID = (?)''', (ID,))
                a = c.fetchall()
                if a != []:
                    fd = pd.DataFrame([a[0][:-1]],
                                      columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp ID",
                                               "Account status"])
                    print_table(fd.columns, fd.to_numpy().tolist(),
                                (12, 20, 20, 20, 15, 18))
                    confirm = AccountCreation.confirm_deletion()
                    if confirm == 1:
                        day_col = list(vol_df.columns[6:])
                        vol_df_byID = vol_df.loc[vol_df["volunteerID"] == ID, :]
                        has_req = False
                        for d in day_col:
                            for ind in vol_df_byID.index:
                                if vol_df_byID[d][ind] == u"\U0001F4D1":
                                    has_req = True

                        if has_req == False:
                            c = conn.cursor()
                            sql = '''DELETE FROM volunteer WHERE volunteerID = (?)'''
                            c.execute(sql, (ID,))
                            conn.commit()
                            c.execute(f"insert into deleted_vol_account (volunteerID, username, password)"
                                      f"values({ID}, '{a[0][3]}', '{a[0][-1]}') ")
                            print(u'\u2705'+'The account is successfully deleted.')
                        else:
                            print("\n")
                            print_table(vol_df_byID.columns, vol_df_byID.to_numpy().tolist(
                            ), (25, 25, 25, 25, 25, 25, 35, 35, 35, 35, 35, 35, 35))
                            print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
                                  " = Unavailable, "+u"\U0001F4D1"+" = Booked \n")
                            warn(
                                "You cannot delete this volunteer account because there is still a task request from the refugee.")
                            return
                else:
                    raise IndexError

        except IndexError:
            print_log(
                "The ID you entered does not exist, you can view all accounts first")
