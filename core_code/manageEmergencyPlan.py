from myfunctionlib import *
from planInput import *
from sqliteFunctions import *


class ManageEmergencyPlan:

    def __init__(self):
        self.menu = menu(self.__class__.__name__)
        self.sqlitePath = '../info_files/emergency_system.db'

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    self.create_emergency_plan()
                    back()
                case 2:
                    self.edit_emergency_plan(self.select_one_plan())
                    back()
                case 3:
                    display_by_IDs('plan', get_all_IDs('plan'))
                    back()
                case 4:
                    self.close_or_open_emergency_plan(self.select_one_plan())
                    back()
                case 5:
                    self.delete_emergency_plan(self.select_one_plan())
                    back()
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
        print('Succeed!')

    def edit_emergency_plan(self, planID):
        df = pd_read_by_IDs('plan', planID)
        display_by_IDs('plan', planID)
        options = []
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
                ], limited=True)
                print('This plan has not been opened.\n'
                      'Please choose one of properties below you want to change.')
            case 1:
                options = Options([
                    'description',
                    'endDate',
                    'priority'
                ], limited=True)
                print('This plan has been opened.\n'
                      'Please choose one of properties below you want to change.')
            case 2:
                print('This plan has been closed, you can not change it.')
                return
        print(options)
        option = options.get_option(
            'Please choose which one you want to edit: ')
        newValue = self.get_new_value(planID, options.values[option])
        self.update_new_value(
            planID=planID, column=options.values[option], newValue=newValue)
        print('Succeed!')

    def get_new_value(self, planID, column):
        df = pd_read_by_IDs('plan', planID)
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

    def close_or_open_emergency_plan(self, planID):
        df = pd_read_by_IDs('plan', planID)
        match df.loc[0, 'status']:
            case 0:
                if confirm('This plan is waiting for open\n'
                           'Do you want to open it now?\n'
                           'The start date will be set to today if you want to open it.'):
                    self.update_new_value(planID, 'status', 1)
                    self.update_new_value(
                        planID, 'startDate', datetime.date.today())
                    print('Succeed!')
                    return
            case 1:
                campIDs = get_linked_IDs('camp', 'plan', planID)
                volunteerIDs = get_linked_IDs('volunteer', 'camp', campIDs)
                refugeeIDs = get_linked_IDs('refugee', 'camp', campIDs)
                if refugeeIDs:
                    print('There are refugees in this plan\n'
                          'Please make sure no refugees in the plan before close it.')
                    return
                else:
                    if volunteerIDs:
                        print('There are volunteers in this plan, close it will move away those volunteers.')
                        with sqlite3.connect('../info_files/emergency_system.db') as conn:
                            c = conn.cursor()
                            c.execute(
                                f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                if confirm('This plan is opened\n'
                           'Do you want to close it now?\n'
                           'The end date will be set to today if you want to open it.'):
                    delete_by_IDs('camp', campIDs)
                    self.update_new_value(planID, 'status', 2)
                    self.update_new_value(
                        planID, 'endDate', datetime.date.today())
                    print('Succeed!')
                    return
            case 2:
                print('This plan has been closed, you can not change it.')
                return

    def delete_emergency_plan(self, planID):
        campIDs = get_linked_IDs('camp', 'plan', planID)
        volunteerIDs = get_linked_IDs('volunteer', 'camp', campIDs)
        refugeeIDs = get_linked_IDs('refugee', 'camp', campIDs)
        if refugeeIDs:
            print('There are refugees in this plan\n'
                  'Please make sure no refugees in the plan before remove it.')
            return
        else:
            if confirm('Once you delete this plan you can not find it anymore.'):
                if volunteerIDs:
                    print('There are volunteers in this plan, close it will move away those volunteers.')
                    with sqlite3.connect('../info_files/emergency_system.db') as conn:
                        c = conn.cursor()
                        c.execute(
                            f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                delete_by_IDs('camp', campIDs)
                delete_by_IDs('plan', planID)
            print('Succeed!')

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
        ], limited=True)
        print(options)
        option = options.get_option(
            'Please choose which one you want to search by: ')
        keyword = input('Please input the keyword:')
        planIDs = search('plan', options.values[option], keyword)
        return planIDs

    def select_one_plan(self):
        planIDs = get_all_IDs('plan')
        while True:
            display_by_IDs('plan', planIDs)
            print('Input 0 to search')
            planIDs.append(0)
            planID = Get.option_in_list(planIDs, 'Please input the planID to choose a plan: ')
            if planID == 0:
                planIDs = self.search_one_plan()
            else:
                return planID

    def insert_one_plan(self, plan):
        with sqlite3.connect('../info_files/emergency_system.db') as conn:
            c = conn.cursor()
            maxPlanID = c.execute('select max(planID) from plan').fetchone()[0]
            seqPlan = 0 if maxPlanID is None else maxPlanID
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'plan'".format(seqPlan))
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
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'camp'".format(seqCamp))
            for i in range(plan['numberOfCamps']):
                c.execute(
                    'insert into camp (capacity, planID) values (20, {})'.format(seqPlan + 1))
            return seqPlan + 1
