
from refugee import Refugee
from db_connect_ref import *
import sys
from system_log import *

def refugee_info_edit(choice, refugeeID, refugee_df, conn):
    ref = Refugee("Edit",conn)
    request = str(
    refugee_df.loc[refugee_df["refugeeID"] == refugeeID, "request"].values[0])
    match choice:
            case 0:
                sys.exit()
            case 1:
                ref.refugee_name()
            case 2:
                ref.refugee_birthdate()
            case 3:
                ref.refugee_gender()
            case 4:
                ref.refugee_race()
            case 5:
                ref.refugee_contact()
            case 6:
                ref.refugee_family()
            case 7:
                if request == "0":
                    # allow only when the request schedule is empty
                    ref.assign_camp_ID()
                else:
                    warn("Warning: The refugee is not allowed to change the camp because she/he has scheduled a request with volunteer.")
                    print("We recommend clearing out all request schedules before moving to a new camp.")
                sys.exit()
            case 8:
                ref.refugee_illnesses()
            case 9:
                ref.refugee_surgery()
            case 10:
                ref.refugee_smoking()
            case 11:
                ref.refugee_alcoholic()
            case 12:
                while True:
                    purpose = input("Specify your purpose of accessing refugee's request system? (add or edit or clear): ")
                    if purpose != "add" and purpose != "edit" and purpose != "clear":
                        print_log("Please enter either 'add' or 'edit' or 'clear'")
                    else:
                        print("\n------------REFUGEE'S REQUEST SYSTEM------------")
                        if purpose!="clear":
                            if request == "0" and purpose =="edit":
                                print_log("You don't have any request in your schedule.")
                                print_log("We recommend changing your purpose to 'add'.")
                                cont = input("Would you like to continue with request edition? (Yes/No): ")
                                if cont == "No":
                                    print("Cancelling all edition. Please start again!")
                                    sys.exit()
                            else:
                                # add or edit (correctly input)
                                ref.ref_request(purpose, refugeeID)
                                break
                        else:
                            # clear volunteer schedule
                            df_task_by_ref = select_task_by_ref_id(conn, refugeeID)
                            print(df_task_by_ref)
                            if df_task_by_ref.empty:
                                print_log("The request is already empty. There is nothing to clear out.")
                                cont = input("Would you like to continue with request edition? (Yes/No): ")
                                if cont == "No":
                                    ref.ref_row.append(0)
                                    break
                            else:
                                # volunteer schedule clear
                                clear_request_schedule(conn, df_task_by_ref)
                                # refugee
                                update_refdb_attr(conn, refugeeID, "request", "0")
                                print("The request schedule related to volunteer and refugee are successfully cleared out.")
                                ref.ref_row.append(0)
                                break
          
    # return refugee information list (array) based on selected field
    return ref.ref_row

