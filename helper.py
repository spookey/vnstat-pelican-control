'''helps doing things'''

from os import path
from subprocess import PIPE, Popen
from config import CODING, NOW, CONTENTPATH, OUTPUTPATH, PELCONFIG, IMGSUBPATH, GATELIST, POSTCONTENT, POSTIMAGES

def writefile(filename, content):
    '''writes content in filename'''
    if not path.exists(path.dirname(filename)):
        print('%s does not exist' %(path.dirname(filename)))
        return
    with open(filename, 'w') as fileh:
        fileh.write(content)

def _getdate(nicefmt=True):
    '''date'''
    sep = '-' if nicefmt else '_'
    return NOW.strftime('%Y{sep}%m{sep}%d'.format(sep=sep))

def _gettime():
    '''time'''
    return NOW.strftime('%H:%M')

def _gettyear():
    '''tag year'''
    return NOW.strftime('%Y')

def _gettmonth():
    '''tag month as abbr'''
    return NOW.strftime('%b')

def _gettday():
    '''tag today'''
    return NOW.strftime('%d')

def getimg_files(gateway, full=True):
    '''status image file path'''
    if GATELIST[gateway]:
        result = list()
        for iface in GATELIST[gateway]['graph_devices']:
            tailp = '%s/%s_%s_%s.png' %(IMGSUBPATH, gateway, iface, _getdate(nicefmt=False))
            if full:
                result.append(path.join(CONTENTPATH, tailp))
            else:
                result.append(tailp)
        return result

def getremoteimg_files(gateway):
    '''status image file path on remote location'''
    if GATELIST[gateway]:
        result = list()
        for iface in GATELIST[gateway]['graph_devices']:
            result.append(path.join(GATELIST[gateway]['file_path'], '%s_%s_%s.png' %(gateway, iface, _getdate(nicefmt=False))))
        return result

def getgraph_cmds(gateway):
    '''returns graphcommand for gateway'''
    if GATELIST[gateway]:
        graphcommand = ''
        for iface in GATELIST[gateway]['graph_devices']:
            graphcommand += 'vnstati -i %s -vs -o %s/%s_%s_%s.png; ' %(iface, GATELIST[gateway]['file_path'], gateway, iface, _getdate(nicefmt=False))
        return graphcommand

def getmd_file(gateway, full=True):
    '''markdown file path'''
    tailp = '%s_%s.md' %(gateway, _getdate(nicefmt=False))
    return path.join(CONTENTPATH, tailp) if full else tailp

def getpost(gateway):
    '''return post content'''
    content = POSTCONTENT.format(
        gateway=gateway, date=_getdate(), time=_gettime(),
        tyear=_gettyear(), tmonth=_gettmonth(), tday=_gettday()
    )
    for ifaceimg in getimg_files(gateway, full=False):
        if path.exists(path.join(CONTENTPATH, ifaceimg)):
            content += POSTIMAGES.format(
                gateway=gateway, date=_getdate(), time=_gettime(), imgfile=ifaceimg
            ) + '\n'
    return content

def localrun(cmdline):
    '''runs a command on the local shell'''
    try:
        print(cmdline)
        pres = Popen(cmdline.split(' '), stderr=PIPE, stdout=PIPE)
        return '\n'.join([p.decode(encoding=CODING) for p in pres.communicate()])

    except (OSError, TypeError) as ex:
        return ex

def remoterun(gateway, cmdline):
    '''runs a command on a remote shell'''
    if GATELIST[gateway]:
        cmdline = 'ssh -p %s -i %s %s@%s %s' %(GATELIST[gateway]['ssh_port'], GATELIST[gateway]['ssh_identity'], GATELIST[gateway]['ssh_user'], GATELIST[gateway]['ssh_host'], cmdline)
        return localrun(cmdline)

def remoteget(gateway, sources, target):
    '''gets remote files'''
    if GATELIST[gateway]:
        if path.exists(target):
            sfiles = str()
            if len(sources) > 1:
                sfiles = '{' + ','.join(sources) + '}'
            else:
                sfiles = ''.join(sources)
            cmdline = 'scp -P %s -i %s %s@%s:%s %s' %(GATELIST[gateway]['ssh_port'], GATELIST[gateway]['ssh_identity'], GATELIST[gateway]['ssh_user'], GATELIST[gateway]['ssh_host'], sfiles, target)
            return localrun(cmdline)
        else:
            print('path %s does not exist' %(target))
            return

def make_pelican():
    return localrun('pelican %s -o %s -s %s' %(CONTENTPATH, OUTPUTPATH, PELCONFIG))

