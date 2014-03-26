'''johnny worker'''

from datetime import date
from names import Dates, Names
from config import GATELIST
from helper import message, mkpelican

class Worker(object):
    '''does the work'''
    wrkday = None
    gatelist = None

    def __init__(self, wrkday):
        self.wrkday = Dates(wrkday)
        self.gatelist = GATELIST

    def run(self):
        '''takes and downloads pictures, makes posts, rides the pelican'''
        for gate in self.gatelist.keys():
            gtn = Names(gate, self.wrkday)
            if self.wrkday.date() == Dates(date.today()).date():
                message('this is today, say cheese', shout=True)
                message(gtn.snapshot(), shout=True)
            message('trying to load graph', shout=True)
            message(gtn.getsnapshot(), shout=True)

            message('writing article', shout=True)
            gtn.mkpost()

        message('feeding the pelican', shout=True)
        mkpelican()
