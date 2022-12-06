from options import *


class PlanInput:
    @staticmethod
    def type():
        print('Type: ')
        options = Options([
            'Wildfire',
            'Earthquakes',
            'Volcanoes',
            'Famines & Droughts',
            'Extreme Precipitation & Flooding',
            'Extreme Temperature',
            'Pandemic'
        ])
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
        print('Area: ')
        options = Options([
            'Asia',
            'Europe',
            'North America',
            'South America',
            "Africa",
            'Oceania'
        ])
        print(options)
        option = options.get_option()
        if option != 0:
            return options.values[option - 1]
        else:
            return input('Please input the geographical area affected by the natural disaster: ')

    @staticmethod
    def start_date():
        print('Start Date:')
        options = Options([
            'Today'
        ])
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
    def end_date(startDate):
        print('End Date:')
        if type(startDate) == type(''):
            startDate = datetime.datetime.strptime(
                startDate, '%Y-%m-%d').date()
        options = Options([
            'Today',
            'Input later'
        ])
        print(options)
        while True:
            match options.get_option():
                case 1:
                    while True:
                        if startDate < datetime.date.today():
                            return datetime.date.today().strftime('%Y-%m-%d')
                        else:
                            print(
                                '*End date is equal or earlier than start date please input a valid date*')
                            break
                case 2:
                    return None
                case 0:
                    while True:
                        endDate = Get.data(
                            'Please input the close date of the emergency plan in the format of yyyy-mm-dd: ')
                        if startDate < endDate:
                            return endDate.strftime('%Y-%m-%d')
                        else:
                            print(
                                '*close date is equal or earlier than start date please input a valid date*')

    @staticmethod
    def number_of_camps():
        return Get.int('Please input the number of camps: ')

    @staticmethod
    def status():
        print('Status: ')
        options = Options([
            'Waiting to open',
            'Opening'
        ], limited=True)
        print(options)
        return options.get_option()

    @staticmethod
    def priority():
        print('Priority: ')
        options = Options([
            'very high',
            'high',
            'normal',
        ], limited=True)
        print(options)
        return options.get_option()
