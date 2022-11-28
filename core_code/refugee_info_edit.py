
from refugee import Refugee

def refugee_info_edit(choice, refugeeID,conn):
    ref = Refugee("Edit",conn)
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
                ref.assign_camp_ID()
            case 8:
                ref.refugee_illnesses()
            case 9:
                ref.refugee_surgery()
            case 10:
                ref.refugee_smoking()
            case 11:
                ref.refugee_alcoholic()
            case 12:
                # while True:
                    purpose = input("Please specify your purpose of accessing refugee's request system? (add or edit): ")
                    # if purpose != "add" and purpose != "edit":
                    #     print("Please enter either 'add' or 'edit'")
                    # else:
                    #     print("\n------------REFUGEE'S REQUEST SYSTEM------------")
                    ref.ref_request(purpose, refugeeID)
                        # break
    # return refugee information list (array) based on selected field
    return ref.ref_row

