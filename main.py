import os
import sys
import pandas as pd
from system_log import *
import utilities
from admin import Admin
from myfunctionlib import *
from volunteer import Volunteer

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)

# sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    """
    TO DO (Possible):
    Some Initialisation staff for the WHOLE program.
    1. update status of plans
    2. update time schedule of all volunteers
    """

    # For Log in
    utilities.check_plan()
    utilities.check_week()

    try:
        while True:
            prCyan("""
 ____      ____ ________ _____      ______   ___   ____    ____ ________
|_  _|    |_  _|_   __  |_   _|   .' ___  |.'   `.|_   \  /   _|_   __  |
  \ \  /\  / /   | |_ \_| | |    / .'   \_/  .-.  \ |   \/   |   | |_ \_|
   \ \/  \/ /    |  _| _  | |   _| |      | |   | | | |\  /| |   |  _| _
    \  /\  /    _| |__/ |_| |__/ \ `.___.'\  `-'  /_| |_\/_| |_ _| |__/ |
     \/  \/    |________|________|`.____ .'`.___.'|_____||_____|________|

                                                   """)
            print('\t\tto the Emergency System Designed By Team K:)\n')
            print("--------------------------------------------------------------------------\n")
            prYellow(u"\U0001F539"+"Please select the account type to login :\n")
            print(menu('Login'))
            match menu_choice_get(menu('Login').count('\n') + 1, "\n-->"):
                case 1:
                    utilities.admin_login()
                    admin = Admin()
                    admin.sub_main()
                case 2:
                    v_ID = utilities.volunteer_login()
                    if v_ID < 0:
                        continue
                    volunteer = Volunteer(volunteer_id=v_ID)
                    volunteer.sub_main()
                case 0:
                    break
    except KeyboardInterrupt:
        print_log('\nForce Quit!')
    # except Exception as e:
    #     print('\nExit with unknown errors')
    #     print(e)
    finally:
        pass
