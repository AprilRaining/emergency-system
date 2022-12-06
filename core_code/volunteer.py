import datetime

from myfunctionlib import *
from get import *
import sqlite3
import json
from options import *


def connection_database(db_file):
  # create the connection between database and python#
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    print("database connected successfully!")
  except Exception as e:
    print("could not connect to the database")
    print(e)
  return conn


class Volunteer:
  """
      This is class for volunteer to operate the system.
    """

  def __init__(self, last_name, first_name, password, campID, workingShift, workingdays, volunteerID):
    self.last_name = last_name
    self.first_name = first_name
    self.password = password
    self.campID = campID
    self.workingShift = workingShift
    self.workingdays = workingdays
    self.volunteerID = volunteerID

    self.menu = menu(self.__class__.__name__)

  def sub_main(self):
    while True:
      print(self.menu)
      match menu_choice_get(self.menu.count('\n') + 1):
        case 1:
          self.manage_personal_information()
        case 2:
          self.manage_camp_file()
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
    while True:
      print(menu())
    match menu_choice_get(menu('edit_my_information').count('\n') + 1):
      case 1:
        self.edit_volunteers_name()
      case 2:
        self.edit_password()
      case 3:
        self.edit_working_perference()
      case 4:
        self.edit_campid()
      case 0:
        return

  def edit_volunteers_name(self):
    conn = connection_database("../info_files/emergency_system.db")
    cur = conn.cursor()
    volunteer_input_id = input("please input your volunteer id to confirm whose information you want to change:\n")
    last_name = input("please input your new last name:\n")
    first_name = input("please input your new first name:\n")
    self.last_name = last_name
    self.first_name = first_name

    query = f'''UPDATE volunteer SET fName='{first_name}',lName='{last_name}' WHERE volunteerID = {volunteer_input_id}'''
    cur.execute(query)
    conn.commit()
    cur.close()

  def edit_password(self):
    conn = connection_database("../info_files/emergency_system.db")
    cur = conn.cursor()
    volunteer_input_id = input("please input your volunteer id to confirm whose information you want to change:\n")
    new_password = input("please input your new password\n")
    self.password = new_password
    query = f'''UPDATE volunteer SET password ='{new_password}' WHERE volunteerID = {volunteer_input_id}'''
    cur.execute(query)
    conn.commit()
    cur.close()

  def edit_working_perference(self):
    conn = connection_database("../info_files/emergency_system.db")
    cur = conn.cursor()

    preference = {'Monday': -1,
                  'Tuesday': -1,
                  'Wednesday': -1,
                  'Thursday': -1,
                  'Friday': -1,
                  'Saturday': -1,
                  'Sunday': -1,
                  'workShift': "Morning shift"}  # used to store the json information


    while True:
      volunteer_input_id = input("please input your volunteer id to confirm your identity:\n")
      query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
      cur.execute(query_1)

      weekday = cur.fetchall()

      if weekday == []:
        print("you input the wrong volunteerID please try again:\n")
        continue
      else:
        break
    the_day = datetime.datetime.now().weekday()
    print("today is weekday:" + str(the_day + 1))


    for the_day in range(the_day, 6):
      judge = weekday[0][the_day]
      if judge > 0:
        print("you cannot change your working shift because you still have unfinished work")
        break
    else:
      if confirm("you can change your preference now,please press y to continue:\n"):

        print("please select your prefer day to work:\n"
              "1.Monday\n"
              "2.Tuesday\n"
              "3.Wednesday\n"
              "4.Thursday\n"
              "5.Friday\n"
              "6.Saturday\n"
              "7.Sunday\n")
        options = Get.list(1, 8, "please input your option in format with number and split by space button! \n")

      else:
        return

      match = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
      for i in options:
        preference[match[i]] = 0

      preference_json = json.dumps(preference)
      print(preference_json)
      query = f'''UPDATE volunteer SET preference='{preference_json}' WHERE volunteerID = {volunteer_input_id}'''
      cur.execute(query)
      conn.commit()

      print("you successfully changed your next weeks working day!\n")

      options_shift = Options([
        'Morning shift',
        'Evening shift',
        'Night shift'

      ], limited=True)
      print(options_shift)
      options_preference = options_shift.get_option("please choose your preferred workShift\n")

      match_preference = ['Morning shift', 'Evening shift', 'Night shift']

      preference['workShift'] = match_preference[options_preference]

      preference = json.dumps(preference)
      query = f'''UPDATE volunteer SET preference='{preference}' WHERE volunteerID = {volunteer_input_id}'''
      cur.execute(query)
      conn.commit()
      cur.close()

  def edit_campid(self):
    conn = connection_database("../info_files/emergency_system.db")
    cur = conn.cursor()
    volunteer_input_id = input("please input your volunteer id to confirm whose information you want to change:\n")

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
