
from refugee import Refugee


def refugee_info_edit(choice, refugee_df, camp_df, camp_ID):
    ref = Refugee("Edit")
    match choice:
            case 1:
                ref.refugee_name(refugee_df)
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
                ref.assign_camp_ID(camp_df,"edit",camp_ID)
            case 8:
                ref.refugee_illnesses()
            case 9:
                ref.refugee_surgery()
            case 10:
                ref.refugee_smoking()
            case 11:
                ref.refugee_alcoholic()
    return ref.ref_row

