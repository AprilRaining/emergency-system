import sys

from admin import Admin
from myfunctionlib import *
from volunteer import Volunteer

if __name__ == "__main__":
    """
    TO DO (Possible):
    Some Initialisation staff for the WHOLE program.
    1. update status of plans
    2. update time schedule of all volunteers
    3. update last login time
    """
    # For Log in
    try:
        while True:
            print(menu('Login'))
            match menu_choice_get(menu('Login').count('\n') + 1):
                case 1:
                    admin = Admin()
                    admin.sub_main()
                case 2:
                    volunteer = Volunteer()
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
