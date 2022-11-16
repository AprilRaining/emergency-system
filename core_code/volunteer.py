from myfunctionlib import *


class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __init__(self):
        """
        To Do:
        1. Process Login when construct a new admin
        2. Show the menu
        3. Maybe for first login require the volunteer to edit their personal information first.
        :return:
        """
        self.menu = menu(self.__class__.__name__)

    def sub_program(self):
        while True:
            print(self.menu)
            match menu_choice_get(menu(self.__class__.__name__).count('\n') + 1):
                case 1:
                    self.manage_personal_information()
                case 2:
                    self.manage_camp_file()
                case 0:
                    return

    def manage_personal_information(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    pass
                case 2:
                    pass
                case 0:
                    return

    def manage_camp_file(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    pass
                case 2:
                    pass
                case 0:
                    return
