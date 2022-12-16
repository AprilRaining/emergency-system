import sqlite3 as db
from get import *
from myError import *
import re
from options import *
from system_log import *
from db_connect_ref import *
from print_table import *


class AccountCreation:

    @staticmethod
    def get_camp_id():
        while True:
            try:
                print("\n"+u"\U0001F531"+"INSTRUCTION: Please assign the camp identification to the volunteer.")
                print("The detail below shows the availability of each camp as well as its related conditions:\n")

                with db.connect('emergency_system.db') as conn:

                    camp_df = display_open_camp_option(conn)
                    camp_df_cop = camp_df.copy()
                    print_table(camp_df_cop.columns,camp_df_cop.to_numpy().tolist(),(25,25,70,70,70,40))
                    print("--------------------------------------------------------------------\n")
                    campID = Get.int(u"\U0001F539"+'Enter the camp ID:')
                    camp_id = (campID,)

                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM camp WHERE campID = (?)''', camp_id)
                    camp_existence = c.fetchall()
                    camp_capacity = camp_existence[0][1]
                if len(camp_existence) == 0:
                    raise IndexError
                else:
                    with db.connect('emergency_system.db') as conn:
                        c = conn.cursor()
                        c.execute(f'''SELECT * FROM volunteer WHERE campID = (?)''', camp_id)
                        camp_current = c.fetchall()
                    if len(camp_current) < camp_capacity:
                        pass
                    else:
                        raise CampCapacityError(campID)
                break
            except IndexError:
                print_log("Camp not existed")
            except CampCapacityError as e:
                print(e)

        return campID

    @staticmethod
    def get_username():
        while True:
            try:
                username = input(u"\U0001F539"+'Enter the username:')
                if username == "":
                    print("The username can not be empty, Please input again:")
                    continue
                user_name = (username,)
                with db.connect('emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM volunteer WHERE username = (?)''', user_name)
                    user_exist = c.fetchall()
                if len(user_exist) != 0:
                    raise IndexError
                break
            except IndexError:
                print_log("User name already existed")
        return username

    @staticmethod
    def preference_default():
        preference = {}
        preference.setdefault('Monday')
        preference.setdefault('Tuesday')
        preference.setdefault('Wednesday')
        preference.setdefault('Thursday')
        preference.setdefault('Friday')
        preference.setdefault('Saturday')
        preference.setdefault('Sunday')
        preference.setdefault('workShift')
        return preference

    @staticmethod
    def get_work_day(day):
        while True:
            try:
                work_or_not = input(u"\U0001F539"+"Will this volunteer work on {}? (Enter 'Y/y' as yes, 'N/n' as no) \n".format(day))
                if work_or_not == 'Y' or work_or_not == 'y':
                    choice = 1
                elif work_or_not == 'N' or work_or_not == 'n':
                    choice = 0
                else:
                    raise InvalidInput(work_or_not)
            except InvalidInput as e:
                print(e)
            else:
                return choice

    @staticmethod
    def get_week_preference():
        preference = {"Monday": -1,
                      "Tuesday": -1,
                      "Wednesday": -1,
                      "Thursday": -1,
                      "Friday": -1,
                      "Saturday": -1,
                      "Sunday": -1
                      }
        weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        while True:
            try:
                print(u"\U0001F4C6","Working Day Options")
                opt_second = Options([
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday',
                        'Sunday',
                        'Not available this week'
                    ])
                print(opt_second)
                input_str = input(u"\U0001F539"+"Please input the day(s) this volunteer is available in a week(from 1 to 7).\n"
                              "For example, 6,7 means Saturday and Sunday are available. \n"
                              "If there is no available day, just press 8: \n--> ")
                if input_str == '8':
                    print("You're not available this week!\n")
                    return preference
                if "," not in input_str:
                    if int(input_str)>8 or int(input_str)<1:
                        warn("Wrong input, check your input please!\n")
                        raise InvalidChoiceError(input_str)
                else:
                    for d in input_str.split(","):
                        if int(d) == 8:
                            raise InvalidChoiceError(d)
                        if int(d)>7 or int(d)<1:
                            # warn("Wrong input, check your input please!\n")
                            raise InvalidChoiceError(d)
                        else:
                            match_result = re.match(re.compile("^[1-7]*$"), d)
                            if match_result:
                                for i in match_result.group():
                                    preference[weekday_list[int(i)-1]] = 0
                            else:
                                warn("Wrong input, check your input please!\n")
                                raise InvalidChoiceError(d)
            except ValueError as e:
                print_log("Your input is invalid, please try again!")
            except InvalidChoiceError as e:
                print_log("""You input is invalid. Please input a numerical value within a range 1 to 8.
                And you cannot input '8' (unavailable) with other options.!\n""")
            else:
                print("\nAccording your input, you are available in these day(s):", [day for day, flag in preference.items() if flag == 0])
                return preference
            

    @staticmethod
    def get_work_shift():
        while True:
            try:
                work_shift = input("\n"+u"\U0001F539"+"What will be a work shift for the volunteer? \n 1. Morning (06:00-14:00) \n "
                                   "2. Afternoon (14:00-22:00) \n 3. Night (22:00-06:00) \n--> ")
                if work_shift == '1':
                    shift = 'Morning'
                elif work_shift == '2':
                    shift = 'Afternoon'
                elif work_shift == '3':
                    shift = 'Night'
                else:
                    raise InvalidChoiceError(work_shift)
            except InvalidChoiceError as e:
                print_log("You input is invalid. Please input a numerical value within a range 1 to 3.")
                print(e)
            else:
                return shift


    @staticmethod
    def confirm_deletion():
        while True:
            try:
                work_or_not = input("\n"+u"\U0001F539"+"Do you confirm to delete this account? (Enter 'Y/y' as yes, 'N/n' as no): ")
                if work_or_not == 'Y' or work_or_not == 'y':
                    choice = 1
                elif work_or_not == 'N' or work_or_not == 'n':
                    choice = 0
                else:
                    raise InvalidInput(work_or_not)
            except InvalidInput as e:
                print_log("You input is invalid. Please try again!.")
                print(e)
            else:
                return choice