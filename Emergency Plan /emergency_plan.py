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
        print("3. Close Emergency Plan.")
        self.user = input('Please enter your choice: ')
        try:
            if int(self.user) == 1:
                create = self.Create_Emergency_Plan()
                create.add()
            elif int(self.user) == 2:
                display = self.Display_Emergency_Plan()
                display
            elif int(self.user) == 3:
                delete = self.Delete_Emergency_Plan()
                delete
            else:
                raise Invalid_input(self.user)
        except Invalid_input as e:
            print(e)
                
        

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
        
        def add(self):
            dataframe = pd.DataFrame(data = None, columns=np.array(['Type', 'Description', 'Geographical Area', 'Start Date']))
            print(dataframe)
        
        

    class Display_Emergency_Plan:
        def __init__(self):
            self.type = input('Please choose which emergency plan to be displayed: ')
 
    class Delete_Emergency_Plan:
         def __init__(self):
            self.type = input('Please choose which emergency plan to be deleted: ')
        


plan = emergency_plan()
plan.selection()


    










