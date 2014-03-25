'''does things'''

from argparse import ArgumentParser
from datetime import date
from config import VERBOSE
from worker import Worker

TODAY = date.today()

def dayparser():
    parser = ArgumentParser(description='gatestats')
    parser.add_argument('ar', nargs='?', default='r', help='type of date entry. (_a_bsolute or _r_elative: default: r)')
    parser.add_argument('-d', default='0', type=int, help='day, default: 0')
    parser.add_argument('-m', default='0', type=int, help='month, default: 0')
    parser.add_argument('-y', default='0', type=int, help='year, default: 0')
    args = parser.parse_args()

    if 'a' in args.ar:
        year = TODAY.year if args.y == 0 else args.y
        month = TODAY.month if args.m == 0 else args.m
        day = TODAY.day if args.d == 0 else args.d
    else:
        year = TODAY.year - args.y
        month = TODAY.month - args.m
        day = TODAY.day - args.d
    try:
        wrkday = TODAY.replace(year, month, day)
    except ValueError as ex:
        print(':: invalid entry: %s' %(ex))
    else:
        return(wrkday)

def main():

    wrkday = dayparser()

    w = Worker(wrkday)
    w.run()

    if VERBOSE:
        print(':: all done')

if __name__ == '__main__':
    main()

