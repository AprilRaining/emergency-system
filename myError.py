class InvalidInput(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return f"\033[91m{self.value} is an invalid input.\nPlease reenter.\033[00m"


class InvalidChoiceError(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return f"\033[91m{self.value} is an invalid choice.\nPlease reenter a number specified above.\033[00m"


class CampCapacityError(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return f"\033[91m Camp {self.value} is now full.\nPlease try to choose another one."
