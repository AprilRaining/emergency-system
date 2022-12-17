import datetime
from system_log import *
from myError import *


class Get:
    @staticmethod
    def int(hint: str, sign=1):
        """
        This function only accept a positive int input.
        With sign parameter equal to 0, it will accept all int number.
        :return: int
        """
        while True:
            try:
                n = int(input(hint))
                if sign != 0:
                    if n <= 0:
                        raise InvalidInput(n)
            except ValueError:
                print_log("You entered a non-numeric value.")
                print_log("Please reenter a valid value.")
            except InvalidInput as e:
                print(e)
            else:
                return n

    @staticmethod
    def data(hint: str):
        while True:
            try:
                date = datetime.datetime.strptime(
                    input(hint), '%Y-%m-%d').date()
            except InvalidInput as e:
                warn(e)
            except ValueError as e:
                warn(e)
            else:
                return date

    @staticmethod
    def listing(start, end, hint='', spliter=','):
        while True:
            try:
                l = input(hint)
                arr = l.split(spliter)
                for i in range(len(arr)):
                    arr[i] = int(arr[i])
                for i in arr:
                    if i not in range(start, end):
                        raise InvalidInput(l)
            except InvalidInput as e:
                print(e)
            except Exception as e:
                print_log("Unknown error")
                print(e)
            else:
                return arr

    @staticmethod
    def option_in_range(span: int, hint='', start=0):
        while True:
            try:
                option = int(input(hint))
                if option not in range(start, span):
                    raise InvalidChoiceError(option)
            except ValueError:
                print_log("You entered a non-numeric value.")
                print_log("Please reenter a valid Number:")
            except InvalidChoiceError as e:
                print(e)
            else:
                return option

    @staticmethod
    def option_in_list(li, hint=''):
        while True:
            try:
                option = int(input(hint))
                if option not in li:
                    raise InvalidChoiceError(option)
            except ValueError:
                print_log("You entered a non-numeric value.")
                print_log("Please reenter a valid Number:")
            except InvalidChoiceError as e:
                print(e)
            else:
                return option

    def option_in_list_full(li, hint=''):
        while True:
            try:
                option = input(hint)
                if option not in li:
                    raise InvalidChoiceError(option)
            except ValueError:
                print("Invalid input.")
                print("Please reenter a valid value.")
            except InvalidChoiceError as e:
                print(e)
            else:
                return option
