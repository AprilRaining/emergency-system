class InvalidInput(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return f'{self.value} is an invalid input.\nPlease reenter.'


class InvalidChoiceError(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return f'{self.value} is an invalid choice.\nPlease reenter a number specified above.'
