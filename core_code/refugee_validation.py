from exception.refugee_exception import *
from collections import OrderedDict
from myError import *
import sys

def refugee_existence_check(refugee_df):
    while True:
        try:
            firstname = input("Enter refugee's firstname: ")
            lastname = input("Enter refugee's lastname: ")
            for ind in refugee_df.index:
                if refugee_df['firstname'][ind]==firstname and refugee_df['firstname'][ind]==lastname:
                    raise refugee_duplicated_regis
        except refugee_duplicated_regis:
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


def birthdate_format_check():
    while True: 
        try:
            birthdate = input("Enter refugee's birthdate (dd/mm/yyyy): ")
            if ("/" not in birthdate):
                raise wrong_birthdate_format
            else:
                bd_val = birthdate.split("/")
                if len(bd_val) != 3:
                    raise wrong_birthdate_format
                if (bd_val[0]) not in [format(x, '02d') for x in range(1,32)]:
                    raise day_out_of_range
                if (bd_val[1]) not in [format(x, '02d') for x in range(1,13)]:
                    raise month_out_of_range
        except wrong_birthdate_format:
            print("Please input the birthdate in day/month/year format e.g. 09/02/1997")
        except day_out_of_range:
            print("Please input the birth day between 1 and 31")
        except month_out_of_range:
            print("Please input the birth month between 1 and 12")
        else: 
            return birthdate

def email_format_check():
    while True:  
        try:
            email = input("Enter refugee's email (if any): ")
            if email=="":
                return email
            elif "@" not in email or "." not in email:
                raise wrong_email_format
        except wrong_email_format:
            print("Please input an email in a valid format e.g example@gmail.com")
        else:
            return email

def camp_capacity_check(camp_df):
    # check if the camp is full or can accept more refugee
    while True:
        try:
            camp = int(input("Assign the camp ID to the refugee: "))
            if camp > camp_df.shape[0] or camp < 0:
                raise camp_id_out_of_range
            for ind in camp_df.index:
                if ind+1 == camp:
                    total_member = camp_df["num_of_volunteers"][ind] + \
                        camp_df["num_of_refugees"][ind]
                    if total_member == camp_df["camp_capacity"][ind]:
                        raise camp_capacity_full
        except camp_capacity_full:
            print("This camp cannot accept more refugees since it has no more capacity.")
            print("Please re-assign the camp for the refugee")
        except camp_id_out_of_range:
            print("Your input camp ID is invalid in the database")
        except ValueError:
            print("Please enter a numerical value for the camp ID.")
        else:
            return camp

def refugee_validity_check_by_ID(cond,refugee_df):
       while True:
            try:
                ref_id = int(input(f"Please input refugee_ID of whom you wish to {cond} the information: "))
                if ref_id > refugee_df.shape[0]-1 or ref_id<0 :
                    raise refugee_id_out_of_range
                if ref_id not in refugee_df["refugee_ID"]:
                    raise refugee_id_out_of_range

            except refugee_id_out_of_range:
                print("Your input refugee ID is invalid in the database")
            except ValueError:
                print("Please enter a numerical value for the refugee ID.")
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