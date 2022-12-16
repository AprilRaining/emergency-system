import datetime
import inspect
import sqlite3

from myError import *
from system_log import *

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
                '[ 1.] Admin\n'
                '[ 2.] Volunteer\n'
                '[ 0.] Exit'
            )
        case 'Admin':
            return (
                '[ 1.] Manage Emergency Plans.\n'
                '[ 2.] Manage Accounts.\n'
                '[ 0.] Exit'
            )
        case 'Volunteer':
            return (
                '[ 1.] Manage Personal Information.\n'
                '[ 2.] Manage Refugees and Camp File.\n'
                '[ 3.] Manage Tasks (Refugee Request).\n'
                '[ 0.] Exit'
            )
        case 'ManageEmergencyPlan':
            return (
                '[ 1.] Create Emergency Plan.\n'
                '[ 2.] Edit Emergency Plan.\n'
                '[ 3.] View Emergency Plan.\n'
                '[ 4.] Close Or Open Emergency Plan.\n'
                '[ 5.] Delete Emergency Plan.\n'
                '[ 0.] Exit'
            )
        case 'manage_account':
            return (
                '[ 1.] Reactivate Volunteer Account.\n'
                '[ 2.] Deactivate Volunteer Account.\n'
                '[ 3.] Create A New Volunteer Account.\n'
                '[ 4.] Display Volunteer Account.\n'
                '[ 5.] Delete volunteer account.\n'
                '[ 0.] Exit'
            )
        case 'display_volunteer_account':
            return (
                '[ 1.] Display Account By Volunteer ID.\n'
                '[ 2.] Display Account By Camp ID.\n'
                '[ 3.] Display All Accounts.\n'
                '[ 0.] Exit'
            )
        case 'manage_personal_information':
            return (
                '[ 1.] Edit My Information.\n'
                '[ 2.] Show My Information.\n'
                '[ 0.] Exit'
            )
        case 'edit_my_information':
            return (
                '[ 1.] Edit volunteer name.\n'
                '[ 2.] Edit volunteer password.\n'
                '[ 3.] Pick volunteer working time.\n'
                '[ 4.] Edit volunteer campID.\n'
                '[ 0.] Exit'
            )
        case 'manage_camp_file':
            return (
                '[ 1.] Create Refugee Account.\n'
                '[ 2.] Edit Refugee Information.\n'
                '[ 3.] View Refugee Request Schedule.\n'
                '[ 4.] Deactivate Refugee Account.\n'
                '[ 5.] Activate Refugee Account.\n'
                '[ 6.] Delete Refugee Account.\n'
                '[ 0.] Exit'
            )
        case 'manage_task':
            return (
                '[ 1.] View this week schedule.\n'
                '[ 0.] Exit'
            )


def menu_choice_get(span, hint=''):
    """
    This function will make sure the user input is a number between 0 to the size of the menu,
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
            print_log("You entered a non-numeric value.")
            print_log("Please reenter a valid Number")
        except InvalidChoiceError as e:
            print(e)
        else:
            return option


def confirm(hint=''):
    """
    This function used for confirmation.
    Y for confirm / Any key else for cancel operation
    Have this function to do the double check when exiting, but redundant this feature later.
    :return: Bool
    """
    print(hint)
    key = input("Enter Yes/yes to confirm your action: ")
    if key == 'Yes' or key == 'yes':
        return True
    else:
        return False


def back(hint=''):
    print(hint)
    while True:
        key = input('Input "Q/q" to go back:')
        if key == 'Q' or key == 'q':
            return


def search(table, column, keyword):
    result = []
    if type(keyword) == str:
        keyword = "'%{}%'".format(keyword)
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        for i in c.execute('select {}Id from {} where {} like {}'.format(
                table, table, column, keyword)).fetchall():
            result.append(i[0])
    return result


def list_to_sqlite_string(indexList):
    if type(indexList) == list:
        indexList = map(str, indexList)
        return '(' + ','.join(indexList) + ')'
    elif type(indexList) == int:
        return '({})'.format(indexList)


def to_date(date):
    if type(date) == str:
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
    else:
        return date
