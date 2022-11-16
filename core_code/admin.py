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
                    self.display_emergency_plan()
                case 4:
                    self.close_emergency_plan()
                case 5:
                    self.delete_emergency_plan()
                case 0:
                    return

    def create_emergency_plan(self):
        pass

    def edit_emergency_plan(self):
        pass

    def display_emergency_plan(self):
        pass

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
