from sqliteFunctions import *


class TableDisplayer():

    @staticmethod
    def match(table):
        match table:
            case 'plan':
                return TableDisplayer.plan
            case 'camp':
                return TableDisplayer.camp

    @staticmethod
    def plan(planIDs):
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
        df['status'] = df.apply(lambda a: TableDisplayer.to_string_plan_status(a), axis=1)
        print_table(df.columns, df.to_numpy().tolist(), (30, 50, 80, 60, 60, 60, 70, 40, 80, 80))

    @staticmethod
    def camp(campIDs):
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
    def volunteers(volunteerIDs):
        volunteerIDs = TableDisplayer.unifiy_type(volunteerIDs)
        df = pd_read_by_IDs('volunteer', volunteerIDs)
        df['accountStatus'] = df['accountStatus'].map({0: 'Inactive', 1: 'Active'})
        workdayDict = {-1: u"\U0000274C", 0: u"\U00002705"}
        df['Monday'] = df['Monday'].map(workdayDict)
        df['Tuesday'] = df['Tuesday'].map(workdayDict)
        df['Wednesday'] = df['Wednesday'].map(workdayDict)
        df['Thursday'] = df['Thursday'].map(workdayDict)
        df['Friday'] = df['Friday'].map(workdayDict)
        df['Saturday'] = df['Saturday'].map(workdayDict)
        df['Sunday'] = df['Sunday'].map(workdayDict)
        del df['preference']
        print_table(df.columns, df.to_numpy().tolist(), (18, 25, 25, 25, 25, 20, 16, 20,
                                                         30, 30, 30, 30, 30, 30, 30))

    @staticmethod
    def to_string_plan_status(df):
        match df['status']:
            case 0:
                return 'Unopened'
            case 1:
                return 'Opened'
            case 2:
                return 'Closed'

    @staticmethod
    def unifiy_type(IDs):
        if type(IDs) == int:
            result = []
            result.append(IDs)
            return result
        else:
            return IDs
