from print_table import *
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
        df['status'] = df.apply(
            lambda a: TableDisplayer.to_string_plan_status(a), axis=1)
        col_width = (8, 20, 30, 16, 20, 20, 14, 8, 20, 20)
        print("\n")
        print_table(df.columns, df.to_numpy().tolist(), col_width)

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
        print(df.to_string(index=False))

    @staticmethod
    def to_string_plan_status(df):
        match df['status']:
            case 0:
                return 'Not opened'
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
