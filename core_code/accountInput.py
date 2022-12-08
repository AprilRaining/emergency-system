import sqlite3 as db
from get import *
from myError import *
import re


class AccountCreation:

    @staticmethod
    def get_camp_id():
        while True:
            try:
                campID = Get.int('Enter the campID:')
                camp_id = (campID,)

                with db.connect('info_files/emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM camp WHERE campID = (?)''', camp_id)
                    camp_existence = c.fetchall()
                    camp_capacity = camp_existence[0][1]
                if len(camp_existence) == 0:
                    raise IndexError
                else:
                    with db.connect('info_files/emergency_system.db') as conn:
                        c = conn.cursor()
                        c.execute(f'''SELECT * FROM volunteer WHERE campID = (?)''', camp_id)
                        camp_current = c.fetchall()
                    if len(camp_current) < camp_capacity:
                        pass
                    else:
                        raise CampCapacityError(campID)
                break
            except IndexError:
                print("Camp not existed")
            except CampCapacityError as e:
                print(e)

        return campID

    @staticmethod
    def get_username():
        while True:
            try:
                username = input('Enter the username:')
                if username == "":
                    print("The username can not be empty, Please input again:")
                    continue
                user_name = (username,)
                with db.connect('info_files/emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM volunteer WHERE username = (?)''', user_name)
                    user_exist = c.fetchall()
                if len(user_exist) != 0:
                    raise IndexError
                break
            except IndexError:
                print("User name already existed")
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
                work_or_not = input("Will this volunteer work on {}? (Enter 'Y/y' as yes, 'N/n' as no) \n".format(day))
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
            input_str = input("Please input the number of day you are available in a week(from 1 to 7).\n"
                              "For example, 6 means Saturday is available. \n"
                              "If there is no day are available, just press enter:\n")
            input_str = input_str.replace(" ", "")
            if input_str == "":
                return preference
            match_result = re.match(re.compile("^[1-7]*$"), input_str)
            if match_result:
                for i in match_result.group():
                    preference[weekday_list[int(i)-1]] = 0
                print("According your input, you are available in these day(s): ")
                for day, flag in preference.items():
                    if flag == 0:
                        print(day)
                return preference
            else:
                print("Wrong input, check your input please!\n")

    @staticmethod
    def get_work_shift():
        while True:
            try:
                work_shift = input("What will be the shift for the volunteer? \n 1. Morning (06:00-14:00) \n "
                                   "2. Afternoon (14:00-22:00) \n 3. Night (22:00-06:00) \n")
                if work_shift == '1':
                    shift = 'morning'
                elif work_shift == '2':
                    shift = 'afternoon'
                elif work_shift == '3':
                    shift = 'night'
                else:
                    raise InvalidChoiceError(work_shift)
            except InvalidChoiceError as e:
                print(e)
            else:
                return shift
