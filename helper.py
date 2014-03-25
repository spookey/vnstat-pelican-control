'''helps doing things'''

from os import path
from subprocess import PIPE, Popen
from config import VERBOSE, CODING

def writefile(filename, content):
    '''writes content in filename'''
    if path.exists(path.dirname(filename)):
        if content:
            with open(filename, 'w') as fileh:
                fileh.write(content)
    else:
        print(':: %s does not exist' %(path.dirname(filename)))
        return

def localrun(cmdline):
    '''runs a command on the local shell'''
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
        if VERBOSE:
            print(':: targetpath %s does not exist' %(target))

