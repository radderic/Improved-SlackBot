from slackclient import SlackClient
from datetime import datetime

class Event(object):
    def __init__(self, **kwargs):
        #all the arguments
        self.raw = kwargs
        self.type = kwargs.get('type', None)
        self.where = kwargs.get('channel', None)
        self.who = kwargs.get('user', None)
        #all information
        self.text = kwargs.get('text', None)
        #self.message - regex version
        self.timestamp = kwargs.get('ts', None)

    #helper functions as needed
    def formattedTime(self):
        time = datetime.fromtimestamp(float(self.timestamp))

        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        if(hour == 0):
            hour = 12
            ampm = 'AM'
        elif(hour > 12):
            hour = hour - 12
            ampm = 'PM'
        else:
            ampm = 'AM'
        minute = time.minute
        second = time.second

        return '{}/{}/{} - {}:{}:{} {}'.format(month, day, year, hour, minute, second, ampm)
