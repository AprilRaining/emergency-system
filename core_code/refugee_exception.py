class wrong_birthdate_format(Exception):
    """Raised when the input birthdate is not in a correct format or the date is invalid"""
    pass
class day_out_of_range(Exception):
    """Raised when the input day is not between 1 and 31"""
    pass
class month_out_of_range(Exception):
    """Raised when the input month is not between 1 and 12"""
    pass
class wrong_email_format(Exception):
    """Raised when the input email is not in a correct format"""
    pass
class camp_capacity_full(Exception):
    """Raised when the user assigns refugee to the camp that's not available or runs out of capacity"""
    pass
class camp_id_out_of_range(Exception):
    """Raised when the user enters invalid camp ID"""
    pass
class refugee_duplicated_regis(Exception):
    """Raised when the user registers the refugee that already exists in the database"""
    pass
class refugee_id_out_of_range(Exception):
    """Raised when the user enters invalid refugee ID"""
    pass
class volunteer_id_out_of_range(Exception):
    """Raised when the user enters invalid volunteer ID"""
    pass
class date_not_available(Exception):
    """Raised when the input date is not in the selectable range"""
    pass
class inactive_refugee_edit(Exception):
    """Raised when volunteer tries to edit the information of inactive refugee infomation"""