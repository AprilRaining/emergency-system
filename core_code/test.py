#
# # import the module
# import textwrap
# import pandas as pd
# from print_table import *
#
# # create a DataFrame
# ODI_runs = {'name': ['Tendulkar', 'Sangakkara', 'Ponting',
#                      'Jayasurya', 'Jayawardene', 'Kohli',
#                      'Haq', 'Kallis', 'Ganguly', 'Dravid'],
#             'runs': [18426, 14234, 13704, 13430, 12650,
#                      11867, 11739, 11579, 11363, 10889]}
# df = pd.DataFrame(ODI_runs)
#
# # making a yellow border
# # df.style.set_table_styles([{'selector' : '',
# #                             'props' : [('border',
# #                                         '10px solid yellow')]}])
# print(df.head(10).style.set_properties(**{'background-color': 'black',
#                                           'color': 'lawngreen',
#                                           'border-color': 'white'}))
#
# # Create an empty list
# Row_list = df.to_numpy().tolist()
#
#
# # Print the list
# print(Row_list)
# print_table(df.columns, Row_list, (15, 15))
#
#
# # ...
#
# import datetime
# now = datetime.datetime.now()
# today = datetime.date.today()
# date_format = today.strftime("%Y-%m-%d")
# print(date_format)
#
#
# def getCalendarHeader():
#     print
#     """
#     BEGIN:VCALENDAR
#     PRODID:-//Atlassian Software Systems//Confluence Calendar Plugin//EN
#     VERSION:2.0
#     CALSCALE:GREGORIAN
#     X-WR-CALNAME;VALUE=TEXT:
#     X-WR-CALDESC;VALUE=TEXT:
#     """
#
#
# getCalendarHeader()
#
# # from termcolor import colored
# # print(colored('python', 'green', attrs=['bold']))
#
# value = "ggg"
#
# print(f"\033[91m {value} is an invalid input.\nPlease reenter.\033[00m")

import datetime

datetime.date.today()