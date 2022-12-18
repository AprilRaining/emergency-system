import pandas as pd
import utilities
from admin import Admin
from myfunctionlib import *
from volunteer import Volunteer

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
            print(
                "--------------------------------------------------------------------------\n")
            prYellow(u"\U0001F539"+"Please select the account type to login :\n")
            print(menu('Login'))
            match menu_choice_get(menu('Login').count('\n') + 1, "\n-->"):
                case 1:
                    utilities.admin_login()
                    admin = Admin()
                    admin.sub_main()
                case 2:
                    volunteerInfo = utilities.volunteer_login()
                    if volunteerInfo[0] < 0:
                        continue
                    volunteer = Volunteer(
                        volunteer_id=volunteerInfo[0], campID=volunteerInfo[2], planID=volunteerInfo[3])
                    volunteer.sub_main()
                case 0:
                    break
    except KeyboardInterrupt:
        print_log('\nForce Quit!')
<<<<<<< HEAD
    except Exception as e:
        warn('\nExit with unknown errors')
        print_log(str(e))
=======
    # except Exception as e:
    #     warn('\nExit with unknown errors')
    #     print(e)
>>>>>>> junfeng
    finally:
        pass
