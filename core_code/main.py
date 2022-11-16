import inspect


class OutOfRangeError(Exception):
    def __init__(self, input):
        Exception.__init__(self)
        self.input = input

    def __str__(self):
        return f'{self.input} is an invalid choice.\nPlease reenter a number specified above.'


def menu_choice_get(size):
    while True:
        try:
            choice = int(input())
            if choice not in range(size):
                raise OutOfRangeError(choice)
        except ValueError:
            print("You entered a non-numeric value.")
            print("Please reenter a valid Number")
        except OutOfRangeError as e:
            print(e)
        else:
            return choice


def double_check():
    """
    This function used for double_check.
    Y for confirm / Any key else for cancel operation
    :return: Bool
    """
    try:
        check = input('"Y/y" to confirm your action(any other key to cancel')
        if check == 'Y' or check == 'y':
            return True
        else:
            return False
    except Exception:
        # TO DO: Exception Handle
        pass


def menu(name=''):
    """
    This function used to store data about UI and return them as a string.
    :return: string
    """
    # if there is no input value for name, the name will be the function which called this function(menu).
    if len(name) == 0:
        name = inspect.stack()[1][3]
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
        case 'Volunteer':
            return (
                '1. Manage Personal Information.\n'
                '2. Manage Camp File\n'
                '0. Exit'
            )
        case 'manage_emergency_plan':
            return (
                '1. Create Emergency Plan.\n'
                '2. Display Emergency Plan.\n'
                '3. Edit Emergency Plan.\n'
                '4. Close Emergency Plan\n'
                '5. Delete Emergency Plan.\n'
                '0. Exit'
            )
        case 'manage_account':
            return (
                '1. Re-active Volunteer Account.\n'
                '2. De-active Volunteer Account.\n'
                '3. Create A New Volunteer Account.\n'
                '4. Display Volunteer Account.\n'
                '0. Exit'
            )
        case 'manage_personal_information':
            return (
                '1. Edit My Information.\n'
                '2. Show My Information.\n'
                '0. Exit'
            )
        case 'manage_camp_file':
            return (
                '1. Create Emergency Refugee File.\n'
                '2. Edit Emergency Refugee File.\n'
                '3. Close Emergency Refugee File.\n'
                '4. Delete Emergency Refugee File.\n'
                '0. Exit'
            )


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


class Login:
    """
        This is the class used to Log in.
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
