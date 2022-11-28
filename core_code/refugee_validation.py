import refugee_exception as exp
from collections import OrderedDict
from myError import *
import sys
from datetime import *
import pandas as pd
from db_connect_ref import *

def refugee_existence_check(conn):
    while True:
        try:
            firstname = input("Enter refugee's firstname: ")
            lastname = input("Enter refugee's lastname: ")
            get_ref = f'''SELECT fName,lName FROM refugee WHERE fName = "{firstname}" AND lName = "{lastname}"'''
            cur = conn.cursor()
            cur.execute(get_ref)
            rows = cur.fetchall()
            if rows != []:
                raise exp.refugee_duplicated_regis
                    
        except exp.refugee_duplicated_regis:
            print("The refugee's firstname and lastname already exist in the database.\nPlease recheck if you're try to register the same person once again.")
            confirm = input("Is this refugee the same person as whom you registered before?(Yes/No): ")
            if(confirm == "No"):
                return (firstname,lastname)
            else:
                cont = input("Would you like to continue the registration?(Yes/No): ")
                if(cont == "Yes"):
                    print("The process restarts!!!")
                else:
                    print("The process ends")
                    sys.exit()
        else:
            return (firstname,lastname)


def date_format_check(purpose,limit_start = '',limit_end = ''):
    while True: 
        try:
            input_date = input(f"Enter refugee's {purpose} (yyyy-mm-dd): ")
            datetime.strptime(input_date, '%Y-%m-%d')
            if ("-" not in input_date):
                raise exp.wrong_birthdate_format
            else:
                bd_val = input_date.split("-")
                if len(bd_val) != 3:
                    raise exp.wrong_birthdate_format
                if (bd_val[2]) not in [format(x, '02d') for x in range(1,32)]:
                    raise exp.day_out_of_range
                if (bd_val[1]) not in [format(x, '02d') for x in range(1,13)]:
                    raise exp.month_out_of_range
                if limit_end != '' and limit_end != '':
                    di, mi, yi = [int(x) for x in input_date.split('-')]
                    date_inpt = date(di, mi, yi)
                    ds, ms, ys = [int(x) for x in limit_start.split('-')]
                    date_start = date(ds, ms, ys)
                    de, me, ye = [int(x) for x in limit_end.split('-')]
                    date_end = date(de, me, ye)
                    if(date_inpt < date_start or date_inpt > date_end):
                        raise exp.date_not_available
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        except exp.wrong_birthdate_format:
            print("Please input the birthdate in YYYY-MM-DD format e.g. 2022-11-20")
        except exp.day_out_of_range:
            print("Please input the day between 1 and 31")
        except exp.month_out_of_range:
            print("Please input the month between 1 and 12")
        except exp.date_not_available:
            print("Please select the date from the options provided by the system.")
        else: 
            return input_date

def email_format_check():
    while True:  
        try:
            email = input("Enter refugee's email (if any): ")
            if email=="":
                return email
            elif "@" not in email or "." not in email:
                raise exp.wrong_email_format
        except exp.wrong_email_format:
            print("Please input an email in a valid format e.g example@gmail.com")
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
            if camp > camp_df.shape[0] or camp < 0:
                raise exp.camp_id_out_of_range
            for ind in camp_df.index:
                if ind+1 == camp:
                    if camp_df["no_of_refugees"][ind] == camp_df["capacity"][ind]:
                        raise exp.camp_capacity_full
        except exp.camp_capacity_full:
            print("This camp cannot accept more refugees since it has no more capacity.")
            print("Please re-assign the camp for the refugee")
        except exp.camp_id_out_of_range:
            print("Your input camp ID is invalid in the database")
        except ValueError:
            print("Please enter a numerical value for the camp ID.")
        else:
            return camp

def refugee_validity_check_by_ID(cond,refugee_df):
        while True:
            try:
                ref_id = int(input(f"Please input refugee ID of whom you wish to {cond} the information: "))
                # print((refugee_df["refugeeID"]).max())
                if ref_id > (refugee_df["refugeeID"]).max() or ref_id<0 :
                    raise exp.refugee_id_out_of_range
                if ref_id not in refugee_df["refugeeID"].values:
                    raise exp.refugee_id_out_of_range
                if cond == "edit":
                    status = refugee_df.loc[refugee_df["refugeeID"]==ref_id,"status"].values[0]
                    if status == "inactive":
                        raise exp.inactive_refugee_edit
            except exp.refugee_id_out_of_range:
                print("Your input refugee ID is invalid in the database")
            except ValueError:
                print("Please enter a numerical value for the refugee ID.")
            except exp.inactive_refugee_edit:
                print("You cannot edit inactive refugee's information.")
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
                        raise OutOfRangeError(v)
            else:
                array_opts.append(selected_opts)
                if int(selected_opts) > options.count("\n")+1:
                    raise OutOfRangeError(selected_opts)
        except OutOfRangeError as e:
            print(e)
        except ValueError:
            print("Please enter a numerical value for your selected options.")
        else:
            # array of numerical input (no duplication)
            return array_opts

def volunteer_ID_req_check(volunteer_df):
    while True:
        try:
            vol_ID = int(input(
                        "\nPlease enter the volunteer ID of whom you want to assign this request to: "))
            if vol_ID > (volunteer_df["volunteerID"]).max() or vol_ID < 1:
                raise exp.volunteer_id_out_of_range
            if vol_ID not in volunteer_df["volunteerID"].values:
                raise exp.volunteer_id_out_of_range
        except exp.volunteer_id_out_of_range:
            print("Your input volunteer ID is invalid regarding the available options.")
        except ValueError:
            print("Please enter a numerical value for the volunteer ID.")
        else: 
            return vol_ID

