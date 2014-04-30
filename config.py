'''configures things'''

from os import path, pardir

MODULE_PATH = path.dirname(path.realpath(__file__))
LOGFILE = path.join(MODULE_PATH, 'logs/logfile.log')
PELIC_PATH = path.realpath(path.join(MODULE_PATH, pardir))
PELIC_CONTENT = path.join(PELIC_PATH, 'content')
PELIC_IMAGESUB = 'images'
PELIC_IMAGE = path.join(PELIC_CONTENT, PELIC_IMAGESUB)
PELIC_OUTPUT = path.join(PELIC_PATH, 'output')
PELIC_CONFIG = path.join(PELIC_PATH, 'pelicanconf.py')
GATES_PATH =  path.join(PELIC_PATH, 'gates')
GATELIST = path.join(GATES_PATH, 'hosts.json')

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

POSTCOMMAND = '''
####{command}

{commandoutput}
'''

