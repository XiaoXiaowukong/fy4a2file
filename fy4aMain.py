# -*- coding:utf-8 -*-
__version__ = '$Id: fy4amain.py 2019-01-14 rouault $'
from readHDF import FY4A_H5
import numpy as np
from createFY4Afile import CreateFY4AFile
import time
import sys
resolution_list = ("0500M", "1000M", "2000M", "4000M")
channelnames = (
    "Channel01", "Channel02", "Channel03", "Channel04", "Channel05", "Channel06", "Channel07", "Channel08",
    "Channel09",
    "Channel10", "Channel11", "Channel12", "Channel13", "Channel14")


class FY4AMain():
    def __init__(self):
        pass

    def initParams(self, **kwargs):
        arguments = []
        for kwarg_key in kwargs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwargs[kwarg_key])
        self.optparse_init()
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        if (self.options.hdf5Files != None):
            self.options.hdf5Files = self.options.hdf5Files.split(",")
        if (self.options.exportFiles != None):
            self.options.exportFiles = self.options.exportFiles.split(",")
        print self.options
        self.process()
        # 外部调用接口

    def outsideParams(self, arguments):
        self.optparse_init()
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        if (self.options.hdf5Files != None):
            self.options.hdf5Files = self.options.hdf5Files.split(",")
        if (self.options.exportFiles != None):
            self.options.exportFiles = self.options.exportFiles.split(",")
        print self.options
        self.process()

    def process(self):
        for hdf5FileIndex, hdf5File in enumerate(self.options.hdf5Files):
            fy4ahdf5 = FY4A_H5(hdf5File, channelnames)
            fy4ahdf5.extract(channelnames, self.options.geoRange, self.options.resolution)
            self.data = fy4ahdf5.channelsValues
            self.createLatLon()
            self.wirteFile(self.options.exportFiles[hdf5FileIndex])

    def createLatLon(self):
        lat_S, lat_N, lon_W, lon_E, step = eval(self.options.geoRange)
        self.lat = np.arange(lat_N, lat_S - 0.01, -step)
        self.lon = np.arange(lon_W, lon_E + 0.01, step)

    def wirteFile(self, exportFile):
        myCreateFY4AFile = CreateFY4AFile()
        myCreateFY4AFile.wirte(self.lat, self.lon, self.data, self.options.nodata, "img", exportFile)

    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        p.add_option(
            '--hdf5_files',
            dest='hdf5Files',
            help='input fy4 hdf files'
        )
        p.add_option(
            '--channel_names',
            dest='channelNames',
            help='fy4a file channelnames'
        )
        # "10,54,70,140,0.05"
        p.add_option(
            '--geo_range',
            dest='geoRange',
            help='lat lon range'
        )
        p.add_option(
            '--resolution',
            dest='resolution',
            type='choice',
            choices=resolution_list,
            help='fy4a file resolution type'
        )
        p.add_option(
            '--nodata',
            dest='nodata',
            help='nodata value'
        )
        p.add_option(
            '--export_files',
            dest='exportFiles',
            help="export some type files"
        )
        p.set_defaults(
            nodata=None,
            channelNames=channelnames,
            geoRange="10,54,70,140,0.05",
            resolution="4000M",

        )

        self.parser = p
if __name__ == '__main__':
    startTime = time.time()
    argv = sys.argv
    if argv:
        myFY4AMain = FY4AMain()
        myFY4AMain.outsideParams(argv[1:])
    print "end time ", time.time() - startTime