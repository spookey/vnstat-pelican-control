'''johnny worker'''

from datetime import date
from names import Dates, Names
from config import VERBOSE, GATELIST, PELIC_CONFIG, PELIC_CONTENT, PELIC_OUTPUT, pelic_theme
from pelican.settings import get_settings_from_file, configure_settings
from pelican import Pelican

class Worker(object):
    wrkday = None

    def __init__(self, wrkday):
        self.wrkday = Dates(wrkday)
        self.gatelist = GATELIST

    def mkpelican(self):
        '''builds pelican posts'''
        psettings = get_settings_from_file(PELIC_CONFIG)
        psettings['PATH'] = PELIC_CONTENT
        psettings['OUTPUT_PATH'] = PELIC_OUTPUT
        psettings['THEME'] = pelic_theme(psettings['THEME'])

        p = Pelican(configure_settings(psettings))
        p.run()


    def run(self):
        for gate in self.gatelist.keys():
            gn = Names(gate, self.wrkday)
            if self.wrkday.date() == Dates(date.today()).date():
                if VERBOSE:
                    print(':: this is today, say cheese')
                print(gn.snapshot())
            if VERBOSE:
                    print(':: trying to load graph')
            print(gn.getsnapshot())

            if VERBOSE:
                print(':: writing article')
            gn.mkpost()

        if VERBOSE:
            print(':: feeding the pelican')
        print(self.mkpelican())
