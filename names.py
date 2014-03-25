'''deals with names'''

from os import path
from datetime import date
from config import VERBOSE, GATELIST, PELIC_IMAGESUB, PELIC_CONTENT, PELIC_IMAGE, POSTCONTENT, POSTIMAGES
from helper import remoterun, remoteget, writefile

class Dates(object):
    wrkday = None

    def __init__(self, wrkday):
        if isinstance(wrkday, date):
            self.wrkday = wrkday
        else:
            raise
        self.__postinit()

    def __postinit(self):
        msg = ':: current scope: %s' %(self.date())
        if VERBOSE:
            print(msg)
            print(':' * len(msg))

    def date(self):
        return self.wrkday.strftime('%Y-%m-%d')

    def filedate(self):
        return self.date().replace('-','_')

    def year(self):
        return self.wrkday.strftime('%Y')

    def month(self):
        return self.wrkday.strftime('%m')

    def day(self):
        return self.wrkday.strftime('%d')

class Names(object):
    gate = None
    gatename = None
    date = None

    def __init__(self, gateway, date):
        if GATELIST[gateway]:
            self.gate = GATELIST[gateway]
            self.gatename = gateway
            self.date = date
        else:
            raise
        msg = ':: current gate: %s' %(gateway)
        if VERBOSE:
            print(msg)
            print('.' * len(msg))

    def image_local(self):
        images = self.image_pelic()
        images.update((iface, path.join(PELIC_CONTENT, pimg)) for iface, pimg in images.items())
        return images

    def image_remote(self):
        images = self.image_pelic()
        images.update((iface, path.join(self.gate['file_path'], path.basename(pimg))) for iface, pimg in images.items())
        return images

    def image_pelic(self):
        result = dict()
        for iface in self.gate['graph_devices']:
            result[iface] = path.join(PELIC_IMAGESUB, '_'.join([self.gatename, iface, self.date.filedate()]) + '_test.png')
        return result

    def _vnstat_cmds(self):
        vncmd = str()
        for iface, rpath in self.image_remote().items():
            vncmd += 'vnstati -i %s -vs -ne -o %s; ' %(iface, rpath)
        return vncmd

    def snapshot(self):
        return(remoterun(self.gate['ssh_user'], self.gate['ssh_host'], self.gate['ssh_port'], self.gate['ssh_identity'], self._vnstat_cmds()))

    def getsnapshot(self):
        return(remoteget(self.gate['ssh_user'], self.gate['ssh_host'], self.gate['ssh_port'], self.gate['ssh_identity'], list(self.image_remote().values()), PELIC_IMAGE))

    def _check_images(self):
        result = dict()
        for iface, lpath in self.image_local().items():
            result[iface] = path.exists(lpath)
        return result

    def existing_images(self):
        return [iface for iface, state in self._check_images().items() if state is True]

    def markdown_path(self):
        return path.join(PELIC_CONTENT, '%s_%s.md' %(self.gatename, self.date.filedate()))

    def content(self):
        pimages = self.image_pelic()
        images = self.existing_images()
        tagifaces = str()
        imageblock = str()

        for iface in images:
            tagifaces += '%s-%s, ' %(self.gatename, iface)
            imageblock += POSTIMAGES.format(
                gateway=self.gatename, iface=iface, filedate=self.date.filedate(), imgfile=pimages[iface]
            )

        content = POSTCONTENT.format(
            gateway=self.gatename, ifaces=tagifaces, date=self.date.date(),
            year=self.date.year(), month=self.date.month(), day=self.date.day()
            ).lstrip() + imageblock


        if len(images) == 0:
            print(':: no images found ~ skipping')
            return
        return content

    def mkpost(self):
        return writefile(self.markdown_path(), self.content())
