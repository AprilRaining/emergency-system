from options import *


class PlanInput:
    @staticmethod
    def type():
        options = Options('type')
        print(options)
        option = options.get_option()
        if option != 0:
            return options.values[option - 1]
        else:
            return input('Please input the type of the emergency plan: ')

    @staticmethod
    def description():
        return input('Please input the description of the emergency plan: ')

    @staticmethod
    def area():
        options = Options('area')
        print(options)
        option = options.get_option()
        if option != 0:
            return options.values[option - 1]
        else:
            return input('Please input the geographical area affected by the natural disaster: ')

    @staticmethod
    def start_date():
        options = Options('start_date')
        print(options)
        match options.get_option():
            case 1:
                return datetime.date.today()
            case 0:
                while True:
                    date = Get.data(
                        'Please input the start date of the emergency plan in the format of yyyy-mm-dd: ')
                    if date > datetime.date.today():
                        return date
                    else:
                        print('Please input a data later then today.')

    @staticmethod
    def close_date(startDate):
        options = Options('close_date')
        print(options)
        while True:
            match options.get_option():
                case 1:
                    while True:
                        if startDate < datetime.date.today():
                            return datetime.date.today().strftime('%Y-%m-%d')
                        else:
                            print('*close date is equal or earlier than start date please input a valid date*')
                            break
                case 2:
                    return 'null'
                case 0:
                    while True:
                        closeDate = Get.data('Please input the close date of the emergency plan in the format of yyyy-mm-dd: ')
                        if startDate < closeDate:
                            return closeDate.strftime('%Y-%m-%d')
                        else:
                            print('*close date is equal or earlier than start date please input a valid date*')

    @staticmethod
    def number_of_camps():
        return Get.int('Please input the number of camps: ')

    @staticmethod
    def status():
        options = Options('status')
        print(options)
        return options.get_option()

    @staticmethod
    def priority():
        options = Options('priority')
        print(options)
        return options.get_option()
