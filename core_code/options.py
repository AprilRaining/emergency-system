from get import *


class Options:
    def __init__(self, name):
        match name:
            case 'type':
                self.values = [
                    'Wildfire',
                    'Earthquakes',
                    'Volcanoes',
                    'Famines & Droughts',
                    'Extreme Precipitation & Flooding',
                    'Extreme Temperature',
                    'Pandemic'
                ]
                self.limited = False
            case 'area':
                self.values = [
                    'Asia',
                    'Europe',
                    'North America',
                    'South America',
                    "Africa",
                    'Oceania'
                ]
                self.limited = False
            case 'start_date':
                self.values = [
                    'Today'
                ]
                self.limited = False
            case 'close_date':
                self.values = [
                    'Today',
                    'Input later'
                ]
                self.limited = False
            case 'status':
                self.values = [
                    'Waiting to open',
                    'Opening'
                ]
                self.limited = True
            case 'priority':
                self.values = [
                    'very high',
                    'high',
                    'normal',
                ]
                self.limited = True
            case 'allowEditNotOpening':
                self.values = [
                    'type',
                    'description',
                    'area',
                    'startDate',
                    'endDate',
                    'numberOfCamps',
                    'priority'
                ]
                self.limited = True
            case 'allowEditOpening':
                self.values = [
                    'description',
                    'endDate',
                    'priority'
                ]
                self.limited = True
        self.len = len(self.values)
        temp = []
        if not self.limited:
            for i in range(self.len):
                temp.append('{}. {}'.format(i + 1, self.values[i]))
            temp.append('0. Manual input.')
            self.optionRange = self.len + 1
        else:
            for i in range(self.len):
                temp.append('{}. {}'.format(i, self.values[i]))
            self.optionRange = self.len
        self.menu = '\n'.join(temp)

    def __str__(self):
        return self.menu

    def get_option(self, hint='Please choose one option: '):
        return Get.option_in_range(self.optionRange, hint)
