import sys

from admin import Admin
from myfunctionlib import *
from volunteer import Volunteer

if __name__ == "__main__":
    """
    TO DO (Possible):
    Some Initialisation staff for the WHOLE program.
    """
    # For Log in
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
                # To Do: Before Quitting Do something?
                sys.exit()
