import sys
import os
import utilities

sys.path.insert(0, os.getcwd())
# print(sys.path)

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
    try:
        while True:
            print('Welcome to the emergency system designed by Team K:)\nPlease select the account type:')
            print(menu('Login'))
            match menu_choice_get(menu('Login').count('\n') + 1):
                case 1:
                    utilities.admin_login()
                    admin = Admin()
                    admin.sub_main()
                case 2:
                    v_ID = utilities.volunteer_login()
                    volunteer = Volunteer(volunteer_id=v_ID)
                    volunteer.sub_main()
                case 0:
                    break
    except KeyboardInterrupt:
        print('\nForce Quit!')
    except Exception as e:
        print('\nExit with unknown errors')
        print(e)
    finally:
        pass
