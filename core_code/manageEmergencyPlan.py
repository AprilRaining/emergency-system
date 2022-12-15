import os
import sys

from TableDisplayer import *
from planInput import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Emergency_Plan.emergency_plan_sql import emergency_plan


class ManageEmergencyPlan:

    def __init__(self):
        self.menu = menu(self.__class__.__name__)

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    # self.create_emergency_plan()
                    create = emergency_plan.Create_Emergency_Plan()
                    create.add()
                    back()
                case 2:
                    self.edit_emergency_plan(select_sqlite('plan', get_all_IDs('plan')))
                    back()
                case 3:
                    self.view_plans(get_all_IDs('plan'))
                    back()
                case 4:
                    self.close_or_open_emergency_plan(select_sqlite('plan', get_all_IDs('plan')))
                    back()
                case 5:
                    # self.delete_emergency_plan(select_sqlite('plan'))
                    delete = emergency_plan.Delete_Emergency_Plan()
                    delete.delete_now()
                    # back()
                case 0:
                    return

    def create_emergency_plan(self):
        plan = dict()
        plan['type'] = PlanInput.type()
        plan['description'] = PlanInput.description()
        plan['area'] = PlanInput.area()
        plan['startDate'] = PlanInput.start_date()
        plan['endDate'] = PlanInput.end_date(to_date(plan['startDate']))
        plan['status'] = 0 if plan['startDate'] > datetime.date.today() else 1
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
                ], limited=True)
                print('This plan has not been opened.\n'
                      'Please choose one of properties below you want to change.')
            case 1:
                options = Options([
                    'description',
                    'endDate',
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

    @staticmethod
    def get_new_value(planID, column):
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
                return PlanInput.start_date_update()
            case 'endDate':
                return PlanInput.end_date_update(to_date(df.loc[0, 'startDate']))
            case 'numberOfCamps':
                return PlanInput.number_of_camps()

    @staticmethod
    def update_new_value(planID, column, newValue):
        with sqlite3.connect('info_files/emergency_system.db') as conn:
            c = conn.cursor()
            match column:
                case 'numberOfCamps':
                    campIDs = get_linked_IDs('camp', 'plan', planID)
                    oldValue = len(campIDs)
                    if (newValue < oldValue):
                        pass
            c.execute("update plan set {} = '{}' where planID = {}"
                      .format(column, newValue, planID))
            conn.commit()

    def view_plans(self, planIDs):
        TableDisplayer.plan(planIDs)
        self.select_in_camp_from(self.select_in_plan_from(planIDs))

    def close_or_open_emergency_plan(self, planID):
        df = pd_read_by_IDs('plan', planID)
        match df.loc[0, 'status']:
            case 0:
                if confirm('This plan is waiting for open\n'
                           'Do you want to open it now?\n'
                           'The start date will be set to today if you want to open it.'):
                    numberOfCamps = PlanInput.number_of_camps()
                    self.update_new_value(planID, 'numberOfCamps', numberOfCamps)
                    self.assign_campIDs_to_plan(planID, numberOfCamps)
                    self.update_new_value(planID, 'status', 1)
                    self.update_new_value(planID, 'startDate', datetime.date.today())
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
                        print(
                            'There are volunteers in this plan, close it will move away those volunteers.')
                        with sqlite3.connect('info_files/emergency_system.db') as conn:
                            c = conn.cursor()
                            c.execute(
                                f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                            conn.commit()
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

    @staticmethod
    def delete_emergency_plan(planID):
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
                    print(
                        'There are volunteers in this plan, close it will move away those volunteers.')
                    with sqlite3.connect('info_files/emergency_system.db') as conn:
                        c = conn.cursor()
                        c.execute(
                            f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                        conn.commit()
                delete_by_IDs('camp', campIDs)
                delete_by_IDs('plan', planID)
            print('Succeed!')

    @staticmethod
    def insert_one_plan(plan):
        with sqlite3.connect('info_files/emergency_system.db') as conn:
            c = conn.cursor()
            maxPlanID = c.execute('select max(planID) from plan').fetchone()[0]
            seqPlan = 0 if maxPlanID is None else maxPlanID
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'plan'".format(seqPlan))
            conn.commit()
            if plan['endDate'] is None:
                c.execute(
                    f'''insert into 
                    plan (type, description, area, startDate, endDate, numberOfCamps, status) 
                    values ('{plan['type']}','{plan['description']}','{plan['area']}','{plan['startDate']}',null,null,'{plan['status']}')'''
                )
                conn.commit()
            else:
                c.execute(
                    f'''insert into 
                    plan (type, description, area, startDate, endDate, numberOfCamps, status) 
                    values ('{plan['type']}','{plan['description']}','{plan['area']}','{plan['startDate']}','{plan['endDate']}',null,'{plan['status']}')'''
                )
                conn.commit()
            maxCampID = c.execute('select max(campID) from camp').fetchone()[0]
            seqCamp = 0 if maxCampID is None else maxCampID
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'camp'".format(seqCamp))
            conn.commit()
            return seqPlan + 1

    @staticmethod
    def select_in_plan_from(planIDs):
        if planIDs:
            return
        else:
            while True:
                option = input(f"Input a plan ID to view more detail or 'q' to quit:")
                if option != 'q':
                    try:
                        option = int(option)
                    except ValueError:
                        print("Please reenter a valid value.")
                    else:
                        if option not in planIDs:
                            print(f'{option} is not a valid input. Please try again.')
                        else:
                            campIDs = get_linked_IDs('camp', 'plan', option)
                            if campIDs:
                                TableDisplayer.camp(campIDs)
                                return campIDs
                            else:
                                print('No camps under this plan.')
                                return False
                else:
                    return False

    @staticmethod
    def select_in_camp_from(campIDs):
        if campIDs:
            return
        else:
            while True:
                option = input(f"Input a camp ID to view more detail or 'q' to quit:")
                if option != 'q':
                    try:
                        option = int(option)
                    except ValueError:
                        print("Please reenter a valid value.")
                    else:
                        if option not in campIDs:
                            print(f'{option} is not a valid input. Please try again.')
                        else:
                            volunteerIDs = get_linked_IDs('volunteer', 'camp', option)
                            refugeeIDs = get_linked_IDs('refugee', 'camp', option)
                            if volunteerIDs:
                                print("Volunteers in this camps:")
                                display_by_IDs('volunteer', volunteerIDs)
                                print('')
                            else:
                                print('No volunteer in this camp')
                            if refugeeIDs:
                                print("Refugees in this camps:")
                                display_by_IDs('refugee', refugeeIDs)
                                print('')
                            else:
                                print('No refugee in this camp')
                            return
                else:
                    return

    @staticmethod
    def assign_campIDs_to_plan(planID, numberOfCamps):
        with sqlite3.connect('info_files/emergency_system.db') as conn:
            c = conn.cursor()
            for i in range(numberOfCamps):
                c.execute(f'insert into camp (capacity, planID) values (20, {planID})')
                conn.commit()
