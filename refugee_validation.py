import refugee_exception as exc
from collections import OrderedDict
from myError import *
import sys
import datetime
import pandas as pd
from db_connect_ref import *
from system_log import *
from myfunctionlib import *
from refugee_utilities import *
from options import *
from print_table import *
from sqliteFunctions import *
from TableDisplayer import *


def refugee_existence_check(conn):
    while True:
        try:
            firstname = input(u"\U0001F539"+"Enter refugee's firstname: ")
            lastname = input(u"\U0001F539"+"Enter refugee's lastname: ")
            get_ref = f'''SELECT fName,lName FROM refugee WHERE fName = "{firstname}" AND lName = "{lastname}"'''
            pd_query = pd.read_sql_query(get_ref, conn)
            df_row = pd.DataFrame(pd_query, columns=["firstname", "lastname"])
            if df_row.empty == False:
                raise exc.refugee_duplicated_regis

        except exc.refugee_duplicated_regis:
            print_log("The refugee's firstname and lastname already exist in the database.\nPlease recheck if you're try to register the same person once again.")
            confirm = yn_valid(
                u"\U0001F539"+"Is this refugee the same person as whom you registered before?(Yes/No): ")
            if (confirm == "No"):
                return (firstname, lastname)
            else:
                cont = yn_valid(
                    u"\U0001F539"+"Would you like to continue the registration?(Yes/No): ")
                if (cont == "Yes"):
                    print("The process restarts!!!")
                else:
                    print("The process ends")
                    return
        except Exception as e:
            print_log(str(e))
        else:
            return (firstname, lastname)


def date_format_check(purpose, limit_start='', limit_end=''):
    while True:
        try:
            input_date = input(
                f"Enter refugee's {purpose} date (yyyy-mm-dd): ")
            bd_val = (input_date).split("-")
            if len(bd_val) != 3:
                raise exc.wrong_birthdate_format
            if (bd_val[2]) not in [format(x, '02d') for x in range(1, 32)]:
                raise exc.day_out_of_range
            if (bd_val[1]) not in [format(x, '02d') for x in range(1, 13)]:
                raise exc.month_out_of_range
            if limit_end != '' and limit_end != '':
                di, mi, yi = [int(x) for x in input_date.split('-')]
                date_inpt = datetime.date(di, mi, yi)
                ds, ms, ys = [int(x) for x in limit_start.split('-')]
                date_start = datetime.date(ds, ms, ys)
                de, me, ye = [int(x) for x in limit_end.split('-')]
                date_end = datetime.date(de, me, ye)
                if (date_inpt < date_start or date_inpt > date_end):
                    raise exc.date_not_available
        except ValueError:
            print_log("Incorrect date format, should be YYYY-MM-DD")
        except exc.wrong_birthdate_format:
            print_log(
                "Please input the birthdate in YYYY-MM-DD format e.g. 2022-11-20")
        except exc.day_out_of_range:
            print_log("Please input the day between 1 and 31")
        except exc.month_out_of_range:
            print_log("Please input the month between 1 and 12")
        except exc.date_not_available:
            print_log(
                "You can only select the date from today till the last date of this week!")
        except Exception as e:
            print_log(str(e))
        else:
            return input_date


def email_format_check():
    while True:
        try:
            email = input(u"\U0001F539"+"Enter refugee's email (if any): ")
            if email == "":
                return email
            elif "@" not in email or "." not in email:
                raise exc.wrong_email_format
        except exc.wrong_email_format:
            print_log(
                "Please input an email in a valid format e.g example@gmail.com")
        except Exception as e:
            print_log(str(e))
        else:
            return email


def camp_capacity_check(conn, purpose, old_camp_id):
    # check if the camp is full or can accept more refugee
    while True:
        try:
            camp_df = display_open_camp_option(conn,"refugee")
            camp_df_cop = camp_df.copy()
            print_table(camp_df_cop.columns,camp_df_cop.to_numpy().tolist(),(25,25,70,70,70,40))
            print("--------------------------------------------------------------------\n")
            camp = int(input(u"\U0001F539"+f"Assign the camp ID to the refugee: "))
            campID_list = list(camp_df.loc[:, "campID"].values)
            if camp not in campID_list:
                raise exc.camp_id_out_of_range
            for ind in camp_df.index:
                if ind+1 == camp:
                    if camp_df["no_of_refugees"][ind] == camp_df["capacity"][ind]:
                        raise exc.camp_capacity_full
            if purpose == "edit":
                new_plan_id = camp_df[camp_df["campID"]
                                      == int(camp)]["planID"].values[0]
                old_plan_id = camp_df[camp_df["campID"]
                                      == int(old_camp_id)]["planID"].values[0]
                if str(old_plan_id) != str(new_plan_id):
                    raise exc.move_to_others_plan
        except exc.camp_capacity_full:
            print_log(
                "This camp cannot accept more refugees since it has no more capacity.")
            print("Please re-assign the camp for the refugee")
        except exc.camp_id_out_of_range:
            print_log("Your input camp ID is invalid in the database")
        except ValueError:
            print_log("Please enter a numerical value for the camp ID.")
        except exc.move_to_others_plan:
            print_log(
                "Refugee cannot be assigned to any camp in different emergency plans.")
        except Exception as e:
            print_log(str(e))
        else:
            selected_camp_info = camp_df.loc[camp_df["campID"] == camp, :]
            return (camp, selected_camp_info)


def refugee_validity_check_by_ID(cond, refugee_df, conn):
    while True:
        try:
            print("Search for the refugee information in your emergency plan by")
            opt_dict = {'First Name': 'fName', 'Last Name': 'lName',
                        'Camp ID': 'campID', 'Family Member Name': 'familyMemberName'}
            options = Options(list(opt_dict.keys()), limited=True)
            print(options)
            opt = list(opt_dict.keys())[
                int(input(u"\U0001F539"+'Please select how you want to search: '))]
            keyword = input("\n"+u"\U0001F539" +
                            f"Please enter the {opt} keyword: ")
            if "'" in keyword:
                raise exc.unpermitted_input
            refugee_list = search_refugee(opt_dict[opt], keyword, conn,cond)
            if refugee_list.empty:
                raise exc.refugee_id_out_of_range
            else:
                print(
                    "\nPlease see details below for the list of refugees that match your search:\n")
                print_table(refugee_list.columns, refugee_list.to_numpy().tolist(
                ), (18, 16, 25, 25, 30, 25, 32, 70, 60, 70, 70, 60, 30, 30, 30, 25))
                print("\n")
            ref_id = int(input(
                u"\U0001F539"+f"Please input refugee ID of whom you wish to {cond} the information: "))
            if ref_id > (refugee_df["refugeeID"]).max() or ref_id < 0:
                raise exc.refugee_id_out_of_range
            if ref_id not in refugee_df["refugeeID"].values:
                raise exc.refugee_id_out_of_range
            if cond == "edit":
                status = refugee_df.loc[refugee_df["refugeeID"]
                                        == ref_id, "status"].values[0]
                if status == "inactive":
                    raise exc.inactive_refugee_edit
        except exc.refugee_id_out_of_range:
            print_log("There is no search result, please change your keyword.")
            print("Note: You are only allowed to search for refugee who is in the same emergency plan as you.")
        except ValueError:
            print_log("Please enter a numerical value for your input.")
        except exc.inactive_refugee_edit:
            print_log("You cannot edit inactive refugee's information.")
        except exc.unpermitted_input:
            print_log("Your input contains some special characters. Please try again with albhabets!")
        except Exception as e:
            print_log(str(e))
        else:
            return ref_id


def numerical_input_check(options):
    while True:
        try:
            selected_opts = input(options + "\n-->")
            array_opts = []
            if "," in selected_opts:
                array_opts.extend(
                    list(OrderedDict.fromkeys(selected_opts.split(","))))
                for v in array_opts:
                    if int(v) > options.count("\n")+1:
                        raise InvalidChoiceError(v)
            else:
                array_opts.append(selected_opts)
                if int(selected_opts) > options.count("\n")+1 or int(selected_opts) <= 0:
                    raise InvalidChoiceError(selected_opts)
        except InvalidChoiceError:
            print_log(
                "Your input number is invalid in our options. Please try again.")
        except ValueError:
            print_log("Please enter a numerical value for your selected options.")
        except Exception as e:
            print_log(str(e))
        else:
            # array of numerical input (no duplication)
            return array_opts

def task_ID_input_check(task_ID_list):
    while True:
        try:
            selected_task = int(input(u"\U0001F539"+"Enter a task ID which refugee would like to make change to: "))
            if selected_task not in task_ID_list:
                raise InvalidChoiceError(selected_task)
        except InvalidChoiceError:
            print_log("Your input number is invalid in our options. Please try again.")
        except ValueError:
            print_log("Please enter a numerical value for your selected options.")
        except Exception as e:
            print_log(str(e))
        else:
            return selected_task


def single_input_check(options):
    while True:
        try:
            selected_opts = input(options + "\n-->")
            if "," in selected_opts:
                raise ValueError
            else:
                if int(selected_opts) > options.count("\n")+1 or int(selected_opts) <= 0:
                    raise InvalidChoiceError(selected_opts)
        except InvalidChoiceError:
            print_log(
                "Your input number is invalid in our options. Please try again.")
        except ValueError:
            print_log(
                "Please enter a single numerical value for your selected options.")
        except Exception as e:
            print_log(str(e))
        else:
            return selected_opts


def volunteer_ID_req_check(volunteer_df, select_today):
    while True:
        try:
            vol_ID = int(input("\n"+u"\U0001F539" +
                               "Enter the volunteer ID of whom you want to assign this request to: "))
            volunteer_list = list(volunteer_df.loc[:, "volunteerID"].values)
            vol_shift = volunteer_df.loc[volunteer_df["volunteerID"]
                                         == vol_ID, "workShift"].values[0]
            if select_today == True:
                has_conflict = check_today_shift_conflict(
                    get_current_shift_time(), vol_shift)
                if has_conflict == True:
                    return 0
            if vol_ID not in volunteer_list:
                raise exc.volunteer_id_out_of_range
        except exc.volunteer_id_out_of_range:
            print_log(
                "Your input volunteer ID is invalid regarding the available options.")
        except ValueError:
            print_log("Please enter a numerical value for the volunteer ID.")
        except Exception as e:
            print_log(str(e))
        else:
            return vol_ID


def yn_valid(question):
    while True:
        try:
            user_input = input(f"{question}")
            if user_input != 'Yes' and user_input != 'No':
                raise exc.wrong_yn_input
        except exc.wrong_yn_input:
            print_log("Your input is invalid. Please enter either 'Yes' or 'No'")
        except Exception as e:
            print(e)
        else:
            return user_input
