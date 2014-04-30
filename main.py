'''does things'''

from argparse import ArgumentParser
from datetime import date
from names import Dates, Names
from helper import message, mkpelican, getgatelist

TODAY = date.today()

def arg_parser():
    '''calendar surfing'''
    parser = ArgumentParser(description='gatestats - vnstat-pelican-control plugin', epilog='Please be careful, this is software', add_help=True)
    parser.add_argument(
        'ar', nargs='?', default='r',
        help='type of date entry. (_a_bsolute or _r_elative: default: r)'
        )
    parser.add_argument('-d', default='0', type=int, help='day, default: 0')
    parser.add_argument('-m', default='0', type=int, help='month, default: 0')
    parser.add_argument('-y', default='0', type=int, help='year, default: 0')
    parser.add_argument('--nonet',
        action='store_true',
        help='Do not try to connect to any gate to generate or download images. (Pelican only mode)'
        )
    return parser.parse_args()

def parse_wrkday(args):
    '''creates a Dates object with content from args entry'''
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
        message('invalid entry: %s' %(ex), level=False)
    else:
        message('valid date: %s' %(wrkday), shout=True)
        return Dates(wrkday)

def main():
    '''the main'''
    message('main called')

    args = arg_parser()
    wrkday = parse_wrkday(args)

    if wrkday:
        for gate in getgatelist().keys():
            gtn = Names(gate, wrkday)

            if not args.nonet:

                if wrkday.date() == Dates(date.today()).date():
                    message('this is today, say cheese', shout=True)
                    message(gtn.snapshot(), shout=True)
                    message(gtn.remotecommands(), shout=True)
                message('trying to load graph', shout=True)
                message(gtn.getsnapshot(), shout=True)

            message('writing article', shout=True)
            gtn.mkpost()

        message('feeding the pelican', shout=True)
        mkpelican()

        message('all done', shout=True)


if __name__ == '__main__':
    main()
