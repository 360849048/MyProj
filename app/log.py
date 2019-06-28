import datetime


class Log:
    def __init__(self, path='./log.txt'):
        self.path = path

    def _getDate(self):
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month) if now.month > 9 else '0' + str(now.month)
        day = str(now.day) if now.day > 9 else '0' + str(now.day)
        hour = str(now.hour) if now.hour > 9 else '0' + str(now.hour)
        minute = str(now.minute) if now.minute > 9 else '0' + str(now.minute)
        second = str(now.second) if now.second > 9 else '0' + str(now.second)
        return year + '.' + month + '.' + day + ' ' + hour + ':' + minute + ':' + second

    def record(self, str_info):
        fp = open(self.path, 'a', encoding='utf-8')
        now = self._getDate()
        fp.write('* ')
        fp.write(now)
        fp.write(' ' * 10)
        fp.write(str_info)
        fp.write('\n')
        fp.close()


log = Log()
