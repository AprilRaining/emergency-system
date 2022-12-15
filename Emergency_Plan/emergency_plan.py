import numpy as np
import pandas as pd
import datetime
import os.path 
from core_code.system_log import *

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
        self.user = input(u'\U0001F539' +'Please enter your choice: ')
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
                print_log(e)
                self.user = input(u"\U0001F539" + 'Please enter your choice: ')
                
        

    class Create_Emergency_Plan:
        def __init__(self):
            self.type = input(u"\U0001F539" + 'Please enter the type of Emgergency: ')
            self.desc = input(u"\U0001F539" + 'Please etner the description of the emergency plan: ')
            self.area = input(u"\U0001F539" + 'Please enter the geographical area affected by the natural diaster: ')
            try:
               date_format = input(u"\U0001F539" + 'Please enter the start date of the emergency plan in the format of yyyy-mm-dd: ') 
               date = date_format.split('-')
               print("date",date)
               # Only allow date after the Year of 2000  
               if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31):
                self.date= datetime.date(int(date[0]), int(date[1]), int(date[2]))
               else:
                raise Invalid_input(date_format)
            except Invalid_input as e:
                print_log(e)
            try:
                refugee = input(u"\U0001F539" + 'Please enter the number of refugees at the camp: ')
                if refugee.isdigit():
                    self.refugee = refugee
                else:
                    raise Invalid_input(refugee)
            except Invalid_input as e:
                print_log(e)
            try:
                volunteer = input(u"\U0001F539" + 'Please enter the number of volunteers required at the camp: ')
                if volunteer.isdigit():
                    self.volunteer = volunteer
                else:
                    raise Invalid_input(volunteer)
            except Invalid_input as e:
                print_log(e)
            
        
        def add(self):
            file_exists = os.path.isfile('emergency_plan_1.csv')
            if not file_exists:
                emptydataframe = pd.DataFrame(data = None, columns = np.array(['Type',
                'Description', 'Area', 'Start Date', '# refugees', '# humanitarian volunteers']))
                emptydataframe.to_csv('emergency_plan_1.csv', index = False)
                newdataframe = pd.DataFrame({'Type': [self.type], 'Description': [self.desc], 
                     'Area': [self.area], 'Start Date': [self.date], '# refugees': [self.refugee], 
                     '# humanitarian volunteers': [self.volunteer]})
                newdataframe.to_csv('emergency_plan_1.csv', mode = 'a', header = False, index = False)
                #emptydataframe = pd.DataFrame(data = None, columns = np.array(['Type',
                #'description', 'Area', 'Start Date', '# refugees', '# humanitarian volunteers']))
                #emptydataframe.to_csv('emergency_plan_1.csv')
                print(newdataframe)
            else:
                dataframe = pd.read_csv('emergency_plan_1.csv')
                if ((dataframe['Type'] == self.type) & (dataframe['Description'] == self.desc)
                & (dataframe['Area'] == self.area) & (dataframe['Start Date'] == self.date)
                & (dataframe['# refugees'] == self.refugee) & (dataframe['# humanitarian volunteers'] == self.volunteer)).any():
                    print(dataframe)
                else: 
                    newdataframe = pd.DataFrame({'Type': [self.type], 'Description': [self.desc], 
                     'Area': [self.area], 'Start Date': [self.date], '# refugees': [self.refugee], 
                     '# humanitarian volunteers': [self.volunteer]})
                    newdataframe.to_csv('emergency_plan_1.csv', mode = 'a', header = False, index = False)
                    updatedframe = pd.read_csv('emergency_plan_1.csv')
                    print(updatedframe)
                
                
                

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input(u"\U0001F539" + 'Please choose which emergency plan to be displayed: ')
            
 
    class Delete_Emergency_Plan:
         def __init__(self):
            print('Do you want to delete the emergencey plan now: ')
            print('1. Now')
            self.when = input(u"\U0001F539" + 'Please enter your choice: ')
            loop = True
            while loop == True: 
                try:
                 if self.when == '1':
                        self.delete_now()
                        loop = False
                 else: 
                        raise Invalid_input(self.when)
                except Invalid_input as e:
                    print_log(e)
                    self.when = input(u"\U0001F539" + 'Please enter your choice: ')
                
        #Delete Plan Now
         def delete_now(self):
            print('1. Delete by viewing the type of the emergency plan.')
            print('2. Delete by viewing the start date of the emergency plan.')
            print('3. Delete by viewing the geographical area of the emergency plan.')
            self.choice = input(u"\U0001F539" + 'Please enter your choice: ')
            loop = True
            while loop == True: 
                try:
                 if self.choice == '1':
                        loop = False
                        typeframe = pd.read_csv('emergency_plan_1.csv')
                        print(f'The choices of type are: {set(typeframe.Type.values)}.')
                        
                        self.type = input(u"\U0001F539" + 'Please enter which type of emergency plan you want to view and then delete: ')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if self.type in typeframe.Type.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Type'] == self.type]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input(u"\U0001F539" + 'Please choose which row above you want to delete: ')
                                    date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
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
                                                            print_log(e)
                                                            self.row = input(u"\U0001F539" + 'Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print_log(e)
                                            date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.type)
                            except Invalid_input as e:
                                 print_log(e)
                                 self.type = input(u"\U0001F539" + 'Please enter your choice: ')
                        
                 elif self.choice == '2':
                        loop = False
                        typeframe = pd.read_csv('emergency_plan_1.csv')
                        print(set(typeframe['Start Date']))
                        self.date = input(u"\U0001F539" + 'Please enter the start date of the emergency plan you want to view and then delete in the format of yyyy-mm-dd: ')
                        start_date_entered = self.date.split('-')
                        loop1 = True
                        while loop1 == True:
                            try:
                                if (2000 <= int(start_date_entered[0])) and (1 <= int(start_date_entered[1]) <= 12) and (1 <= int(start_date_entered[2]) <= 31) and self.date in set(typeframe['Start Date']):
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Start Date'] == self.date]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input(u"\U0001F539" + 'Please choose which row above you want to delete: ')
                                    date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
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
                                                            print_log(e)
                                                            self.row = input(u"\U0001F539" + 'Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print_log(e)
                                            date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.date)
                            except Invalid_input as e:
                                 print_log(e)
                                 self.date = input(u"\U0001F539" + 'Please enter the start date of the emergency plan you want to view and then delete in the format of yyyy-mm-dd: ')
                 elif self.choice == '3':
                    loop = False
                    typeframe = pd.read_csv('emergency_plan_1.csv')
                    print(f'The choices of type are: {set(typeframe.Area.values)}.')
                    self.area = input(u"\U0001F539" + 'Please enter the area of the emergency plan you want to view and then delete: ')
                    loop1 = True
                    while loop1 == True:
                            try:
                                if self.area in typeframe.Area.values:
                                    loop1 = False
                                    finalframe = typeframe[typeframe['Area'] == self.area]
                                    finalframe = finalframe.reset_index(drop = True)
                                    print(finalframe)
                                    self.row = input(u"\U0001F539" + 'Please choose which row above you want to delete: ')
                                    date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
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
                                                            print_log(e)
                                                            self.row = input(u"\U0001F539" + 'Please enter your choice: ')
                                            else: 
                                                raise Invalid_input(date_format)
                                        except Invalid_input as e:
                                            print_log(e)
                                            date_format = input(u"\U0001F539" + 'Please enter the close date of the emergency plan in the format of yyyy-mm-dd: ') 
                                            date = date_format.split('-')
                                else: 
                                    raise Invalid_input(self.area)
                            except Invalid_input as e:
                                 print_log(e)
                                 self.area = input(u"\U0001F539" + 'Please enter the area of the emergency plan you want to view and then delete: ')
                 else: 
                        raise Invalid_input(self.choice)
                except Invalid_input as e:
                    print_log(e)
                    self.choice = input(u"\U0001F539" + 'Please enter your choice: ')


         




        #Delete Plan in a future date 

    class Edit_Emergency_Plan:
         def __init__(self):
            self.type = input(u"\U0001F539" + 'Please choose which emergency plan to be edited: ')
        


plan = emergency_plan()
plan.selection()


    










