from sqliteFunctions import *


class TableDisplayer():

    @staticmethod
    def match(table):
        match table:
            case 'plan':
                return TableDisplayer.plan
            case 'camp':
                return TableDisplayer.camp
            case 'volunteer':
                return TableDisplayer.volunteer
            case 'refugee':
                return TableDisplayer.refugee

    @staticmethod
    def plan(planIDs):
        if not planIDs:
            warn('No reasult!')
            return
        planIDs = TableDisplayer.unifiy_type(planIDs)
        df = pd_read_by_IDs('plan', planIDs)
        numberOfVolunteers = []
        numberOfRefugees = []
        for planID in planIDs:
            campIDs = get_linked_IDs('camp', 'plan', planID)
            volunteerIDs = get_linked_IDs('volunteer', 'camp', campIDs)
            numberOfVolunteers.append(len(volunteerIDs))
            refugeeIDs = get_linked_IDs('refugee', 'camp', campIDs)
            numberOfRefugees.append(len(refugeeIDs))
        df['numberOfVolunteers'] = numberOfVolunteers
        df['numberOfRefugees'] = numberOfRefugees
        df['status'] = df.apply(
            lambda a: TableDisplayer.to_string_plan_status(a), axis=1)
        print_table(df.columns, df.to_numpy().tolist(),
                    (30, 50, 80, 60, 60, 60, 70, 40, 80, 80))

    @staticmethod
    def camp(campIDs):
        if not campIDs:
            warn('No reasult!')
            return
        campIDs = TableDisplayer.unifiy_type(campIDs)
        df = pd_read_by_IDs('camp', campIDs)
        numberOfVolunteers = []
        numberOfRefugees = []
        for campID in campIDs:
            volunteerIDs = get_linked_IDs('volunteer', 'camp', campID)
            numberOfVolunteers.append(len(volunteerIDs))
            refugeeIDs = get_linked_IDs('refugee', 'camp', campID)
            numberOfRefugees.append(len(refugeeIDs))
        df['numberOfVolunteers'] = numberOfVolunteers
        df['numberOfRefugees'] = numberOfRefugees
        print_table(df.columns, df.to_numpy().tolist(), (30, 30, 30, 70, 70))

    @staticmethod
    def volunteer(volunteerIDs):
        if not volunteerIDs:
            warn('No reasult!')
            return
        volunteerIDs = TableDisplayer.unifiy_type(volunteerIDs)
        df = pd_read_by_IDs('volunteer', volunteerIDs)
        df['accountStatus'] = df['accountStatus'].map(
            {0: 'Inactive', 1: 'Active'})
        df['Monday'] = df['Monday'].map(TableDisplayer.to_string_work_schedule)
        df['Tuesday'] = df['Tuesday'].map(
            TableDisplayer.to_string_work_schedule)
        df['Wednesday'] = df['Wednesday'].map(
            TableDisplayer.to_string_work_schedule)
        df['Thursday'] = df['Thursday'].map(
            TableDisplayer.to_string_work_schedule)
        df['Friday'] = df['Friday'].map(TableDisplayer.to_string_work_schedule)
        df['Saturday'] = df['Saturday'].map(
            TableDisplayer.to_string_work_schedule)
        df['Sunday'] = df['Sunday'].map(TableDisplayer.to_string_work_schedule)
        del df['preference']
        print_table(df.columns, df.to_numpy().tolist(), (18, 25, 25, 25, 25, 20, 16, 20,
                                                         30, 30, 30, 30, 30, 30, 30))
        print("\nNote:"+u"\U00002705"+" = Free, "+u"\U0000274C" +
              " = Unavailable,"+u"\U0001F4D1"+" = Booked \n")

    @staticmethod
    def refugee(refugeeIDs):
        if not refugeeIDs:
            warn('No reasult!')
            return
        refugeeIDs = TableDisplayer.unifiy_type(refugeeIDs)
        df = pd_read_by_IDs('refugee', refugeeIDs)
        print_table(df.columns, df.to_numpy().tolist(), (18, 16, 25, 25, 30, 25, 32, 70,
                                                         60, 70, 70, 60, 30, 30, 30, 25))

    @staticmethod
    def to_string_plan_status(df):
        match df['status']:
            case 0:
                return 'Unopened'
            case 1:
                return 'Opened'
            case 2:
                return 'Closed'

    def to_string_work_schedule(n):
        match n:
            case -1:
                return u"\U0000274C"
            case 0:
                return u"\U00002705"
        return u"\U0001F4D1"

    @staticmethod
    def unifiy_type(IDs):
        if type(IDs) == int:
            result = []
            result.append(IDs)
            return result
        else:
            return IDs
