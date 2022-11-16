from myfunctionlib import *
from admin import Admin
from volunteer import Volunteer


class Login:
    """
        This is the class used choose which type of account to log in.
    """

    def __init__(self):
        self.menu = menu(self.__class__.__name__)

    def sub_program(self):
        while True:
            print(self.menu)
            match menu_choice_get(menu(self.__class__.__name__).count('\n') + 1):
                case 1:
                    admin = Admin()
                    admin.sub_program()
                case 2:
                    volunteer = Volunteer()
                    volunteer.sub_program()
                case 0:
                    return


class StartProgram(object):
    """
        This is the class used to start the program and read files.
    """

    def __init__(self):
        """
        TO DO (Possible):
        Some Initialisation staff for the WHOLE program.
        """

    @staticmethod
    def sub_program():
        login = Login()
        login.sub_program()


if __name__ == "__main__":
    program = StartProgram()
    program.sub_program()
