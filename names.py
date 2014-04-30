'''deals with names'''

from os import path
from datetime import date
from config import PELIC_IMAGESUB, PELIC_CONTENT, PELIC_IMAGE, POSTCONTENT, POSTIMAGES, POSTCOMMAND
from helper import message, remoterun, remoteget, writefile, getgatelist

class Dates(object):
    '''watches in his pocket calendar'''
    wrkday = None

    def __init__(self, wrkday):
        if isinstance(wrkday, date):
            self.wrkday = wrkday
        else:
            raise Exception('wrong datetime.date object')
        self.__postinit()

    def __postinit(self):
        '''init afterparty'''
        msg = 'current scope: %s' %(self.date())
        message(msg)
        message(':' * len(msg))

    def date(self):
        '''date with - '''
        return self.wrkday.strftime('%Y-%m-%d')

    def filedate(self):
        '''date with _ (for filenames)'''
        return self.date().replace('-', '_')

    def year(self):
        '''year'''
        return self.wrkday.strftime('%Y')

    def month(self):
        '''month'''
        return self.wrkday.strftime('%m')

    def day(self):
        '''day'''
        return self.wrkday.strftime('%d')

class Names(object):
    '''they call him names'''
    gate = None
    gatename = None
    date = None
    rcmdout = None

    def __init__(self, gateway, wrkdate):
        if getgatelist()[gateway]:
            self.gate = getgatelist()[gateway]
            self.gatename = gateway
            self.date = wrkdate
            self.rcmdout = None
        else:
            raise Exception('wrong names.Dates object')
        msg = 'current gate: %s' %(gateway)
        message(msg)
        message('.' * len(msg))

    def image_local(self):
        '''local images'''
        images = self.image_pelic()
        images.update(
            (iface, path.join(PELIC_CONTENT, pimg))
                for iface, pimg in images.items()
            )
        return images

    def image_remote(self):
        '''remote images'''
        images = self.image_pelic()
        images.update(
            (iface, path.join(self.gate['file_path'], path.basename(pimg)))
            for iface, pimg in images.items()
            )
        return images

    def image_pelic(self):
        '''pelican intern images'''
        result = dict()
        for iface in self.gate['graph_devices']:
            result[iface] = path.join(PELIC_IMAGESUB, '_'.join([self.gatename, iface, self.date.filedate()]) + '.png')
        return result

    def _vnstat_cmds(self):
        '''preparing camera'''
        vncmd = str()
        for iface, rpath in self.image_remote().items():
            vncmd += 'vnstati -i %s -vs -ne -o %s; ' %(iface, rpath)
        return vncmd

    def snapshot(self):
        '''executes remote snapshot commands'''
        return remoterun(
            self.gate['ssh_user'],
            self.gate['ssh_host'],
            self.gate['ssh_port'],
            self.gate['ssh_identity'],
            self._vnstat_cmds()
            )

    def getsnapshot(self):
        '''downloads remote snapshots'''
        return remoteget(
            self.gate['ssh_user'],
            self.gate['ssh_host'],
            self.gate['ssh_port'],
            self.gate['ssh_identity'],
            list(self.image_remote().values()),
            PELIC_IMAGE
            )

    def _check_images(self):
        '''do images exist local'''
        result = dict()
        for iface, lpath in self.image_local().items():
            result[iface] = path.exists(lpath)
        return result

    def existing_images(self):
        '''all local existing images (for a post)'''
        return [iface for iface, state in self._check_images().items() if state is True]

    def remotecommands(self):
        '''run remote commands'''
        if self.gate['commands']:
            self.rcmdout = dict()
            for command in self.gate['commands']:
                self.rcmdout[command] = remoterun(
                    self.gate['ssh_user'],
                    self.gate['ssh_host'],
                    self.gate['ssh_port'],
                    self.gate['ssh_identity'],
                    command
                    )

    def markdown_path(self):
        '''where is my markdown file today?'''
        return path.join(PELIC_CONTENT, '%s_%s.md' %(self.gatename, self.date.filedate()))

    def content(self):
        '''writes beautiful blog entries'''
        pimages = self.image_pelic()
        images = self.existing_images()
        tagifaces = str()
        imageblock = str()

        for iface in images:
            tagifaces += '%s-%s, ' %(self.gatename, iface)
            imageblock += POSTIMAGES.format(
                gateway=self.gatename, iface=iface,
                filedate=self.date.filedate(), imgfile=pimages[iface]
            )

        content = POSTCONTENT.format(
            gateway=self.gatename, ifaces=tagifaces, date=self.date.date(),
            year=self.date.year(), month=self.date.month(), day=self.date.day()
            ).lstrip() + imageblock

        if self.rcmdout:
            rcmdlist = self.rcmdout.keys()
            for rcommand in sorted(rcmdlist):
                rcblock = str()
                for rcline in self.rcmdout[rcommand].split('\n'):
                    rcblock += '\n\t%s' %(rcline)
                content += POSTCOMMAND.format(command=rcommand, commandoutput=rcblock)

        if len(images) == 0:
            message('no images for %s [%s] found. skipping' %(self.gatename, self.date.date()), level=False)
            return
        return content

    def mkpost(self):
        '''puts content into markdown'''
        return writefile(self.markdown_path(), self.content())
