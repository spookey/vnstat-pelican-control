'''configures things'''

from os import path, pardir

MODULE_PATH = path.dirname(path.realpath(__file__))
PELIC_PATH = path.realpath(path.join(MODULE_PATH, pardir))
PELIC_CONTENT = path.join(PELIC_PATH, 'content')
PELIC_IMAGESUB = 'images'
PELIC_IMAGE = path.join(PELIC_CONTENT, PELIC_IMAGESUB)
PELIC_OUTPUT = path.join(PELIC_PATH, 'output')
PELIC_CONFIG = path.join(PELIC_PATH, 'pelicanconf.py')
def pelic_theme(tailp):
    return path.join(PELIC_PATH, tailp)

VERBOSE = False
CODING = 'UTF-8'

POSTCONTENT = '''
Title: {gateway} Status {date}
Date: {date} 23:23
Category: {gateway} Status
Tags: {year}-{month}, {year}, {month}, {day}, {ifaces}

{gateway} Status: {date}

'''

POSTIMAGES = '''
##{iface}

![{gateway} Status {filedate}]({{filename}}/{imgfile})
'''

GATELIST = {
    'Gate05': {
        'ssh_host': 'ns3095578.ip-94-23-58.eu',
        'ssh_user': 'monitor',
        'ssh_port': '22',
        'ssh_identity': path.join(path.expanduser('~'), '.ssh/gate05_monitor_rsa'),
        'file_path': '/home/monitor/stats',
        'graph_devices': ['eth0'],
    },
}
