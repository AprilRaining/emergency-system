import json

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
        pass

    def deactive_volunteer_account(self):
        pass

    def creat_a_volunteer_account(self):
        new_volunteer = []

        fname = input('Enter the first name:')
        lname = input('Enter the last name:')
        username = AccountCreation.get_username()
        password = input('Enter the password:')
        campID = AccountCreation.get_camp_id()

        preference = AccountCreation.preference_default()
        preference['Monday'] = AccountCreation.get_work_day('Monday')
        preference['Tuesday'] = AccountCreation.get_work_day('Tuesday')
        preference['Wednesday'] = AccountCreation.get_work_day('Wednesday')
        preference['Thursday'] = AccountCreation.get_work_day('Thursday')
        preference['Friday'] = AccountCreation.get_work_day('Friday')
        preference['Saturday'] = AccountCreation.get_work_day('Saturday')
        preference['Sunday'] = AccountCreation.get_work_day('Sunday')
        preference['workShift'] = AccountCreation.get_work_shift()
        json_preference = json.dumps(preference)

        new_volunteer.append(fname)
        new_volunteer.append(lname)
        new_volunteer.append(username)
        new_volunteer.append(password)
        new_volunteer.append(campID)
        new_volunteer.append(json_preference)

        print(new_volunteer)
        with db.connect('emergency_system.db') as conn:
            c = conn.cursor()
            sql = '''INSERT INTO volunteer 
            (fName, lName, username, password, campID, preference, accountStatus) VALUES (?, ?, ?, ?, ?, ?, 1)'''

            # status default 1 !!!!!!!!!!
            c.execute(sql, new_volunteer)

    def display_volunteer_account(self):
        pass
