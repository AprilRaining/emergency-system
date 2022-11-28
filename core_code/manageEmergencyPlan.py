import pandas as pd

from myfunctionlib import *
from planInput import *


class ManageEmergencyPlan:

    def __init__(self):
        """
        Read from file.
        """
        self.menu = menu(self.__class__.__name__)

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    self.create_emergency_plan()
                case 2:
                    self.edit_emergency_plan()
                case 3:
                    self.display_all_emergency_plans()
                    back()
                case 4:
                    self.close_or_open_emergency_plan()
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
        plan['endDate'] = PlanInput.end_date(plan['startDate'])
        plan['numberOfCamps'] = PlanInput.number_of_camps()
        plan['status'] = 0 if plan['startDate'] > datetime.date.today() else 1
        plan['priority'] = PlanInput.priority()
        self.insert_one_plan(plan)
        back('Succeed!')

    def edit_emergency_plan(self):
        if not self.display_all_emergency_plans():
            back()
            return
        planID = self.select_one_plan()
        df = self.read_plans(planID)
        self.display_emergency_plans(planID)
        match df.loc[0, 'status']:
            case 0:
                options = Options([
                    'type',
                    'description',
                    'area',
                    'startDate',
                    'endDate',
                    'numberOfCamps',
                    'priority'
                ], limied=True)
                print('This plan has not been opened.\n'
                      'Please choose one of properties below you want to change.')
            case 1:
                options = Options([
                    'description',
                    'endDate',
                    'priority'
                ], limied=True)
                print('This plan has been opened.\n'
                      'Please choose one of properties below you want to change.')
            case 2:
                back('This plan has been closed, you can not change it.')
                return
        print(options)
        option = options.get_option('Please choose which one you want to edit: ')
        newValue = self.get_new_value(planID, options.values[option])
        self.update_new_value(planID=planID, column=options.values[option], newValue=newValue)
        back('Succeed!')

    def get_new_value(self, planID, column):
        df = self.read_plans(planID)
        print('Please input a new value.')
        match column:
            case 'type':
                return PlanInput.type()
            case 'description':
                return PlanInput.description()
            case 'area':
                return PlanInput.area()
            case 'startDate':
                return PlanInput.start_date()
            case 'endDate':
                return PlanInput.end_date(df.loc[0, 'startDate'])
            case 'numberOfCamps':
                return PlanInput.number_of_camps()
            case 'priority':
                return PlanInput.priority()

    def update_new_value(self, planID, column, newValue):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            c = conn.cursor()
            c.execute("update plan set {} = '{}' where planID = {}"
                      .format(column, newValue, planID))

    def display_all_emergency_plans(self):
        df = self.read_all_plans().to_string(index=False)
        if len(df) != 0:
            print(df)
            return True
        else:
            print('There is not any plan. Please create one first.')
            return False

    def close_or_open_emergency_plan(self):
        if not self.display_all_emergency_plans():
            back()
            return
        planID = self.select_one_plan()
        df = self.read_plans(planID)
        match df.loc[0, 'status']:
            case 0:
                if confirm('This plan is waiting for open\n'
                           'Do you want to open it now?\n'
                           'The start date will be set to today if you want to open it.'):
                    self.update_new_value(planID, 'status', 1)
                    self.update_new_value(planID, 'startDate', datetime.date.today())
                    back('Succeed!')
                    return
            case 1:
                if confirm('This plan is opened\n'
                           'Do you want to close it now?\n'
                           'The end date will be set to today if you want to open it.'):
                    self.update_new_value(planID, 'status', 2)
                    self.update_new_value(planID, 'endDate', datetime.date.today())
                    back('Succeed!')
                    return
            case 2:
                back('This plan has been closed, you can not change it.')
                return

    def delete_emergency_plan(self):
        if not self.display_all_emergency_plans():
            back()
            return
        planID = self.select_one_plan()
        df = self.read_plans(planID)
        if confirm('Once you delete this plan you can not find it anymore.'):
            self.delete_plans(planID)
            back('Succeed!')

    def search_one_plan(self):
        options = Options([
            'type',
            'description',
            'area',
            'startDate',
            'endDate',
            'numberOfCamps',
            'status',
            'priority'
        ], limied=True)
        print(options)
        option = options.get_option('Please choose which one you want to search by: ')
        keyword = input('Please input the keyword:')
        planIDs = search('plan', options.values[option], keyword)
        return planIDs

    def select_one_plan(self):
        print('Can not find the Plan?\n'
              'Input 0 to use search function to help you find the PlanID')
        planID = Get.option_in_range(self.get_max_planID() + 1,
                                     'Please input choose planID: ')
        if planID == 0:
            planIDs = self.search_one_plan()
            self.display_emergency_plans(planIDs)
            planID = Get.option_in_list(planIDs, 'Please input choose planID: ')
        return planID

    def display_emergency_plans(self, index):
        print(self.read_plans(index).to_string(index=False))

    def insert_one_plan(self, plan):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            c = conn.cursor()
            maxPlanID = c.execute('select max(planID) from plan').fetchone()[0]
            seqPlan = 0 if maxPlanID is None else maxPlanID
            c.execute("update sqlite_sequence set seq = {} where name = 'plan'".format(seqPlan))
            if plan['endDate'] is None:
                c.execute(
                    '''insert into 
                    plan (type, description, area, startDate, endDate, numberOfCamps, status, priority) 
                    values ('{}','{}','{}','{}',null,'{}','{}','{}')'''.format(
                        plan['type'],
                        plan['description'],
                        plan['area'],
                        plan['startDate'],
                        plan['numberOfCamps'],
                        plan['status'],
                        plan['priority']
                    ))
            else:
                c.execute(
                    '''insert into 
                    plan (type, description, area, startDate, endDate, numberOfCamps, status, priority) 
                    values ('{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                        plan['type'],
                        plan['description'],
                        plan['area'],
                        plan['startDate'],
                        plan['endDate'],
                        plan['numberOfCamps'],
                        plan['status'],
                        plan['priority']
                    ))
            maxCampID = c.execute('select max(campID) from camp').fetchone()[0]
            seqCamp = 0 if maxCampID is None else maxCampID
            c.execute("update sqlite_sequence set seq = {} where name = 'camp'".format(seqCamp))
            for i in range(plan['numberOfCamps']):
                c.execute('insert into camp (capacity, planID) values (20, {})'.format(seqPlan + 1))
            return seqPlan + 1

    def read_all_plans(self):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            return pd.read_sql_query('select * from plan', conn)

    def read_plans(self, index):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            return pd.read_sql_query('select * from plan where planID in {}'
                                     .format(list_to_sqlite_string(index)), conn)

    def delete_plans(self, index):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            c = conn.cursor()
            c.execute('delete from plan where planID in {}'
                      .format(list_to_sqlite_string(index)))
            c.execute('delete from camp where planID in {}'
                      .format(list_to_sqlite_string(index)))

    def get_max_planID(self):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            c = conn.cursor()
            return c.execute('select max(planID) from plan').fetchone()[0]
