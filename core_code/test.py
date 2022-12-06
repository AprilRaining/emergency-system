import volunteer
import json
import datetime
import sqlite3
from get import *

# conn = volunteer.connection_database("edit_volunteers_name")
# v = volunteer.Volunteer('lu', 'jiaxuan', '123', 1, '123', 3, 6)
# v.edit_volunteers_name()
# volunteer.Volunteer.connection
#   conn=sqlite3.connect("emergency_system.db")
# c = conn.cursor()
# v = volunteer.Volunteer('lu', 'jiaxuan', '123', 1, '123', 3)
if __name__ == '__main__':
  conn = volunteer.connection_database("../info_files/emergency_system.db")

  cur = conn.cursor()
  v = volunteer.Volunteer('lu', 'jiaxuan', '123', 1, '123', 3, 6)
  v.edit_working_perference()
36


  # o = Get.list(1, 8)

  # v.edit_working_perference()
  # volunteer_input_id = input("please input your volunteer id to confirm your identity:\n")
  # query_1 = f'''SELECT Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday from volunteer WHERE volunteerID={volunteer_input_id}'''
  # cur.execute(query_1)
  # weekday = cur.fetchall()
  # print(list(weekday))
  # the_day = datetime.datetime.now().weekday()
  # print(the_day)
  # print(weekday[0][the_day])
  # for the_day in range(the_day, 6):
  #   judge = weekday[0][the_day]
  #   if judge > 0:
  #     print("你不能改")
  #     break
  # else:
  #     print("可以改")

  # v.edit_volunteers_name()
  # print("your new name is:" + v.first_name+" "+v.last_name)
  # v.edit_password()
  # print("your new password is:" + v.password)
