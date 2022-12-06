class OutOfRangeError(Exception):
    def __init__(self, input):
        Exception.__init__(self)
        self.input = input

    def __str__(self):
        return f'{self.input} is an invalid choice.\nPlease reenter a number specified above.'
