from datetime import datetime
import datetime
from myfunctionlib import *
import sqlite3 as db



class Volunteer:
    """
    This is class for volunteer to operate the system.
    """

    def __init__(self):
        """
        To Do:
        1. Process Login when construct a new admin
        2. Show the menu
        3. Maybe for first login require the volunteer to edit their personal information first.
        :return:
        """
        self.menu = menu(self.__class__.__name__)
        self.volunteerID = None

    def sub_main(self):
        while True:
            print(self.menu)
            match menu_choice_get(self.menu.count('\n') + 1):
                case 1:
                    self.manage_personal_information()
                case 2:
                    self.manage_camp_file()
                case 3:
                    self.manage_task()
                case 0:
                    return

    def manage_personal_information(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.edit_my_information()
                case 2:
                    self.show_my_information()
                case 0:
                    return

    def edit_my_information(self):
        pass

    def show_my_information(self):
        pass

    def manage_camp_file(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    self.create_emergency_refugee_file()
                case 2:
                    self.edit_emergency_refugee_file()
                case 3:
                    self.close_emergency_refugee_file()
                case 4:
                    self.delete_emergency_refugee_file()
                case 0:
                    return

    def create_emergency_refugee_file(self):
        pass

    def edit_emergency_refugee_file(self):
        pass

    def close_emergency_refugee_file(self):
        pass

    def delete_emergency_refugee_file(self):
        pass

    def manage_task(self):
        while True:
            print(menu())
            match menu_choice_get(menu().count('\n') + 1):
                case 1:
                    volunteer_id = input("Enter ur ID")
                    self.view_my_schedule(volunteer_id)
                case 0:
                    return

    def view_my_schedule(self, ID):
        def get_current_weekday():
            monday = datetime.date.today()
            one_day = datetime.timedelta(days=1)
            while monday.weekday() != 0:
                monday -= one_day
            tuesday = monday + one_day
            wednesday = tuesday + one_day
            thursday = wednesday + one_day
            friday = thursday + one_day
            saturday = friday + one_day
            sunday = saturday + one_day

            return datetime.datetime.strftime(monday, "%Y-%m-%d"), datetime.datetime.strftime(tuesday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(wednesday, "%Y-%m-%d"), datetime.datetime.strftime(thursday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(friday, "%Y-%m-%d"), datetime.datetime.strftime(saturday, "%Y-%m-%d"), \
                   datetime.datetime.strftime(sunday, "%Y-%m-%d")

        def display_schedule(volunteer, day, date):
            try:
                with db.connect('emergency_system.db') as conn:
                    c = conn.cursor()
                    c.execute(f'''SELECT * FROM task WHERE volunteerID = (?) and startDate = (?)''', (volunteer, date))
                    task = c.fetchall()
                    task_info = task[0][3]
                    task_schedule = task[0][5]
                if task_schedule == 'morning':
                    day_schedule = [day, task_info, '/', '/']
                elif task_schedule == 'afternoon':
                    day_schedule = [day, '/', task_info, '/']
                elif task_schedule == 'night':
                    day_schedule = [day, '/', '/', task_info]
            except IndexError:
                day_schedule = [day, '/', '/', '/']
            return day_schedule

        date_monday = get_current_weekday()[0]
        date_tuesday = get_current_weekday()[1]
        date_wednesday = get_current_weekday()[2]
        date_thursday = get_current_weekday()[3]
        date_friday = get_current_weekday()[4]
        date_saturday = get_current_weekday()[5]
        date_sunday = get_current_weekday()[6]

        d = []
        d.append(display_schedule(1, 'Monday', date_monday))
        d.append(display_schedule(1, 'Tuesday', date_tuesday))
        d.append(display_schedule(1, 'Wednesday', date_wednesday))
        d.append(display_schedule(1, 'Thursday', date_thursday))
        d.append(display_schedule(1, 'Friday', date_friday))
        d.append(display_schedule(1, 'Saturday', date_saturday))
        d.append(display_schedule(1, 'Sunday', date_sunday))

        print("{:<15} {:<15} {:<15} {:<15}".format('Day', 'Morning(06:00 - 14:00)',
                                                   'Afternoon(14:00 - 22:00)', 'Night(22:00 - 06:00)'))

        for v in d:
            day, morning, afternoon, night = v
            print("{:<15} {:<22} {:<24} {:<15}".format(day, morning, afternoon, night))


