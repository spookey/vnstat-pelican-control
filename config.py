'''configures things'''

from os import path
from datetime import datetime

NOW = datetime.now()
MODULEPATH = path.dirname(path.realpath(__file__))
CONTENTPATH = path.join(MODULEPATH, '../content')
IMGSUBPATH = 'images'
IMGPATH = path.join(CONTENTPATH, IMGSUBPATH)
OUTPUTPATH = path.join(MODULEPATH, '../output')
# PELCONFIG = path.join(MODULEPATH, '../publishconf.py')
PELCONFIG = path.join(MODULEPATH, '../pelicanconf.py')

CODING = 'UTF-8'

POSTCONTENT = '''Title: {gateway} Status {date}
Date: {date} {time}
Category: {gateway} Status
Tags: {tyear}-{tmonth}, {tyear}, {tmonth}, {tday}

{gateway} Status: {date}, {time}

'''

POSTIMAGES = '![{gateway} Status {date} {time}]({{filename}}/{imgfile})'

GATELIST = {
    'Gate05': {
        'ssh_host': 'ns3095578.ip-94-23-58.eu',
        'ssh_user': 'monitor',
        'ssh_port': '22',
        'ssh_identity': path.join(path.expanduser('~'), '.ssh/gate05_monitor_rsa'),
        'file_path': '/home/monitor/stats',
        'graph_devices': ['eth0'],
        'test_test': 'Wurst',
    },
}
