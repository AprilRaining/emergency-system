import json
from get import Get
import pandas as pd
from manageEmergencyPlan import *
from accountInput import *
import sqlite3 as db


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
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    manage_emergency_plan = ManageEmergencyPlan()
                    manage_emergency_plan.sub_main()
                case 2:
                    self.manage_account()
                case 0:
                    return

    def manage_account(self):
        while True:
            print("\nChoose the number of operation you want to do:")
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.reactive_volunteer_account()
                case 2:
                    self.deactive_volunteer_account()
                case 3:
                    self.creat_a_volunteer_account()
                case 4:
                    self.display_volunteer_account()
                case 0:
                    return

    def reactive_volunteer_account(self):
        ID = Get.int('Enter the volunteer ID:')
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT accountStatus FROM volunteer WHERE volunteerID = (?)''', (ID, ))
                status = c.fetchall()[0][0]
            if status == 1:
                print("This account is already active.")
                print("-------------------------------------")
            else:
                c.execute(f'''UPDATE volunteer SET accountStatus = 1 WHERE volunteerID = (?)''', (ID, ))
                conn.commit()
                print("Volunteer {}'s account is now reactive".format(ID))
        except IndexError:
            print("{} is an invalid ID".format(ID))
        except:
            print("Wrong connection to the database.")


    def deactive_volunteer_account(self):
        ID = Get.int('Enter the volunteer ID:')
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT accountStatus FROM volunteer WHERE volunteerID = (?)''', (ID,))
                status = c.fetchall()[0][0]
            if status == 0:
                print("This account is already deactive.")
                print("-------------------------------------")
            else:
                c.execute(f'''UPDATE volunteer SET accountStatus = 0 WHERE volunteerID = (?)''', (ID,))
                conn.commit()
                print("Volunteer {}'s account is now deactive".format(ID))
        except IndexError:
            print("{} is an invalid ID".format(ID))
        except:
            print("Wrong connection to the database.")

    def creat_a_volunteer_account(self):
        new_volunteer = []

        fname = input('Enter the first name:')
        lname = input('Enter the last name:')
        username = AccountCreation.get_username()
        password = input('Enter the password:')
        campID = AccountCreation.get_camp_id()


        # preference = AccountCreation.preference_default()
        # preference['Monday'] = AccountCreation.get_work_day('Monday')
        # preference['Tuesday'] = AccountCreation.get_work_day('Tuesday')
        # preference['Wednesday'] = AccountCreation.get_work_day('Wednesday')
        # preference['Thursday'] = AccountCreation.get_work_day('Thursday')
        # preference['Friday'] = AccountCreation.get_work_day('Friday')
        # preference['Saturday'] = AccountCreation.get_work_day('Saturday')
        # preference['Sunday'] = AccountCreation.get_work_day('Sunday')

        preference = AccountCreation.get_week_preference()
        workshift = AccountCreation.get_work_shift()

        show_dict = {"first name": fname, "last name": lname, "username": username, "password": password,
                     "campID": campID, "preference": preference, "workshift": workshift}
        while True:
            print("\nThis is the new account's information(In preference, 0 means available, -1 means not available):")
            for key, value in show_dict.items():
                print(key, ': ', value)
            check = input("If the information is right, please press Y/y, or N/n to correct:\n")
            if check == "Y" or check == "y":
                break
            elif check == "N" or check == "n":
                while True:
                    print("Please input what you want to correct from this list:")
                    for i in show_dict.keys():
                        print(i)
                    input_second = input()
                    if input_second in show_dict.keys():
                        if input_second == "first name":
                            show_dict["first name"] = input('Enter the first name:')
                        elif input_second == "last name":
                            show_dict["last name"] = input('Enter the last name:')
                        elif input_second == "username":
                            show_dict["username"] = AccountCreation.get_username()
                        elif input_second == "password":
                            show_dict["password"] = input('Enter the password:')
                        elif input_second == "campID":
                            show_dict["campID"] = AccountCreation.get_camp_id()
                        elif input_second == "preference":
                            show_dict["preference"] = AccountCreation.get_week_preference()
                        elif input_second == "workshift":
                            show_dict["workshift"] = AccountCreation.get_work_shift()
                        break
                    else:
                        print("Wrong Input.")
            else:
                print("Illegal input!. Please input Y/y or N/n:\n")

        preference = show_dict["preference"]
        preference["workShift"] = show_dict["workshift"]
        json_preference = json.dumps(preference)

        new_volunteer.append(show_dict["first name"])
        new_volunteer.append(show_dict["last name"])
        new_volunteer.append(show_dict["username"])
        new_volunteer.append(show_dict["password"])
        new_volunteer.append(show_dict["campID"])
        new_volunteer.append(json_preference)
        new_volunteer.append(1)
        for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "workShift"]:
            new_volunteer.append(preference[i])

        with db.connect('info_files/emergency_system.db') as conn:
            c = conn.cursor()
            sql = '''INSERT INTO volunteer 
            (fName, lName, username, password, campID, preference, accountStatus, 
            Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, workShift) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

            # status default 1 !!!!!!!!!!
            c.execute(sql, new_volunteer)
            conn.commit()
            print("Your account has been created!")

    def display_volunteer_account(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.display_account_byID()
                case 2:
                    self.display_account_byCamp()
                case 3:
                    self.display_all_account()
                case 0:
                    return

    def display_account_byID(self):
        ID = Get.int('Enter the volunteer ID:')
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                volunteerID = (?)''', (ID,))
            fd = pd.DataFrame(list(c.fetchall()), columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp iD", "Account status"])
            if fd.empty:
                print(f"There is no account based on the volunteerID: {ID}")
            else:
                print(f"The information about volunteer {ID} is below: \n", fd)
        except IndexError:
            print("{} is an invalid ID".format(ID))
        except:
            print("Wrong connection to the database.")

    def display_account_byCamp(self):
        ID = Get.int('Enter the Camp ID:')
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                        campID = (?)''', (ID,))
            fd = pd.DataFrame(list(c.fetchall()),
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp iD",
                                       "Account status"])
            if fd.empty:
                print(f"There is no account based in the camp {ID}.")
            else:
                print(f"Volunteers in camp {ID} are below: \n", fd)
        except:
            print("Wrong connection to the database.")

    def display_all_account(self):
        try:
            with db.connect('info_files/emergency_system.db') as conn:
                c = conn.cursor()
                c.execute(f'''SELECT volunteerID, fName, lName, username, campID, accountStatus FROM volunteer WHERE 
                                1''')
            fd = pd.DataFrame(list(c.fetchall()),
                              columns=["VolunteerID", "First Name", "Last Name", "Username", "Camp iD",
                                       "Account status"])
            if fd.empty:
                print(f"There is no volunteer account in the system! Recruit some volunteers please.")
            else:
                print("All volunteers are here: \n", fd)
        except:
            print("Wrong connection to the database")
