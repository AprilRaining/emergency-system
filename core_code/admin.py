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

    def sub_program(self):
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
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 0:
                    return

    def manage_account(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 0:
                    return
