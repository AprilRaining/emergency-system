import numpy as np
import pandas as pd
import sqlite3 as db
import re
from sqliteFunctions import get_linked_IDs, list_to_sqlite_string
from planInput import *
from print_table import *
from utilities import *
from system_log import *
import datetime

# To do
# Fix exceptions, Add stop button (while loop)
# change delete functions to include planid and status of the plan


def validate(date_text):
    try:
        res = bool(datetime.datetime.strptime(date_text, "%Y-%m-%d"))
        return res
    except ValueError:
        res = False
        return res


class Invalid_input(Exception):
    def __init__(self, input):
        Exception.__init__(self)
        self.input = input

    def __str__(self):
        return f'{str(self.input)} is an invalid input. Plese reenter your choice.'


class emergency_plan:
    def selection(self):
        print("1. Create Emergency Plan.")
        print("2. Display Emergency Plan.")
        print("3. Edit Emergency Plan.")
        print("4. Delete Emergency Plan.")
        self.user = input('Please enter your choice: ')
        loop = True
        while loop == True:
            try:
                if self.user == '1':
                    self.user = input(
                        u"\U0001F539" + 'Please enter your choice: ')
                    loop = True
                    loop = False
                elif self.user == '2':
                    display = self.Display_Emergency_Plan()
                    display
                    loop = False
                elif self.user == '3':
                    edit = self.Edit_Emergency_Plan()
                    edit
                    loop = False
                elif self.user == '4':
                    delete = self.Delete_Emergency_Plan()
                    delete
                    loop = False
                else:
                    raise Invalid_input(self.user)
            except Invalid_input as e:
                print_log(str(e))
                self.user = input(u"\U0001F539" + 'Please enter your choice: ')

    class Create_Emergency_Plan:
        def __init__(self):
            self.type = PlanInput.type()
            self.desc = PlanInput.description()
            self.area = input(
                u"\U0001F539" + 'Please input the geographical area affected by the natural disaster: ')
            loop = True
            while loop:
                try:
                    date_format = input(u"\U0001F539" + 'Please enter the start date of the emergency plan in the '
                                                        'format of yyyy-mm-dd: ')
                    if validate(date_format) == True:
                        in_date = date_format.split('-')
                        # Only allow date after the Year of 2000
                        # Need to consider literal (change here)
                        try:
                            self.date = datetime.date(
                                int(in_date[0]), int(in_date[1]), int(in_date[2]))
                            if (2000 <= int(in_date[0])) and (1 <= int(in_date[1]) <= 12) and (1 <= int(in_date[2]) <= 31) and \
                                    self.date >= datetime.date.today():
                                loop = False
                                if self.date == datetime.date.today():
                                    self.status = 1
                                else:
                                    self.status = 0
                            else:
                                print(
                                    "\nThe start date must be later than today or just today!")
                                raise Invalid_input(date_format)
                        except Invalid_input as e:
                            print_log(str(e))
                    else:
                        raise Invalid_input(date_format)
                except Invalid_input as e:
                    print_log(str(e))
            loop = True
            while loop:
                try:
                    camp = 0
                    if camp.isdigit():
                        self.camp = camp
                        print("\n")
                        loop = False
                    else:
                        raise Invalid_input(camp)
                except Invalid_input as e:
                    print_log(str(e))

        def add(self):
            conn = db.connect('info_files/emergency_system.db')
            c = conn.cursor()
            c.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='plan'")
            if len(c.fetchall()) == 0:
                newdataframe = pd.DataFrame({'planID': [1], 'type': [self.type], 'description': [self.desc],
                                             'area': [self.area], 'startDate': [self.date],
                                             'numberOfCamps': [self.camp], 'status': [self.status]})
                newdataframe.to_sql('plan', conn, index=False)
                print(newdataframe.to_string(index=False))
                c.execute(
                    "CREATE TABLE camp (campID INTEGER PRIMARY KEY AUTOINCREMENT, capacity INTEGER, planID INTEGER)")
                conn.commit()
                for _ in range(int(self.camp)):
                    c.execute(
                        "INSERT INTO camp (capacity, planID) VALUES (?, ?)", (20, 1))
                    conn.commit()

            else:
                dataframe = pd.read_sql_query('SELECT * FROM plan', conn)
                self.planID = int(
                    c.execute("select max(planID) from plan").fetchall()[0][0]) + 1
                # print(self.planID, type(self.planID))
                newdataframe = pd.DataFrame(
                    {'planID': [self.planID], 'type': [self.type], 'description': [self.desc],
                     'area': [self.area], 'startDate': [self.date], 'numberOfCamps': [self.camp],
                     'status': [self.status]})
                if ((self.type in dataframe['type'].values)
                        & (self.desc in dataframe['description'].values)
                        & (self.area in dataframe['area'].values)
                        & (str(self.date) in dataframe['startDate'].values)
                        & (self.camp in list(dataframe['numberOfCamps'].values))):
                    print(dataframe.to_string(index=False))
                else:
                    newdataframe.to_sql(
                        'plan', conn, index=False, if_exists="append")
                    updatedframe = pd.read_sql_query(
                        'SELECT * FROM plan', conn)
                    # campframe = pd.read_sql_query('SELECT * FROM camp', conn)
                    # campID = int(campframe['campID'].iloc[-1]) + 1
                    # for i in range(int(self.camp)):
                    #     c.execute("INSERT INTO camp (campID, capacity, planID) VALUES (?, ?, ?)",
                    #               (campID + i, 20, self.planID))
                    #     conn.commit()
                    print(updatedframe.to_string(index=False))
            conn.close()

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input(
                'Please choose which emergency plan to be displayed: ')

    class Delete_Emergency_Plan:
        def __init__(self):
            self.delete_now()

        # Delete Plan Now
        def delete_now(self):
            conn = db.connect('info_files/emergency_system.db')
            c = conn.cursor()
            print('1. Delete by viewing the type of the emergency plan.')
            print('2. Delete by viewing the start date of the emergency plan.')
            print('3. Delete by viewing the geographical area of the emergency plan.')
            print('0. Exit.')
            self.choice = input('Please enter your choice: ')
            loop = True
            while loop == True:
                try:
                    if self.choice == '1':
                        loop = False
                        typeframe = pd.read_sql_query(
                            'SELECT * FROM plan where status = 2', conn)
                        print(
                            f'The choices of type are: {set(typeframe.type.values)}.')
                        self.type = input(
                            'Please enter which type of emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.type in typeframe.type.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['type']
                                                           == self.type]
                                    finalframe = finalframe.reset_index(
                                        drop=True)
                                    print(finalframe)
                                    while True:
                                        self.row = input(
                                            'Please choose which row starting from 0 above you want to delete: ')
                                        if (not self.row.isdigit()) or (int(self.row) >= len(finalframe)):
                                            print(
                                                "Please input a valid number.")
                                            continue
                                        else:
                                            self.row = int(self.row)
                                            break

                                    # while True:
                                    #     date_format = input('Please enter the close date of the emergency plan '
                                    #                         'in the format of yyyy-mm-dd: ')
                                    #     if not re.match(re.compile(r"^\d{4}-\d{2}-\d{2}$"), date_format.strip()):
                                    #         print("input format is not right, please input again.")
                                    #         continue
                                    #     else:
                                    #         break
                                    date_format = datetime.datetime.now().strftime("%Y-%m-%d")
                                    in_date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(
                                                self.row)]
                                            if check_camp(int(row[0])):
                                                return
                                            planID = row[0]
                                            type = row[1]
                                            desc = row[2]
                                            area = row[3]
                                            start_date = row[4]
                                            camp = row[5]
                                            status = row[6]
                                            self.close = datetime.date(
                                                int(in_date[0]), int(in_date[1]), int(in_date[2]))
                                            start_date_raw = start_date.split(
                                                '-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),
                                                                           int(
                                                                               start_date_raw[1]),
                                                                           int(start_date_raw[2]))
                                            if (2000 <= int(in_date[0])) and (1 <= int(in_date[1]) <= 12) and (
                                                    1 <= int(in_date[2]) <= 31):
                                                loop2 = False
                                                while loop3 == True:
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            c.execute(
                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                            if len(c.fetchall()) == 0:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp]})
                                                                newdataframe.to_sql(
                                                                    'delete', conn, index=False)

                                                            else:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp]})
                                                                newdataframe.to_sql('delete', conn, index=False,
                                                                                    if_exists="append")

                                                            index = typeframe[(
                                                                typeframe['planID'] == planID)].index

                                                            typeframe = typeframe.drop(
                                                                index)

                                                            typeframe.to_sql('plan', conn, index=False,
                                                                             if_exists="replace")
                                                            updatedframe = pd.read_sql_query(
                                                                'SELECT * FROM plan', conn)
                                                            print(
                                                                "Delete successfully! These are the current plans:")
                                                            print(updatedframe.to_string(
                                                                index=False))

                                                            campframe = pd.read_sql_query(
                                                                'SELECT * FROM camp', conn)
                                                            index1 = campframe[campframe['planID']
                                                                               == planID].index
                                                            campframe = campframe.drop(
                                                                index1)
                                                            campframe.to_sql('camp', conn, index=False,
                                                                             if_exists="replace")

                                                            move_vol(
                                                                int(row[0]))

                                                        else:
                                                            raise Invalid_input(
                                                                self.row)
                                                    except Invalid_input as e:
                                                        print(e)
                                                        self.row = input(
                                                            'Please enter your choice: ')
                                            else:
                                                raise Invalid_input(
                                                    date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input(
                                                'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                            in_date = date_format.split('-')
                                else:
                                    raise Invalid_input(self.type)
                            except Invalid_input as e:
                                print(e)
                                self.type = input('Please enter your choice: ')

                    elif self.choice == '2':
                        loop = False
                        typeframe = pd.read_sql_query(
                            'SELECT * FROM plan where status = 2', conn)
                        print(set(typeframe['startDate']))
                        while True:
                            self.date = input('Please enter the start date of the emergency plan you want to '
                                              'view and then delete in the format of yyyy-mm-dd: ')
                            if not re.match(re.compile(r"^\d{4}-\d{2}-\d{2}$"), self.date.strip()):
                                print(
                                    "input format is not right, please input again.")
                                continue
                            else:
                                break

                        start_date_entered = self.date.split('-')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if (2000 <= int(start_date_entered[0])) and (
                                        1 <= int(start_date_entered[1]) <= 12) and (
                                        1 <= int(start_date_entered[2]) <= 31) and self.date in set(
                                        typeframe['startDate']):
                                    loop1 = False
                                    finalframe = typeframe[typeframe['startDate']
                                                           == self.date]

                                    finalframe = finalframe.reset_index(
                                        drop=True)
                                    print(finalframe)

                                    while True:
                                        self.row = input('Please choose which row '
                                                         'starting from 0 above you want to delete: ')
                                        if (not self.row.isdigit()) or int(self.row) >= len(finalframe):
                                            print(
                                                "Please input a valid number ")
                                            continue
                                        else:
                                            self.row = int(self.row)
                                            break

                                    # date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                    date_format = datetime.datetime.now().strftime("%Y-%m-%d")
                                    in_date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(
                                                self.row)]
                                            if check_camp(int(row[0])):
                                                return
                                            planID = row[0]
                                            type = row[1]
                                            desc = row[2]
                                            area = row[3]
                                            start_date = row[4]
                                            camp = row[5]
                                            status = row[6]
                                            self.close = datetime.date(
                                                int(in_date[0]), int(in_date[1]), int(in_date[2]))
                                            start_date_raw = start_date.split(
                                                '-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),
                                                                           int(
                                                                               start_date_raw[1]),
                                                                           int(start_date_raw[2]))
                                            # print("sssss: ", start_date, date)
                                            if (2000 <= int(in_date[0])) and (1 <= int(in_date[1]) <= 12) and (
                                                    1 <= int(in_date[2]) <= 31):
                                                loop2 = False
                                                while loop3 == True:
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            c.execute(
                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                            if len(c.fetchall()) == 0:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp]})
                                                                newdataframe.to_sql(
                                                                    'delete', conn, index=False)

                                                            else:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp]})
                                                                newdataframe.to_sql('delete', conn, index=False,
                                                                                    if_exists="append")

                                                            move_vol(
                                                                int(row[0]))

                                                            index = typeframe[(
                                                                typeframe['planID'] == planID)].index
                                                            typeframe = typeframe.drop(
                                                                index)
                                                            typeframe.to_sql('plan', conn, index=False,
                                                                             if_exists="replace")
                                                            updatedframe = pd.read_sql_query(
                                                                'SELECT * FROM plan', conn)
                                                            print(
                                                                "Delete successfully! These are the current plans:")
                                                            print(updatedframe.to_string(
                                                                index=False))

                                                            campframe = pd.read_sql_query(
                                                                'SELECT * FROM camp', conn)
                                                            index1 = campframe[campframe['planID']
                                                                               == planID].index
                                                            campframe = campframe.drop(
                                                                index1)
                                                            campframe.to_sql('camp', conn, index=False,
                                                                             if_exists="replace")

                                                        else:
                                                            raise Invalid_input(
                                                                self.row)
                                                    except Invalid_input as e:
                                                        print(e)
                                                        self.row = input(
                                                            'Please enter your choice: ')
                                            else:
                                                raise Invalid_input(
                                                    date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input(
                                                'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                            in_date = date_format.split('-')
                                else:
                                    raise Invalid_input(self.date)
                            except Invalid_input as e:
                                print(e)
                                self.date = input('Please enter the start date of the emergency plan you want to '
                                                  'view and then delete in the format of yyyy-mm-dd: ')
                    elif self.choice == '3':
                        loop = False
                        typeframe = pd.read_sql_query(
                            'SELECT * FROM plan where status = 2', conn)
                        print(
                            f'The choices of type are: {set(typeframe.area.values)}.')
                        self.area = input(
                            'Please enter the area of the emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.area in typeframe.area.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['area']
                                                           == self.area]
                                    finalframe = finalframe.reset_index(
                                        drop=True)
                                    print(finalframe)

                                    while True:
                                        self.row = input('Please choose which row '
                                                         'starting from 0 above you want to delete:')
                                        if (not self.row.isdigit()) or int(self.row) >= len(finalframe):
                                            print(
                                                "Please input a valid number ")
                                            continue
                                        else:
                                            self.row = int(self.row)
                                            break

                                    # date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                    date_format = datetime.datetime.now().strftime("%Y-%m-%d")
                                    in_date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(
                                                self.row)]
                                            if check_camp(int(row[0])):
                                                return
                                            planID = row[0]
                                            type = row[1]
                                            desc = row[2]
                                            area = row[3]
                                            start_date = row[4]
                                            camp = row[5]
                                            status = row[6]
                                            self.close = datetime.date(
                                                int(in_date[0]), int(in_date[1]), int(in_date[2]))
                                            start_date_raw = start_date.split(
                                                '-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),
                                                                           int(
                                                                               start_date_raw[1]),
                                                                           int(start_date_raw[2]))
                                            if (2000 <= int(in_date[0])) and (1 <= int(in_date[1]) <= 12) and (
                                                    1 <= int(in_date[2]) <= 31):
                                                loop2 = False
                                                while loop3 == True:
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            c.execute(
                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                            if len(c.fetchall()) == 0:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp],
                                                                     'Clost Date': [self.close], 'status': [2]})
                                                                newdataframe.to_sql(
                                                                    'delete', conn, index=False)

                                                            else:
                                                                newdataframe = pd.DataFrame(
                                                                    {'planID': [planID], 'type': [type],
                                                                     'description': [desc],
                                                                     'area': [area], 'startDate': [start_date],
                                                                     'numberOfCamps': [camp],
                                                                     'Clost Date': [self.close], 'status': [2]})
                                                                newdataframe.to_sql('delete', conn, index=False,
                                                                                    if_exists="append")

                                                            index = typeframe[(
                                                                typeframe['planID'] == planID)].index
                                                            typeframe = typeframe.drop(
                                                                index)
                                                            typeframe.to_sql('plan', conn, index=False,
                                                                             if_exists="replace")
                                                            updatedframe = pd.read_sql_query(
                                                                'SELECT * FROM plan', conn)
                                                            print(
                                                                "Delete successfully! These are the current plans:")
                                                            print(updatedframe.to_string(
                                                                index=False))

                                                            campframe = pd.read_sql_query(
                                                                'SELECT * FROM camp', conn)
                                                            index1 = campframe[campframe['planID']
                                                                               == planID].index
                                                            campframe = campframe.drop(
                                                                index1)
                                                            campframe.to_sql('camp', conn, index=False,
                                                                             if_exists="replace")

                                                            move_vol(
                                                                int(row[0]))

                                                        else:
                                                            raise Invalid_input(
                                                                self.row)
                                                    except Invalid_input as e:
                                                        print(e)
                                                        self.row = input(
                                                            'Please enter your choice: ')
                                            else:
                                                raise Invalid_input(
                                                    date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input(
                                                'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                            in_date = date_format.split('-')
                                else:
                                    raise Invalid_input(self.area)
                            except Invalid_input as e:
                                print(e)
                                self.area = input(
                                    'Please enter the area of the emergency plan you want to view and then delete: ')
                    elif self.choice == '0':
                        return
                    else:
                        raise Invalid_input(self.choice)
                except Invalid_input as e:
                    print(e)
                    self.choice = input('Please enter your choice: ')

    # Delete Plan in a future date

    class Edit_Emergency_Plan:
        def __init__(self):
            self.type = input(
                'Please choose which emergency plan to be edited: ')


def check_camp(planID):
    # print("planID is ", planID)
    campIDs = get_linked_IDs('camp', 'plan', planID)
    # print(campIDs)
    refugeeIDs = get_linked_IDs('refugee', 'camp', campIDs)
    if refugeeIDs:
        print("There are some refugees in this plan, please treat them first.")
        return 1
    else:
        return 0


def move_vol(planID):
    campIDs = get_linked_IDs('camp', 'plan', planID)
    volunteerIDs = get_linked_IDs('volunteer', 'camp', campIDs)
    with db.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        c.execute(
            f'update volunteer set campId = 0 where volunteerID in {list_to_sqlite_string(volunteerIDs)}')
        conn.commit()
