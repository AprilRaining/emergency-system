import sys


class OutOfRangeError(Exception):
    def __init__(self, input):
        Exception.__init__(self)
        self.input = input

    def __str__(self):
        return f'{self.input} is an invalid choice.\nPlease reenter a number specified above.'


def MenuChoiceGet(r):
    while True:
        try:
            choice = int(input())
            if choice not in range(r):
                raise OutOfRangeError(choice)
        except ValueError:
            print("You entered a non-numeric value.")
            print("Please reenter a valid Number")
        except OutOfRangeError as e:
            print(e)
        else:
            return choice


def menu(name):
    match name:
        case 'Login':
            return (
                '1. Admin\n'
                '2. Volunteer\n'
                '0. Exit'
            )
        case 'Admin':
            return (
                '1. Manage Plans.\n'
                '2. Manage Account.\n'
                '0. Exit'
            )


class Login:
    """
        This is the class used to Log in.
    """

    def __init__(self):
        print(menu(self.__class__.__name__))

    def sub_program(self):
        match MenuChoiceGet(menu(self.__class__.__name__).count('\n') + 1):
            case 1:
                try:
                    admin = Admin()
                except Exception:
                    sys.exit()
                else:
                    admin.sub_program()
            case 2:
                try:
                    volunteer = Volunteer()
                except Exception:
                    sys.exit()
                else:
                    volunteer.sub_program()
            case 0:
                sys.exit()


class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __int__(self):
        """
        1. Process Login when construct a new admin
        2. Show the menu
        :return:
        """
    def sub_program(self):
        pass

class Admin:
    """
        This is the admin class for admin program.
    """

    # MENU_NAME = 'admin_main'

    def __init__(self):
        """
        TO DO:
        1. Process Login when construct a new admin
        2. Show the menu
        :return:
        """
        # Process Login. If fail more than 5 times. Exit
        # Show Menu
        print(menu(self.__class__.__name__))

    def sub_program(self):
        match MenuChoiceGet(menu(self.__class__.__name__).count('\n') + 1):
            case 1:
                pass
            case 2:
                pass
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
