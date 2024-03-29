from options import *
from system_log import *
from myfunctionlib import *


class PlanInput:
    @staticmethod
    def type():
        prCyan('Type of Natural Disaster:')
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
            return Get.string(u"\U0001F539" + 'Please input the type of the emergency plan: ')

    @staticmethod
    def description():
        prCyan('\nPlan Description:')
        return Get.text(u"\U0001F539" + 'Please input the description of the emergency plan: ')

    @staticmethod
    def area():
        prCyan('\nGeographical Area Affected: ')
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
            return Get.string(u"\U0001F539"+'Please input the geographical area affected by the natural disaster: ')

    @staticmethod
    def start_date():
        prCyan('\nStart Date:')
        options = Options([
            'Today'
        ])
        print(options)
        match options.get_option():
            case 1:
                return datetime.date.today()
            case 0:
                return PlanInput.start_date_manual_input()

    @staticmethod
    def end_date(startDate):
        prCyan('\nEnd Date:')
        options = Options([
            'Input later'
        ])
        print(options)
        while True:
            match options.get_option():
                case 1:
                    return None
                case 0:
                    PlanInput.end_date_manual_input(startDate)

    @staticmethod
    def number_of_camps():
        prCyan('\nNumber of Refugee Camps:')
        return Get.int(u"\U0001F539" + 'Please input the number of camps: ')

    @staticmethod
    def status():
        print('Status: ')
        options = Options([
            'Waiting to open',
            'Opening'
        ], limited=True)
        print(options)
        return options.get_option()

    def start_date_update():
        return PlanInput.start_date_manual_input()

    @staticmethod
    def end_date_update(startDate):
        return PlanInput.end_date_manual_input(startDate)

    @staticmethod
    def end_date_manual_input(startDate):
        while True:
            endDate = Get.data(
                u"\U0001F539" + 'Please input the close date of the emergency plan in the format of yyyy-mm-dd: ')
            if startDate < endDate:
                return endDate.strftime('%Y-%m-%d')
            else:
                warn(
                    '*Close date is equal or earlier than the start date, please input a valid date.*')

    @staticmethod
    def start_date_manual_input():
        while True:
            date = Get.data(
                u"\U0001F539" + 'Please input the start date of the emergency plan in the format of yyyy-mm-dd: ')
            if date > datetime.date.today():
                return date
            elif date == datetime.date.today():
                prYellow(
                    'The date your input is today.\n If you want to open it now, please use the open plan function.')
            else:
                warn('Please input a data later than today.')
