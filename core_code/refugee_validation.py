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

def refugee_existence_check(conn):
    while True:
        try:
            firstname = input("Enter refugee's firstname: ")
            lastname = input("Enter refugee's lastname: ")
            get_ref = f'''SELECT fName,lName FROM refugee WHERE fName = "{firstname}" AND lName = "{lastname}"'''
            pd_query = pd.read_sql_query(get_ref,conn)
            df_row = pd.DataFrame(pd_query,columns=["firstname","lastname"])
            if df_row.empty == False:
                raise exc.refugee_duplicated_regis
                    
        except exc.refugee_duplicated_regis:
            print("The refugee's firstname and lastname already exist in the database.\nPlease recheck if you're try to register the same person once again.")
            confirm = yn_valid("Is this refugee the same person as whom you registered before?(Yes/No): ")
            if(confirm == "No"):
                return (firstname,lastname)
            else:
                cont = yn_valid("Would you like to continue the registration?(Yes/No): ")
                if(cont == "Yes"):
                    print("The process restarts!!!")
                else:
                    print("The process ends")
                    sys.exit()
        except Exception as e:
            print_log(str(e))
        else:
            return (firstname,lastname)


def date_format_check(purpose,limit_start = '',limit_end = ''):
    while True: 
        try:
            input_date = input(f"Enter refugee's {purpose} (yyyy-mm-dd): ")
            bd_val = (input_date).split("-")
            if len(bd_val) != 3:
                raise exc.wrong_birthdate_format
            if (bd_val[2]) not in [format(x, '02d') for x in range(1,32)]:
                raise exc.day_out_of_range
            if (bd_val[1]) not in [format(x, '02d') for x in range(1,13)]:
                raise exc.month_out_of_range
            if limit_end != '' and limit_end != '':
                di, mi, yi = [int(x) for x in input_date.split('-')]
                date_inpt = datetime.date(di, mi, yi)
                ds, ms, ys = [int(x) for x in limit_start.split('-')]
                date_start = datetime.date(ds, ms, ys)
                de, me, ye = [int(x) for x in limit_end.split('-')]
                date_end = datetime.date(de, me, ye)
                if(date_inpt < date_start or date_inpt > date_end):
                    raise exc.date_not_available
        except ValueError:
            print_log("Incorrect date format, should be YYYY-MM-DD")
        except exc.wrong_birthdate_format:
            print_log("Please input the birthdate in YYYY-MM-DD format e.g. 2022-11-20")
        except exc.day_out_of_range:
            print_log("Please input the day between 1 and 31")
        except exc.month_out_of_range:
            print_log("Please input the month between 1 and 12")
        except exc.date_not_available:
            print_log("Please select the date from the options provided by the system.")
        except Exception as e:
            print_log(str(e))
        else: 
            return input_date

def email_format_check():
    while True:  
        try:
            email = input("Enter refugee's email (if any): ")
            if email=="":
                return email
            elif "@" not in email or "." not in email:
                raise exc.wrong_email_format
        except exc.wrong_email_format:
            print_log("Please input an email in a valid format e.g example@gmail.com")
        except Exception as e:
            print_log(str(e))
        else:
            return email

def camp_capacity_check(conn):
    # check if the camp is full or can accept more refugee
    while True:
        try:
            camp_query = '''SELECT camp.campID, COUNT(refugeeID) as no_of_refugees,capacity FROM camp LEFT JOIN refugee ON camp.campID = refugee.campID GROUP BY camp.campID'''
            pd_camp = pd.read_sql_query(camp_query, conn)
            camp_df = pd.DataFrame(
            pd_camp, columns=['campID', 'no_of_refugees', 'capacity'])
            print(camp_df)
            print("-------------------------------------------")
            camp = int(input("Assign the camp ID to the refugee: "))
            if camp > camp_df.shape[0] or camp <= 0:
                raise exc.camp_id_out_of_range
            for ind in camp_df.index:
                if ind+1 == camp:
                    if camp_df["no_of_refugees"][ind] == camp_df["capacity"][ind]:
                        raise exc.camp_capacity_full
        except exc.camp_capacity_full:
            print_log("This camp cannot accept more refugees since it has no more capacity.")
            print("Please re-assign the camp for the refugee")
        except exc.camp_id_out_of_range:
            print_log("Your input camp ID is invalid in the database")
        except ValueError:
            print_log("Please enter a numerical value for the camp ID.")
        except Exception as e:
            print_log(str(e))
        else:
            return camp

def refugee_validity_check_by_ID(cond,refugee_df, conn):
        while True:
            try:
                print("Search for the refugee information by")
                col_opt = ['fName','lName','campID','familyMemberName']
                options = Options(col_opt, limied=True)
                print(options)
                opt = col_opt[int(input('Please select how you want to search: '))]
                keyword = input(f"\nPlease enter the {opt} keyword: ")
                refugee_list = search_refugee(opt,keyword,conn)
                if refugee_list.empty:
                    raise exc.refugee_id_out_of_range
                else:
                    print("\nPlease see details below for the list of refugees that match your search:")
                    print(refugee_list)
                ref_id = int(input(f"Please input refugee ID of whom you wish to {cond} the information: "))
                if ref_id > (refugee_df["refugeeID"]).max() or ref_id<0 :
                    raise exc.refugee_id_out_of_range
                if ref_id not in refugee_df["refugeeID"].values:
                    raise exc.refugee_id_out_of_range
                if cond == "edit":
                    status = refugee_df.loc[refugee_df["refugeeID"]==ref_id,"status"].values[0]
                    if status == "inactive":
                        raise exc.inactive_refugee_edit
            except exc.refugee_id_out_of_range:
                print_log("Your input is invalid in our database")
            except ValueError:
                print_log("Please enter a numerical value for your input.")
            except exc.inactive_refugee_edit:
                print_log("You cannot edit inactive refugee's information.")
            except Exception as e:
                print_log(str(e))
            else: 
                return ref_id

def numerical_input_check(options):
    while True:
        try:
            selected_opts = input(options + "\n:")
            array_opts = []
            if "," in selected_opts:
                array_opts.extend(list(OrderedDict.fromkeys(selected_opts.split(","))))
                for v in array_opts:
                    if int(v) > options.count("\n")+1:
                        raise InvalidChoiceError(v)
            else:
                array_opts.append(selected_opts)
                if int(selected_opts) > options.count("\n")+1:
                    raise InvalidChoiceError(selected_opts)
        except InvalidChoiceError:
            print_log("Your input number is invalid in our options. Please try again.")
        except ValueError:
            print_log("Please enter a numerical value for your selected options.")
        except Exception as e:
            print_log(str(e))
        else:
            # array of numerical input (no duplication)
            return array_opts

def volunteer_ID_req_check(volunteer_df):
    while True:
        try:
            vol_ID = int(input(
                        "\nEnter the volunteer ID of whom you want to assign this request to: "))
            if vol_ID > (volunteer_df["volunteerID"]).max() or vol_ID < 1:
                raise exc.volunteer_id_out_of_range
            if vol_ID not in volunteer_df["volunteerID"].values:
                raise exc.volunteer_id_out_of_range
        except exc.volunteer_id_out_of_range:
            print_log("Your input volunteer ID is invalid regarding the available options.")
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
            print_log(e)
        else:
            return user_input




