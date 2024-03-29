import sys
from system_log import *
from emergency_plan_sql import emergency_plan
from planInput import *
from utilities import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ManageEmergencyPlan:

    def __init__(self):
        self.menu = menu(self.__class__.__name__)

    def sub_main(self):
        print("--------------------------------------------------------------------------")
        prPurple("\t\t\tEMERGENCY PLAN MANAGEMENT\n")
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1, "\n-->"):
                case 1:
                    print(
                        "--------------------------------------------------------------------------")
                    prLightPurple("\t\t\tCREATE EMERGENCY PLAN\n")
                    # self.create_emergency_plan()
                    create = emergency_plan.Create_Emergency_Plan()
                    create.add()
                    print("\n", u'\u2705',
                          'New emergency plan is successfully created.')
                    back()
                case 2:

                    print(
                        "--------------------------------------------------------------------------")
                    prLightPurple("\t\t\tEDIT EMERGENCY PLAN\n")
                    self.edit_emergency_plan(
                        select_sqlite('plan', get_all_IDs('plan')))
                    back()
                case 3:
                    print(
                        "--------------------------------------------------------------------------")
                    prLightPurple("\t\t\tVIEW EMERGENCY PLANS SUMMARY\n")
                    self.view_plans(get_all_IDs('plan'))
                case 4:
                    print(
                        "--------------------------------------------------------------------------")
                    prLightPurple("\t\t\tCLOSE or OPEN EMERGENCY PLAN\n")
                    self.close_or_open_emergency_plan(
                        select_sqlite('plan', get_all_IDs('plan')))
                    back()
                case 5:
                    print(
                        "--------------------------------------------------------------------------")
                    prLightPurple("\t\t\tDELETE EMERGENCY PLAN\n")
                    self.delete_emergency_plan(
                        select_sqlite('plan', get_all_IDs('plan')))
                    # delete = emergency_plan.Delete_Emergency_Plan()
                    # delete.delete_now()
                    back()
                case 0:
                    return

    def create_emergency_plan(self):
        plan = dict()
        plan['type'] = PlanInput.type()
        plan['description'] = PlanInput.description()
        plan['area'] = PlanInput.area()
        plan['startDate'] = PlanInput.start_date()
        plan['endDate'] = PlanInput.end_date(to_date(plan['startDate']))
        plan['numberOfCamps'] = PlanInput.number_of_camps()
        plan['status'] = 0 if plan['startDate'] > datetime.date.today() else 1
        self.insert_one_plan(plan)

    def edit_emergency_plan(self, planID):
        print("Please see the current emergency plan database below:\n")
        df = pd_read_by_IDs('plan', planID)
        TableDisplayer.plan(planID)
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
                print(
                    "\n" + u"\u2757" + 'This plan has not been opened yet. You could edit the properties below:\n')
            case 1:
                options = Options([
                    'description',
                    'endDate',
                ], limited=True)
                print(
                    "\n" + u"\u2757" + 'This plan has already been opened. You can only edit the properties below:\n')
            case 2:
                warn('This plan has been closed. You are not allowed edit it!')
                return
        print(options)
        option = options.get_option("\n" +
                                    u"\U0001F539" + 'Please choose one of properties above that you want to edit: ')
        newValue = self.get_new_value(planID, options.values[option])
        self.update_new_value(
            planID=planID, column=options.values[option], newValue=newValue)
        if options.values[option] == 'startDate':
            if newValue == datetime.date.today():
                self.update_new_value(
                    planID=planID, column='status', newValue=1)
        print('Succeed!')
        print("\n", u'\u2705', 'The emergency plan is successfully updated.')

    @staticmethod
    def get_new_value(planID, column):
        df = pd_read_by_IDs('plan', planID)
        print('\n---INPUT A NEW VALUE---')
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

    def update_new_value(self, planID, column, newValue):
        with sqlite3.connect('emergency_system.db') as conn:
            c = conn.cursor()
            match column:
                case 'numberOfCamps':
                    campIDs = get_linked_IDs('camp', 'plan', planID)
                    delete_by_IDs('camp', campIDs)
                    self.assign_campIDs_to_plan(planID, newValue)
            c.execute("update plan set {} = '{}' where planID = {}"
                      .format(column, newValue, planID))
            conn.commit()

    def view_plans(self, planIDs):
        print(u"\U0001F538" + "Please see emergency plan summary below: \n")
        select_info_from_camp(select_camps_from_plan(planIDs))
        print("\n")

    def close_or_open_emergency_plan(self, planID):
        df = pd_read_by_IDs('plan', planID)
        match df.loc[0, 'status']:
            case 0:
                if confirm('This plan is an unopened plan.\n'
                           u"\U0001F539" + 'Do you want to open it now?\n'
                                           u"\u2757" + 'Note: The start date will be set to today if you want to open it.'):
                    self.update_new_value(planID, 'status', 1)
                    self.update_new_value(
                        planID, 'startDate', datetime.date.today())
                    print('\nSucceed!')
                    print(u'\u2705' +
                          'This emergency plan is successfully opened.')
                    return
            case 1:
                campIDs = get_linked_IDs('camp', 'plan', planID)
                volunteerIDs = get_linked_IDs('volunteer', 'camp', campIDs)
                refugeeIDs = get_linked_IDs('refugee', 'camp', campIDs)
                if refugeeIDs:
                    warn('There are refugees in this plan\n'
                         'Please make sure no refugees in the plan before closing it.')
                    return
                else:
                    if volunteerIDs:
                        if confirm('There are volunteers in this plan, closing it will remove those volunteers.'):
                            with sqlite3.connect('emergency_system.db') as conn:
                                c = conn.cursor()
                                c.execute(
                                    f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                                conn.commit()
                                c.execute(
                                    f'update volunteer set accountStatus = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
                                conn.commit()
                        else:
                            return
                    delete_by_IDs('camp', campIDs)
                    self.update_new_value(planID, 'status', 2)
                    self.update_new_value(
                        planID, 'endDate', datetime.date.today())
                    print('Succeed!')
                    print(
                        u'\u2705', f"This plan ID: {planID} is successfully closed.")
                    return
            case 2:
                warn('This plan has been closed. You can not make any change to it.')
                return

    @staticmethod
    def delete_emergency_plan(planID):
        df = pd_read_by_IDs('plan', planID)
        match df.loc[0, 'status']:
            case 0:
                print('This plan has not been opened yet.')
                if confirm('Once you delete this plan, you will not be able to find it anymore.'):
                    campIDs = get_linked_IDs('camp', 'plan', planID)
                    delete_by_IDs('camp', campIDs)
                    delete_by_IDs('plan', planID)
                    print('Succeed!')
                    print(
                        u'\u2705'+f"The emergency plan ID: {planID} is successfully deleted.")
            case 1:
                warn('This plan is currently opened. You can not delete it!')
                print("You can only delete a closed plan.")
                print("Please close this plan first, before deleting it!")
            case 2:
                print('This plan is originally closed. You can delete it.')
                if confirm('Once you delete this plan, you will not be able to find it anymore.'):
                    delete_by_IDs('plan', planID)
                    print('Succeed!')
                    print(
                        u'\u2705'+f"The emergency plan ID: {planID} is successfully deleted.")

    def insert_one_plan(self, plan):
        with sqlite3.connect('emergency_system.db') as conn:
            c = conn.cursor()
            maxPlanID = c.execute('select max(planID) from plan').fetchone()[0]
            seqPlan = 0 if maxPlanID is None else maxPlanID
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'plan'".format(seqPlan))
            conn.commit()
            if plan['endDate'] is None:
                c.execute(
                    f'''insert into
                    plan (type, description, area, startDate,
                          endDate, numberOfCamps, status)
                    values ('{plan['type']}','{plan['description']}','{plan['area']}','{plan['startDate']}',null,{plan['numberOfCamps']},'{plan['status']}')'''
                )
                conn.commit()
            else:
                c.execute(
                    f'''insert into
                    plan (type, description, area, startDate,
                          endDate, numberOfCamps, status)
                    values ('{plan['type']}','{plan['description']}','{plan['area']}','{plan['startDate']}','{plan['endDate']}',{plan['numberOfCamps']},'{plan['status']}')'''
                )
                conn.commit()
            maxCampID = c.execute('select max(campID) from camp').fetchone()[0]
            seqCamp = 0 if maxCampID is None else maxCampID
            c.execute(
                "update sqlite_sequence set seq = {} where name = 'camp'".format(seqCamp))
            conn.commit()
            self.assign_campIDs_to_plan(seqPlan + 1, plan['numberOfCamps'])
            print(u"\U0001F538" + f"New Plan ID: {seqPlan + 1}")
            return seqPlan + 1

    @staticmethod
    def assign_campIDs_to_plan(planID, numberOfCamps):
        new_campID = []
        with sqlite3.connect('emergency_system.db') as conn:
            c = conn.cursor()
            campframe = pd.read_sql_query('SELECT * FROM camp', conn)
            campID_latest = int(campframe['campID'].iloc[-1]) + 1
            for i in range(numberOfCamps):
                new_campID.append(campID_latest + i)
                c.execute(
                    f'insert into camp (capacity, planID) values (20, {planID})')
                conn.commit()
        print("\n" + u"\U0001F538" +
              f"New Camp ID associated with new plan ID: {new_campID}")
