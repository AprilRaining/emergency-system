import numpy as np
import pandas as pd
import datetime
import sqlite3 as db

conn = db.connect('info_files/emergency_system.db')
c = conn.cursor()


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
        return f'{self.input} is an invalid input. Plese reenter your choice.'


class emergency_plan:
    def selection(self):
        print("0. Exit the program.")
        print("1. Create Emergency Plan.")
        print("2. Display Emergency Plan.")
        print("3. Edit Emergency Plan.")
        print("4. Delete Emergency Plan.")
        self.user = input('Please enter your choice: ')
        loop = True
        while loop == True:
            try:
                if self.user == '0':
                    break
                elif self.user == '1':
                    create = self.Create_Emergency_Plan()
                    create.add()
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
                print(e)
                self.user = input('Please enter your choice: ')

    class Create_Emergency_Plan:
        def __init__(self):
            self.type = input('Please enter the type of Emgergency: ')
            self.desc = input('Please enter the description of the emergency plan: ')
            self.area = input('Please enter the geographical area affected by the natural diaster: ')
            loop = True
            while loop:
                try:
                    date_format = input(
                        'Please enter the start date of the emergency plan in the format of yyyy-mm-dd: ')
                    if validate(date_format) == True:
                        date = date_format.split('-')
                        # Only allow date after the Year of 2000
                        # Need to consider literal (change here)
                        try:
                            self.date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                            if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (
                                    1 <= int(date[2]) <= 31) and self.date >= datetime.date.today():
                                loop = False
                                if self.date == datetime.date.today():
                                    self.status = 1
                                else:
                                    self.status = 0
                            else:
                                raise Invalid_input(date_format)
                        except Invalid_input as e:
                            print(e)
                    else:
                        raise Invalid_input(date_format)
                except Invalid_input as e:
                    print(e)
            loop = True
            while loop:
                try:
                    camp = input('Please enter the number of camps required: ')
                    if camp.isdigit():
                        self.camp = camp
                        loop = False
                    else:
                        raise Invalid_input(camp)
                except Invalid_input as e:
                    print(e)

        def add(self):
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plan'")
            if len(c.fetchall()) == 0:
                newdataframe = pd.DataFrame({'planID': [1], 'type': [self.type], 'description': [self.desc],
                                             'area': [self.area], 'startDate': [self.date], 'numberOfCamps': [self.camp],
                                             'status': [self.status]})
                newdataframe.to_sql('plan', conn, index=False)
                print(newdataframe.to_string(index=False))
                c.execute(
                    "CREATE TABLE camp (campID INTEGER PRIMARY KEY AUTOINCREMENT, capacity INTEGER, planID INTEGER)")
                for _ in range(int(self.camp)):
                    c.execute("INSERT INTO camp (capacity, planID) VALUES (?, ?)", (20, 1))
                conn.commit()

            else:
                dataframe = pd.read_sql_query('SELECT * FROM plan', conn)
                if len(dataframe) == 0:
                    self.planID = 1
                else:
                    self.planID = int(dataframe['planID'].iloc[-1]) + 1
                if ((self.type in dataframe['type'].values) & (self.desc in dataframe['description'].values) & (
                        self.area in dataframe['area'].values) & (str(self.date) in dataframe['startDate'].values)):
                    print(dataframe.to_string(index=False))
                else:
                    newdataframe = pd.DataFrame(
                        {'planID': [self.planID], 'type': [self.type], 'description': [self.desc],
                         'area': [self.area], 'startDate': [self.date], 'numberOfCamps': [self.camp],
                         'status': [self.status]})
                    newdataframe.to_sql('plan', conn, index=False, if_exists="append")
                    updatedframe = pd.read_sql_query('SELECT * FROM plan', conn)
                    campframe = pd.read_sql_query('SELECT * FROM camp', conn)
                    if len(campframe) == 0:
                        campID = 1
                    else:
                        campID = int(campframe['campID'].iloc[-1]) + 1
                    for i in range(int(self.camp)):
                        c.execute("INSERT INTO camp (campID, capacity, planID) VALUES (?, ?, ?)",
                                  (campID + i, 20, self.planID))
                    conn.commit()
                    print(updatedframe.to_string(index=False))

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input('Please choose which emergency plan to be displayed: ')

    class Delete_Emergency_Plan:
        def __init__(self):
            # print('Do you want to delete the emergencey plan now: ')
            # print('0. Exit')
            # print('1. Now')
            # self.when = input('Please enter your choice: ')
            # loop = True
            # while loop == True:
            #     try:
            #         if self.when == '0':
            #             break
            #         elif self.when == '1':
            #             self.delete_now()
            #             loop = False
            #         else:
            #             raise Invalid_input(self.when)
            #     except Invalid_input as e:
            #         print(e)
            #         self.when = input('Please enter your choice: ')
            pass

        # Delete Plan Now
        def delete_now(self):
            print('0. Exit.')
            print('1. Delete by viewing the type of the emergency plan.')
            print('2. Delete by viewing the start date of the emergency plan.')
            print('3. Delete by viewing the geographical area of the emergency plan.')
            self.choice = input('Please enter your choice: ')
            loop = True
            while loop == True:
                try:
                    if self.choice == '0':
                        break
                    elif self.choice == '1':
                        loop = False
                        typeframe = pd.read_sql_query('SELECT * FROM plan', conn)
                        print(f'The choices of type are: {set(typeframe.type.values)}.')
                        self.type = input(
                            'Please enter which type of emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.type in typeframe.type.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['type'] == self.type]
                                    finalframe = finalframe.reset_index(drop=True)
                                    print(finalframe)
                                    self.row = input(
                                        'Please choose which row starting from 0 above you want to delete: ')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            if self.row.isdigit():
                                                try:
                                                    if int(self.row) in finalframe.index:
                                                        row = finalframe.iloc[int(self.row)]
                                                        planID = row[0]
                                                        type = row[1]
                                                        desc = row[2]
                                                        area = row[3]
                                                        start_date = row[4]
                                                        camp = row[5]
                                                        status = row[6]
                                                        loop2 = False
                                                        while loop3 == True:
                                                            try:
                                                                date_format = input(
                                                                    'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                                                if validate(date_format) == True:
                                                                    date = date_format.split('-')
                                                                    try:
                                                                        self.close = datetime.date(int(date[0]),
                                                                                                   int(date[1]),
                                                                                                   int(date[2]))
                                                                        start_date_raw = start_date.split('-')
                                                                        start_datetime = datetime.date(
                                                                            int(start_date_raw[0]),
                                                                            int(start_date_raw[1]),
                                                                            int(start_date_raw[2]))
                                                                        if (2000 <= int(date[0])) and (
                                                                                1 <= int(date[1]) <= 12) and (1 <= int(
                                                                                date[
                                                                                    2]) <= 31) and self.close >= start_datetime and validate(
                                                                                date_format) == True:
                                                                            loop3 = False
                                                                            c.execute(
                                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                                            if len(c.fetchall()) == 0:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False)

                                                                            else:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False,
                                                                                                    if_exists="append")

                                                                            index = typeframe[
                                                                                (typeframe['planID'] == planID) & (
                                                                                            typeframe['type'] == type) &
                                                                                (typeframe['description'] == desc) & (
                                                                                            typeframe['area'] == area) &
                                                                                (typeframe[
                                                                                     'startDate'] == start_date) & (
                                                                                            typeframe[
                                                                                                'numberOfCamps'] == camp)
                                                                                & (typeframe['status'] == status)].index
                                                                            typeframe = typeframe.drop(index)
                                                                            typeframe.to_sql('plan', conn, index=False,
                                                                                             if_exists="replace")
                                                                            updatedframe = pd.read_sql_query(
                                                                                'SELECT * FROM plan', conn)
                                                                            print(updatedframe.to_string(index=False))

                                                                            campframe = pd.read_sql_query(
                                                                                'SELECT * FROM camp', conn)
                                                                            index1 = campframe[
                                                                                campframe['planID'] == planID].index
                                                                            campframe = campframe.drop(index1)
                                                                            campframe.to_sql('camp', conn, index=False,
                                                                                             if_exists="replace")
                                                                        else:
                                                                            raise Invalid_input(date_format)
                                                                    except Invalid_input as e:
                                                                        print(e)
                                                                else:
                                                                    raise Invalid_input(date_format)
                                                            except Invalid_input as e:
                                                                print(e)



                                                    else:
                                                        raise Invalid_input(self.row)
                                                except Invalid_input as e:
                                                    print(e)
                                                    self.row = input('Please enter your choice: ')
                                            else:
                                                raise Invalid_input(self.row)
                                        except Invalid_input as e:
                                            print(e)
                                            self.row = input('Please enter your choice: ')


                                else:
                                    raise Invalid_input(self.type)
                            except Invalid_input as e:
                                print(e)
                                self.type = input('Please enter your choice: ')

                    elif self.choice == '2':
                        loop = False
                        typeframe = pd.read_sql_query('SELECT * FROM plan', conn)
                        print(set(typeframe['startDate']))
                        loop1 = True
                        while loop1 == True:
                            try:
                                self.date = input(
                                    'Please enter the start date of the emergency plan you want to view and then delete in the format of yyyy-mm-dd: ')
                                if self.date in set(typeframe['startDate']):
                                    loop1 = False
                                    finalframe = typeframe[typeframe['startDate'] == self.date]
                                    finalframe = finalframe.reset_index(drop=True)
                                    print(finalframe)
                                    self.row = input(
                                        'Please choose which row starting from 0 above you want to delete: ')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            if self.row.isdigit():
                                                try:
                                                    if int(self.row) in finalframe.index:
                                                        row = finalframe.iloc[int(self.row)]
                                                        planID = row[0]
                                                        type = row[1]
                                                        desc = row[2]
                                                        area = row[3]
                                                        start_date = row[4]
                                                        camp = row[5]
                                                        status = row[6]
                                                        loop2 = False
                                                        while loop3 == True:
                                                            try:
                                                                date_format = input(
                                                                    'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                                                if validate(date_format) == True:
                                                                    date = date_format.split('-')
                                                                    try:
                                                                        self.close = datetime.date(int(date[0]),
                                                                                                   int(date[1]),
                                                                                                   int(date[2]))
                                                                        start_date_raw = start_date.split('-')
                                                                        start_datetime = datetime.date(
                                                                            int(start_date_raw[0]),
                                                                            int(start_date_raw[1]),
                                                                            int(start_date_raw[2]))
                                                                        if (2000 <= int(date[0])) and (
                                                                                1 <= int(date[1]) <= 12) and (1 <= int(
                                                                                date[
                                                                                    2]) <= 31) and self.close >= start_datetime:
                                                                            loop3 = False
                                                                            c.execute(
                                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                                            if len(c.fetchall()) == 0:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False)

                                                                            else:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False,
                                                                                                    if_exists="append")

                                                                            index = typeframe[
                                                                                (typeframe['planID'] == planID) & (
                                                                                            typeframe['type'] == type) &
                                                                                (typeframe['description'] == desc) & (
                                                                                            typeframe['area'] == area) &
                                                                                (typeframe[
                                                                                     'startDate'] == start_date) & (
                                                                                            typeframe[
                                                                                                'numberOfCamps'] == camp)
                                                                                & (typeframe['status'] == status)].index
                                                                            typeframe = typeframe.drop(index)
                                                                            typeframe.to_sql('plan', conn, index=False,
                                                                                             if_exists="replace")
                                                                            updatedframe = pd.read_sql_query(
                                                                                'SELECT * FROM plan', conn)
                                                                            print(updatedframe.to_string(index=False))

                                                                            campframe = pd.read_sql_query(
                                                                                'SELECT * FROM camp', conn)
                                                                            index1 = campframe[
                                                                                campframe['planID'] == planID].index
                                                                            campframe = campframe.drop(index1)
                                                                            campframe.to_sql('camp', conn, index=False,
                                                                                             if_exists="replace")

                                                                        else:
                                                                            raise Invalid_input(date_format)
                                                                    except Invalid_input as e:
                                                                        print(e)
                                                                else:
                                                                    raise Invalid_input(date_format)
                                                            except Invalid_input as e:
                                                                print(e)


                                                    else:
                                                        raise Invalid_input(self.row)
                                                except Invalid_input as e:
                                                    print(e)
                                                    self.row = input('Please enter your choice: ')
                                            else:
                                                raise Invalid_input(self.row)
                                        except Invalid_input as e:
                                            print(e)
                                            self.row = input('Please enter your choice: ')



                                else:
                                    raise Invalid_input(self.date)
                            except Invalid_input as e:
                                print(e)

                    elif self.choice == '3':
                        loop = False
                        typeframe = pd.read_sql_query('SELECT * FROM plan', conn)
                        print(f'The choices of area are: {set(typeframe.area.values)}.')
                        self.area = input(
                            'Please enter the area of the emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.area in typeframe.area.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['area'] == self.area]
                                    finalframe = finalframe.reset_index(drop=True)
                                    print(finalframe)
                                    self.row = input(
                                        'Please choose which row starting from 0 above you want to delete: ')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            if self.row.isdigit() == True:
                                                try:
                                                    if int(self.row) in finalframe.index:
                                                        row = finalframe.iloc[int(self.row)]
                                                        planID = row[0]
                                                        type = row[1]
                                                        desc = row[2]
                                                        area = row[3]
                                                        start_date = row[4]
                                                        camp = row[5]
                                                        status = row[6]
                                                        loop2 = False
                                                        while loop3 == True:
                                                            try:
                                                                date_format = input(
                                                                    'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ')
                                                                if validate(date_format) == True:
                                                                    date = date_format.split('-')
                                                                    try:
                                                                        self.close = datetime.date(int(date[0]),
                                                                                                   int(date[1]),
                                                                                                   int(date[2]))
                                                                        start_date_raw = start_date.split('-')
                                                                        start_datetime = datetime.date(
                                                                            int(start_date_raw[0]),
                                                                            int(start_date_raw[1]),
                                                                            int(start_date_raw[2]))

                                                                        if (2000 <= int(date[0])) and (
                                                                                1 <= int(date[1]) <= 12) and (1 <= int(
                                                                                date[
                                                                                    2]) <= 31) and self.close >= start_datetime:
                                                                            loop3 = False
                                                                            c.execute(
                                                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='delete'")
                                                                            if len(c.fetchall()) == 0:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False)

                                                                            else:
                                                                                newdataframe = pd.DataFrame(
                                                                                    {'planID': [planID], 'type': [type],
                                                                                     'description': [desc],
                                                                                     'area': [area],
                                                                                     'startDate': [start_date],
                                                                                     'numberOfCamps': [camp],
                                                                                     'Clost Date': [self.close],
                                                                                     'status': [2]})
                                                                                newdataframe.to_sql('delete', conn,
                                                                                                    index=False,
                                                                                                    if_exists="append")

                                                                            index = typeframe[
                                                                                (typeframe['planID'] == planID) & (
                                                                                            typeframe['type'] == type) &
                                                                                (typeframe['description'] == desc) & (
                                                                                            typeframe['area'] == area) &
                                                                                (typeframe[
                                                                                     'startDate'] == start_date) & (
                                                                                            typeframe[
                                                                                                'numberOfCamps'] == camp)
                                                                                & (typeframe['status'] == status)].index
                                                                            typeframe = typeframe.drop(index)
                                                                            typeframe.to_sql('plan', conn, index=False,
                                                                                             if_exists="replace")
                                                                            updatedframe = pd.read_sql_query(
                                                                                'SELECT * FROM plan', conn)
                                                                            print(updatedframe.to_string(index=False))

                                                                            campframe = pd.read_sql_query(
                                                                                'SELECT * FROM camp', conn)
                                                                            index1 = campframe[
                                                                                campframe['planID'] == planID].index
                                                                            campframe = campframe.drop(index1)
                                                                            campframe.to_sql('camp', conn, index=False,
                                                                                             if_exists="replace")



                                                                        else:
                                                                            raise Invalid_input(date_format)
                                                                    except Invalid_input as e:
                                                                        print(e)
                                                                else:
                                                                    raise Invalid_input(date_format)
                                                            except Invalid_input as e:
                                                                print(e)

                                                    else:
                                                        raise Invalid_input(self.row)
                                                except Invalid_input as e:
                                                    print(e)
                                                    self.row = input('Please enter your choice: ')
                                            else:
                                                raise Invalid_input(self.row)
                                        except Invalid_input as e:
                                            print(e)
                                            self.row = input('Please enter your choice: ')



                                else:
                                    raise Invalid_input(self.area)
                            except Invalid_input as e:
                                print(e)
                                self.area = input(
                                    'Please enter the area of the emergency plan you want to view and then delete: ')
                    else:
                        raise Invalid_input(self.choice)
                except Invalid_input as e:
                    print(e)
                    self.choice = input('Please enter your choice: ')

    # Delete Plan in a future date

    class Edit_Emergency_Plan:
        def __init__(self):
            self.type = input('Please choose which emergency plan to be edited: ')

#
# plan = emergency_plan()
# plan.selection()













