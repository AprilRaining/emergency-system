import numpy as np
import pandas as pd
import datetime 

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
               if (2000 <= int(date[0])) and (1 <= int(date[1]) <= 12) and (1 <= int(date[2]) <= 31):
                self.date= datetime.date(int(date[0]), int(date[1]), int(date[2]))
               else:
                raise Invalid_input(date_format)
            except Invalid_input as e:
                print(e)
            try:
                refugee = input('Please enter the number of refugees at the camp: ')
                if refugee.isdigit():
                    self.refugee = refugee
                else:
                    raise Invalid_input(refugee)
            except Invalid_input as e:
                print(e)
            try:
                volunteer = input('Please enter the number of volunteers required at the camp: ')
                if volunteer.isdigit():
                    self.volunteer = volunteer
                else:
                    raise Invalid_input(volunteer)
            except Invalid_input as e:
                print(e)
            
        
        def add(self):
            dataframe = pd.DataFrame(data = None, columns=np.array(['Type', 'Description', 'Area', 'Start Date', '# refugees', 
            '# humanitarian volunteers']))
            if ((dataframe['Type'] == self.type) & (dataframe['Description'] == self.desc)
            & (dataframe['Area'] == self.area) & (dataframe['Start Date'] == self.date)
            & (dataframe['# refugees'] == self.refugee) & (dataframe['# humanitarian volunteers'] == self.volunteer)).any():
                print(dataframe)
                
            else: 
                new_dataframe = pd.DataFrame({'Type': [self.type], 'Description': [self.desc],
                'Area': [self.area], 'Start Date': [self.date],
                '# refugees': [self.refugee], '# humanitarian volunteers': [self.volunteer]})
                dataframe = pd.concat([dataframe, new_dataframe], ignore_index
                = False)
                print(dataframe)
        

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input('Please choose which emergency plan to be displayed: ')
 
    class Delete_Emergency_Plan:
         def __init__(self):
            self.type = input('Please choose which emergency plan to be deleted: ')

    class Edit_Emergency_Plan:
         def __init__(self):
            self.type = input('Please choose which emergency plan to be edited: ')
        


plan = emergency_plan()
plan.selection()


    










