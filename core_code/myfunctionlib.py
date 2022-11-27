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
        case 'ManageEmergencyPlan':
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


def option_get(span, hint=''):
    """
    This function will make sure the user input would be a number between 0 to the size of the menu,
    otherwise it will ask the user to input again until a valid number is input.
    :param hint: String
    :param span: Int
    :return: Int
    """
    while True:
        try:
            option = int(input(hint))
            if option not in range(span):
                raise InvalidChoiceError(option)
        except ValueError:
            print("You entered a non-numeric value.")
            print("Please reenter a valid Number")
        except InvalidChoiceError as e:
            print(e)
        else:
            return option


def double_check():
    """
    This function used for double_check.
    Y for confirm / Any key else for cancel operation
    Have this function to do the double check when exiting, but redundant this feature later.
    :return: Bool
    """
    key = input('"Y/y" to confirm your action(any other key to cancel')
    if key == 'Y' or key == 'y':
        return True
    else:
        return False


def back():
    while True:
        key = input('Input "Q/q" to go back.')
        if key == 'Q' or key == 'q':
            return
