import inspect

from myError import *


def menu(name=''):
    """
    This function used to store data about UI and return them as a string.
    If there is no input value for name, the name will be the function which called this function(menu).
    :return: string
    """
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
                '2. Edit Emergency Plan.\n'
                '3. Display Emergency Plan.\n'
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
