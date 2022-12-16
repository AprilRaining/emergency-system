
from refugee import Refugee
from db_connect_ref import *
import sys
from system_log import *
from refugee_validation import *

def refugee_info_edit(choice, refugeeID, refugee_df, conn):
    ref = Refugee("Edit",conn)
    request = str(
    refugee_df.loc[refugee_df["refugeeID"] == refugeeID, "request"].values[0])
    orig_camp = str(
    refugee_df.loc[refugee_df["refugeeID"] == refugeeID, "campID"].values[0])
    match choice:
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
                    ref.assign_camp_ID("edit",orig_camp)
                else:
                    print("\n------------REFUGEE'S CAMP CHANGE------------")
                    warn("The refugee is not allowed to change the camp because she/he has scheduled a request with volunteer.")
                    print("We recommend clearing out all request schedules before moving to a new camp.")
                    ref.ref_row.append(int(request))
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
                    print("\n------------REFUGEE'S REQUEST SYSTEM------------")
                    purpose = input(u"\U0001F539"+"Specify your purpose of accessing refugee's request system? (add or edit or clear): ")
                    if purpose != "add" and purpose != "edit" and purpose != "clear":
                        print_log("Please enter either 'add' or 'edit' or 'clear'")
                    else:
                        if purpose!="clear":
                            if request == "0" and purpose =="edit":
                                warn("You don't have any request in your schedule.")
                                warn("We recommend changing your purpose to 'add'.")
                                cont = yn_valid(u"\U0001F539"+"Would you like to abort your request edition? (Yes/No): ")
                                if cont == "Yes":
                                    ref.ref_row.append(0)
                                    break
                            else:
                                # add or edit (correctly input)
                                ref.ref_request(purpose, refugeeID)
                                break
                        else:
                            # clear volunteer schedule
                            df_task_by_ref = select_task_by_ref_id(conn, refugeeID)
                            if df_task_by_ref.empty:
                                warn("The request is already empty. There is nothing to clear out.")
                                cont = yn_valid(u"\U0001F539"+"Would you like to continue with request edition? (Yes/No): ")
                                if cont == "No":
                                    ref.ref_row.append(0)
                                    break
                            else:
                                print("Please see the task schedule below: \n")
                                print_table(df_task_by_ref.columns,df_task_by_ref.to_numpy().tolist(),(18,22,30,40,14,40,40,30))
                                # volunteer schedule clear
                                clear_request_schedule(conn, df_task_by_ref)
                                # refugee
                                update_refdb_attr(conn, refugeeID, "request", "0")
                                print(u"\U0001F539"+"The request schedule related to volunteer and refugee are successfully cleared out.")
                                ref.ref_row.append(0)
                                break
            case 13:
                sys.exit()
          
    # return refugee information list (array) based on selected field
    return ref.ref_row

