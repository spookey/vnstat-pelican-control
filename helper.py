'''helps doing things'''

from os import path
from subprocess import PIPE, Popen
from pelican.settings import get_settings_from_file, configure_settings
from pelican import Pelican
from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler
from config import VERBOSE, CODING, LOGFILE, PELIC_PATH, PELIC_CONFIG, PELIC_CONTENT, PELIC_OUTPUT

FILEHANDLER = RotatingFileHandler(LOGFILE, 'a', 1 * 1024 * 1024, 10)
FILEHANDLER.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
LOG = getLogger('vnstat-pelican-control')
LOG.setLevel(INFO)
LOG.addHandler(FILEHANDLER)

def message(msg, level=None, shout=False, *args, **kwargs):
    '''logs output'''
    sev = {
        None: LOG.info,
        True: LOG.warning,
        False: LOG.error,
    }
    if level in sev.keys():
        sev[level](msg, *args, **kwargs)
    if VERBOSE or level == False or shout == True:
        print(':: %s' %(msg))

def writefile(filename, content):
    '''writes content in filename'''
    if path.exists(path.dirname(filename)):
        if content:
            with open(filename, 'w') as fileh:
                fileh.write(content)
            message('written %s [%s]' %(filename, content[:23]))
    else:
        message('%s does not exist' %(path.dirname(filename)), level=False)
        return

def localrun(cmdline):
    '''runs a command on the local shell'''
    message('running: %s' %(cmdline), shout=True)
    try:
        pres = Popen(cmdline.split(' '), stderr=PIPE, stdout=PIPE)
        return '\n'.join([p.decode(encoding=CODING) for p in pres.communicate()])
    except (OSError, TypeError) as ex:
        return ex

def remoterun(user, host, port, key_file, command):
    '''runs a command on a remote shell'''
    cmdline = 'ssh -p %s -i %s %s@%s %s' %(port, key_file, user, host, command)
    return localrun(cmdline)

def remoteget(user, host, port, key_file, sources, target):
    '''gets remote files'''
    if path.exists(target):
        sfiles = str()
        if len(sources) > 1:
            sfiles = '{' + ','.join(sources) + '}'
        else:
            sfiles = ''.join(sources)
        cmdline = 'scp -P %s -i %s %s@%s:%s %s' %(port, key_file, user, host, sfiles, target)
        return localrun(cmdline)
    else:
        message('targetpath %s does not exist' %(target), level=False)

def mkpelican():
    '''runs pelican build'''
    def fullthemepath(tpath):
        '''joins theme path'''
        return path.join(PELIC_PATH, tpath)
    psettings = get_settings_from_file(PELIC_CONFIG)
    psettings['PATH'] = PELIC_CONTENT
    psettings['OUTPUT_PATH'] = PELIC_OUTPUT
    psettings['THEME'] = fullthemepath(psettings['THEME'])

    message('running something similar to \'pelican -t %s -s %s %s -o %s\'' %(psettings['THEME'], PELIC_CONFIG, PELIC_CONTENT, PELIC_OUTPUT), shout=True)
    pinst = Pelican(configure_settings(psettings))
    pinst.run()


