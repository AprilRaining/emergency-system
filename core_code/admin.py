import numpy as np
import pandas as pd

from myfunctionlib import *


class Admin:
    """
        This is the admin class for admin program.
    """

    def __init__(self):
        """
        TO DO:
        1. Process Login when construct a new admin
        2. Show the menu
        :return:
        """
        # Process Login. If fail more than 5 times. Exit
        # Get Menu
        self.menu = menu(self.__class__.__name__)
        self.emergency_plan_csv = '../info_files/emergency_plan.csv'

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(menu(self.__class__.__name__).count('\n') + 1):
                case 1:
                    self.manage_emergency_plan()
                case 2:
                    self.manage_account()
                case 0:
                    return

    def manage_emergency_plan(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.create_emergency_plan()
                case 2:
                    self.edit_emergency_plan()
                case 3:
                    self.display_all_emergency_plans()
                case 4:
                    self.close_emergency_plan()
                case 5:
                    self.delete_emergency_plan()
                case 0:
                    return

    def create_emergency_plan(self):
        type = input('Please enter the type of Emergency: ')
        desc = input('Please enter the description of the emergency plan: ')
        area = input('Please enter the geographical area affected by the natural disater: ')
        date = get_data('Please enter the start date of the emergency plan in the format of yyyy-mm-dd: ')
        refugee = get_int('Please enter the number of refugees at the camp: ')
        volunteer = get_int('Please enter the number of volunteers required at the camp: ')
        dataframe = pd.DataFrame(data=None,
                                 columns=np.array(['Type', 'Description', 'Area', 'Start Date', '# refugees',
                                                   '# humanitarian volunteers']))
        if ((dataframe['Type'] == type) & (dataframe['Description'] == desc)
            & (dataframe['Area'] == area) & (dataframe['Start Date'] == date)
            & (dataframe['# refugees'] == refugee) & (
                    dataframe['# humanitarian volunteers'] == volunteer)).any():
            print(dataframe)
        else:
            new_dataframe = pd.DataFrame({'Type': [type], 'Description': [desc],
                                          'Area': [area], 'Start Date': [date],
                                          '# refugees': [refugee],
                                          '# humanitarian volunteers': [volunteer]})
            dataframe = pd.concat([dataframe, new_dataframe], ignore_index=False)
            dataframe.to_csv('../info_files/emergency_plan.csv', mode='a', header=False)

    def edit_emergency_plan(self):
        df = pd.read_csv('../info_files/emergency_plan.csv', index_col=0)
        print(df)
        index_plan = menu_choice_get(df.to_string().count('\n'), hint='Please choice which plan you want to change: ')
        self.display_one_emergency_plan_in_detail(index_plan)
        index_argument = menu_choice_get(5, hint='Please choice which one you want to edit: ')
        print(df.loc[index_plan])
        print(df.loc[index_plan].values[index_argument])
        df.iloc[index_plan, index_argument] = input('Please input new value:')
        df.to_csv('../info_files/emergency_plan.csv')
        back()

    def display_one_emergency_plan_in_detail(self, index):
        df = pd.read_csv('../info_files/emergency_plan.csv', index_col=0)
        for i in range(len(df.columns.values)):
            print('{}. {}:{}'.format(i, df.columns.values[i], df.loc[index].values[i]))

    def display_all_emergency_plans(self):
        df = pd.read_csv('../info_files/emergency_plan.csv', index_col=0)
        print(df)
        back()

    def close_emergency_plan(self):
        pass

    def delete_emergency_plan(self):
        pass

    def manage_account(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.reactive_volunteer_account()
                case 2:
                    self.deactive_volunteer_account()
                case 3:
                    self.creat_a_volunteer_account()
                case 4:
                    self.display_volunteer_account()
                case 0:
                    return

    def reactive_volunteer_account(self):
        pass

    def deactive_volunteer_account(self):
        pass

    def creat_a_volunteer_account(self):
        pass

    def display_volunteer_account(self):
        pass
