from get import *


class Options:
    def __init__(self, optionsList, limited=False):
        self.values = optionsList
        self.limited = limited
        self.len = len(self.values)
        temp = []
        if not self.limited:
            for i in range(self.len):
                temp.append('[ {}.] {}'.format(i + 1, self.values[i]))
            temp.append(u"\U0001F531"+'[Hint]Enter 0 for Manual Input.')
            self.optionRange = self.len + 1
        else:
            for i in range(self.len):
                temp.append('[ {}.] {}'.format(i, self.values[i]))
            self.optionRange = self.len
        self.menu = '\n'.join(temp)

    def __str__(self):
        return self.menu

    def get_option(self, hint=u"\U0001F539"+'Please choose one option: '):
        return Get.option_in_range(self.optionRange, hint)
