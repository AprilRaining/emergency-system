import numpy as np
import pandas as pd
import datetime
import os.path 
import sqlite3 as db

conn = db.connect('emergency_system.db')
c = conn.cursor()

# To do 
# Fix exceptions, Add stop button 



class Invalid_input(Exception):
    def __init__(self, input):
        Exception.__init__(self)
        self.input = input
    def __str__(self): 
        return f'{self.input} is an invalid choice. Plese reenter a number specified above.'


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
            self.desc = input('Please etner the description of the emergency plan: ')
            self.area = input('Please enter the geographical area affected by the natural diaster: ')
            try:
               date_format = input('Please enter the start date of the emergency plan in the format of yyyy-mm-dd: ') 
               date = date_format.split('-')
               # Only allow date after the Year of 2000  
               # Need to consider literal (change here )
               if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31):
                self.date= datetime.date(int(date[0]), int(date[1]), int(date[2]))
               else:
                raise Invalid_input(date_format)
            except Invalid_input as e:
                print(e)
            try:
                camp = input('Please enter the number of camps required: ')
                if camp.isdigit():
                    self.camp = camp 
                else:
                    raise Invalid_input(camp)
            except Invalid_input as e:
                print(e)
            
        
        def add(self):
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plan'")
                if len(c.fetchall()) == 0: 
                    newdataframe = pd.DataFrame({'Type': [self.type], 'Description': [self.desc], 
                     'Area': [self.area], 'Start Date': [self.date], '# camps': [self.camp]})
                    newdataframe.to_sql('plan', conn, index= False)
                    print(newdataframe)
                else: 
                    dataframe = pd.read_sql_query('SELECT * FROM plan', conn)
                    if((self.type in dataframe['Type'].values) & (self.desc in dataframe['Description'].values) & (self.area in dataframe['Area'].values) & (str(self.date) in dataframe['Start Date'].values) & (self.camp in dataframe['# camps'].values)):
                        print(dataframe)
                    else:
                        newdataframe = pd.DataFrame({'Type': [self.type], 'Description': [self.desc], 
                        'Area': [self.area], 'Start Date': [self.date], '# camps': [self.camp]})
                        newdataframe.to_sql('plan', conn, index= False, if_exists="append")
                        updatedframe = pd.read_sql_query('SELECT * FROM plan', conn)
                        print(updatedframe)
            
                
                
                

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input('Please choose which emergency plan to be displayed: ')
            
 
    class Delete_Emergency_Plan:
         def __init__(self):
            print('Do you want to delete the emergencey plan now: ')
            print('1. Now')
            self.when = input('Please enter your choice: ')
            loop = True
            while loop == True: 
                try:
                 if self.when == '1':
                        self.delete_now()
                        loop = False
                 else: 
                        raise Invalid_input(self.when)
                except Invalid_input as e:
                    print(e)
                    self.when = input('Please enter your choice: ')
                
        #Delete Plan Now
         def delete_now(self):
            print('1. Delete by viewing the type of the emergency plan.')
            print('2. Delete by viewing the start date of the emergency plan.')
            print('3. Delete by viewing the geographical area of the emergency plan.')
            self.choice = input('Please enter your choice: ')
            loop = True
            while loop == True: 
                try:
                 if self.choice == '1':
                        loop = False
                        typeframe = pd.read_csv('emergency_plan_1.csv')
                        print(f'The choices of type are: {set(typeframe.Type.values)}.')
                        self.type = input('Please enter which type of emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.type in typeframe.Type.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Type'] == self.type]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input('Please choose which row above you want to delete: ')
                                    date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                    date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(self.row)]
                                            type = row[0]
                                            desc = row[1]
                                            area = row[2]
                                            start_date = row[3]
                                            refugee = row[4]
                                            volunteer = row[5]
                                            self.close = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                                            start_date_raw = start_date.split('-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),  int(start_date_raw[1]), int(start_date_raw[2]))
                                            if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31) and self.close >= start_datetime:
                                                loop2 = False
                                                while loop3 == True: 
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            file_exists = os.path.isfile('delete.csv')
                                                            if not file_exists:
                                                                 emptydataframe = pd.DataFrame(data = None, columns = np.array(['Type',
                                                                 'Description', 'Area', 'Start Date', '# refugees', '# humanitarian volunteers',
                                                                 'close date']))
                                                                 emptydataframe.to_csv('delete.csv', index = False)
                                                                 newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                 'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                 '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                 newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                            else:
                                                                dataframe = pd.read_csv('delete.csv')
                                                                if not ((dataframe['Type'] == type) & (dataframe['Description'] == desc)
                                                                & (dataframe['Area'] == area) & (dataframe['Start Date'] == start_date)
                                                                & (dataframe['# refugees'] == refugee) & (dataframe['# humanitarian volunteers'] == volunteer)
                                                                & (dataframe['close date'] == self.close)).any(): 
                                                                    newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                    'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                    '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                    newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                                    
                                                            index = typeframe[(typeframe['Type'] == type) &
                                                            (typeframe['Description'] == desc) & (typeframe['Area'] == area) & 
                                                            (typeframe['Start Date'] == start_date) & (typeframe['# refugees'] == refugee)
                                                            & (typeframe['# humanitarian volunteers'] == volunteer)].index
                                                            typeframe = typeframe.drop(index)
                                                            typeframe.to_csv('emergency_plan_1.csv', mode = 'w', index = False)
                                                        else: 
                                                             raise Invalid_input(self.row)
                                                    except Invalid_input as e:
                                                            print(e)
                                                            self.row = input('Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.type)
                            except Invalid_input as e:
                                 print(e)
                                 self.type = input('Please enter your choice: ')
                        
                 elif self.choice == '2':
                        loop = False
                        typeframe = pd.read_csv('emergency_plan_1.csv')
                        print(set(typeframe['Start Date']))
                        self.date = input('Please enter the start date of the emergency plan you want to view and then delete in the format of yyyy-mm-dd: ')
                        start_date_entered = self.date.split('-')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if (2000 <= int(start_date_entered[0])) and (1 <= int(start_date_entered[1]) <= 12) and (1 <= int(start_date_entered[2]) <= 31) and self.date in set(typeframe['Start Date']):
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Start Date'] == self.date]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input('Please choose which row above you want to delete: ')
                                    date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                    date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(self.row)]
                                            type = row[0]
                                            desc = row[1]
                                            area = row[2]
                                            start_date = row[3]
                                            refugee = row[4]
                                            volunteer = row[5]
                                            self.close = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                                            start_date_raw = start_date.split('-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),  int(start_date_raw[1]), int(start_date_raw[2]))
                                            if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31) and self.close >= start_datetime:
                                                loop2 = False
                                                while loop3 == True: 
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            file_exists = os.path.isfile('delete.csv')
                                                            if not file_exists:
                                                                 emptydataframe = pd.DataFrame(data = None, columns = np.array(['Type',
                                                                 'Description', 'Area', 'Start Date', '# refugees', '# humanitarian volunteers',
                                                                 'close date']))
                                                                 emptydataframe.to_csv('delete.csv', index = False)
                                                                 newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                 'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                 '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                 newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                            else:
                                                                dataframe = pd.read_csv('delete.csv')
                                                                if not ((dataframe['Type'] == type) & (dataframe['Description'] == desc)
                                                                & (dataframe['Area'] == area) & (dataframe['Start Date'] == start_date)
                                                                & (dataframe['# refugees'] == refugee) & (dataframe['# humanitarian volunteers'] == volunteer)
                                                                & (dataframe['close date'] == self.close)).any(): 
                                                                    newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                    'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                    '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                    newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                                    
                                                            index = typeframe[(typeframe['Type'] == type) &
                                                            (typeframe['Description'] == desc) & (typeframe['Area'] == area) & 
                                                            (typeframe['Start Date'] == start_date) & (typeframe['# refugees'] == refugee)
                                                            & (typeframe['# humanitarian volunteers'] == volunteer)].index
                                                            typeframe = typeframe.drop(index)
                                                            typeframe.to_csv('emergency_plan_1.csv', mode = 'w', index = False)
                                                        else: 
                                                             raise Invalid_input(self.row)
                                                    except Invalid_input as e:
                                                            print(e)
                                                            self.row = input('Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.date)
                            except Invalid_input as e:
                                 print(e)
                                 self.date = input('Please enter the start date of the emergency plan you want to view and then delete in the format of yyyy-mm-dd: ')
                 elif self.choice == '3':
                    loop = False
                    typeframe = pd.read_csv('emergency_plan_1.csv')
                    print(f'The choices of type are: {set(typeframe.Area.values)}.')
                    self.area = input('Please enter the area of the emergency plan you want to view and then delete: ')
                    loop1 = True
                    while loop1 == True:
                            try:
                                if self.area in typeframe.Area.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Area'] == self.area]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input('Please choose which row above you want to delete: ')
                                    date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                    date = date_format.split('-')
                                    loop2 = True
                                    loop3 = True
                                    while loop2 == True:
                                        try:
                                            row = finalframe.iloc[int(self.row)]
                                            type = row[0]
                                            desc = row[1]
                                            area = row[2]
                                            start_date = row[3]
                                            refugee = row[4]
                                            volunteer = row[5]
                                            self.close = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                                            start_date_raw = start_date.split('-')
                                            start_datetime = datetime.date(int(start_date_raw[0]),  int(start_date_raw[1]), int(start_date_raw[2]))
                                            if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31) and self.close >= start_datetime:
                                                loop2 = False
                                                while loop3 == True: 
                                                    try:
                                                        if int(self.row) in finalframe.index:
                                                            loop3 = False
                                                            file_exists = os.path.isfile('delete.csv')
                                                            if not file_exists:
                                                                 emptydataframe = pd.DataFrame(data = None, columns = np.array(['Type',
                                                                 'Description', 'Area', 'Start Date', '# refugees', '# humanitarian volunteers',
                                                                 'close date']))
                                                                 emptydataframe.to_csv('delete.csv', index = False)
                                                                 newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                 'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                 '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                 newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                            else:
                                                                dataframe = pd.read_csv('delete.csv')
                                                                if not ((dataframe['Type'] == type) & (dataframe['Description'] == desc)
                                                                & (dataframe['Area'] == area) & (dataframe['Start Date'] == start_date)
                                                                & (dataframe['# refugees'] == refugee) & (dataframe['# humanitarian volunteers'] == volunteer)
                                                                & (dataframe['close date'] == self.close)).any(): 
                                                                    newdataframe = pd.DataFrame({'Type': [type], 'Description': [desc], 
                                                                    'Area': [area], 'Start Date': [start_date], '# refugees': [refugee], 
                                                                    '# humanitarian volunteers': [volunteer], 'close date': [self.close]})
                                                                    newdataframe.to_csv('delete.csv', mode = 'a', header = False, index = False)
                                                                    
                                                            index = typeframe[(typeframe['Type'] == type) &
                                                            (typeframe['Description'] == desc) & (typeframe['Area'] == area) & 
                                                            (typeframe['Start Date'] == start_date) & (typeframe['# refugees'] == refugee)
                                                            & (typeframe['# humanitarian volunteers'] == volunteer)].index
                                                            typeframe = typeframe.drop(index)
                                                            typeframe.to_csv('emergency_plan_1.csv', mode = 'w', index = False)
                                                        else: 
                                                             raise Invalid_input(self.row)
                                                    except Invalid_input as e:
                                                            print(e)
                                                            self.row = input('Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print(e)
                                            date_format = input('Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.area)
                            except Invalid_input as e:
                                 print(e)
                                 self.area = input('Please enter the area of the emergency plan you want to view and then delete: ')
                 else: 
                        raise Invalid_input(self.choice)
                except Invalid_input as e:
                    print(e)
                    self.choice = input('Please enter your choice: ')


         




        #Delete Plan in a future date 

    class Edit_Emergency_Plan:
         def __init__(self):
            self.type = input('Please choose which emergency plan to be edited: ')
        


plan = emergency_plan()
plan.selection()


    










