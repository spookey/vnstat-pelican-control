'''does things'''

from config import GATELIST, IMGPATH
from helper import remoterun, remoteget, writefile, getgraph_cmds, getremoteimg_files, getmd_file, getpost, make_pelican

if __name__ == '__main__':
    for gate in GATELIST.keys():
        remoterun(gate, getgraph_cmds(gate))
        remoteget(gate, getremoteimg_files(gate), IMGPATH)
        writefile(getmd_file(gate), getpost(gate))
    make_pelican()
