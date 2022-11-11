import pandas as pd


# abspath = os.path.abspath(__file__)
# camp = pd.read_csv("../info_files/camp.csv")


class StartProgram(object):

    """
        This is the class used to start the program and read files.

    """

    def __init__(self):
        self.camp_file = pd.read_csv("../info_files/camp.csv")
        self.plan_file = pd.read_csv("../info_files/emergency_plan.csv")
        self.refugee_file = pd.read_csv("../info_files/refugee.csv")
        self.volunteer_file = pd.read_csv("../info_files/volunteer.csv")

    def admin_manage_plan(self):
        pass

    def admin_manage_account(self):
        pass

    def volunteer_manage_info(self):
        pass

    def volunteer_manage_profile(self):
        pass

    def login(self):
        pass

    def register(self):
        pass


if __name__ == "__main__":
    program = StartProgram()
    print(program.camp_file)


