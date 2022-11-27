import sqlite3

import pandas as pd

from myfunctionlib import *
from planInput import *


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
            match option_get(self.menu.count('\n') + 1):
                case 1:
                    manage_emergency_plan = self.ManageEmergencyPlan()
                    manage_emergency_plan.sub_main()
                case 2:
                    self.manage_account()
                case 0:
                    return

    class ManageEmergencyPlan:

        def __init__(self):
            """
            Read from file.
            """
            self.menu = menu(self.__class__.__name__)

        def sub_main(self):
            while True:
                print(self.menu)
                match option_get(self.menu.count('\n') + 1):
                    case 1:
                        self.create_emergency_plan()
                    case 2:
                        self.edit_emergency_plan()
                    case 3:
                        self.display_all_emergency_plans()
                    case 4:
                        self.close_emergency_plan()
                    case 5:
                        self.delete_emergency_plan()
                    case 0:
                        return

        def create_emergency_plan(self):
            plan = dict()
            plan['type'] = PlanInput.type()
            plan['description'] = PlanInput.description()
            plan['area'] = PlanInput.area()
            plan['startDate'] = PlanInput.start_date()
            plan['closeDate'] = PlanInput.close_date(plan['startDate'])
            plan['numberOfCamps'] = PlanInput.number_of_camps()
            plan['status'] = False if plan['startDate'] > datetime.date.today() else True
            plan['priority'] = PlanInput.priority()
            print(plan)
            self.insert_one_plan(plan)
            back()

        def edit_emergency_plan(self):
            self.display_all_emergency_plans()
            option = Get.int('Please input the planID of the plan you want to change: ')
            self.display_one_emergency_plan()

        def display_all_emergency_plans(self):
            print(self.read_all_plans().to_string(index=False))
            back()

        def close_emergency_plan(self):
            pass

        def delete_emergency_plan(self):
            pass

        def display_one_emergency_plan(self, index):
            print(self.read_one_plan(index))

        def insert_one_plan(self, plan):
            with sqlite3.connect('../info_files/emergency_system.db') as conn:
                c = conn.cursor()
                maxPlanID = c.execute('select max(planID) from plan').fetchone()[0]
                if maxPlanID:
                    c.execute("update sqlite_sequence set seq = {} where name = 'plan'".format(maxPlanID))
                else:
                    c.execute(
                        "update sqlite_sequence set seq = 0 where name = 'plan'")
                c.execute(
                    '''insert into 
                    plan (type, description, area, startDate, endDate, numberOfCamps, status, priority) 
                    values ('{}','{}','{}','{}',{},'{}','{}','{}')'''.format(
                        plan['type'],
                        plan['description'],
                        plan['area'],
                        plan['startDate'],
                        plan['closeDate'],
                        plan['numberOfCamps'],
                        plan['status'],
                        plan['priority']
                    ))

        def read_all_plans(self):
            with sqlite3.connect('../info_files/emergency_system.db') as conn:
                return pd.read_sql_query('select * from plan', conn)

        def read_one_plan(self, index):
            with sqlite3.connect('../info_files/emergency_system.db') as conn:
                return pd.read_sql_query('select * from plan where planID = {}'.format(index))

    def manage_account(self):
        while True:
            print(menu())
            match option_get(menu().count('\n') + 1):
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
        pass

    def display_volunteer_account(self):
        pass
