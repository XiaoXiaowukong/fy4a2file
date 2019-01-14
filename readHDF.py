# -*- coding: utf-8 -*-
from h5py import File as h5File
import numpy as np
from projection import latlon2lc
from numpy import rint

# 各分辨率文件包含的通道号
CONTENTS = {"0500M": ("Channel02",),
            "1000M": ("Channel01", "Channel02", "Channel03"),
            "2000M": tuple(["Channel{x:02d}" for x in range(1, 8)]),
            "4000M": tuple(["Channel{x:02d}" for x in range(1, 15)])}
# 各分辨率行列数
SIZES = {"0500M": 21984,
         "1000M": 10992,
         "2000M": 5496,
         "4000M": 2748}


class FY4A_H5(object):
    def __init__(self, hdf5File, channelnames=None):
        # 获得h5文件对象、记录读取状态
        self.h5file = h5File(hdf5File, 'r')
        self.channelnames = channelnames or CONTENTS[hdf5File[-15:-10]]
        self.channels = {x: None for x in self.channelnames}
        self.channelsValues = []
        self.geo_range = None
        self.l = None
        self.c = None
        self.l_begin = self.h5file.attrs["Begin Line Number"]
        self.l_end = self.h5file.attrs["End Line Number"]
        # if geo_range is not None:
        #     self.lat_S, self.lat_N, self.lon_W, self.lon_E, self.step = geo_range

    def __del__(self):
        # 确保关闭h5文件
        self.h5file.close()

    def extract(self, channelnames, geo_range=None, resolution=None):
        """
        最邻近插值提取
        l：行号
        c：列号
        channelnames：提取的通道名（两位数字字符串序列）
        返回字典
        暂时没有处理缺测值（异常）
        REGC超出范围未解决
        """
        for channelname in channelnames:
            NOMChannelname = "NOM" + channelname
            CALChannelname = "CAL" + channelname
            # 若geo_range没有指定，则读取全部数据，不定标
            if geo_range is None:
                channel = self.h5file[NOMChannelname].value
                self.channels[channelname] = channel
                return None
            geo_range_final = eval(geo_range)
            if self.geo_range != geo_range_final:
                self.geo_range = geo_range_final
                lat_S, lat_N, lon_W, lon_E, step = geo_range_final
                lat = np.arange(lat_N, lat_S - 0.005, -step)
                lon = np.arange(lon_W, lon_E + 0.005, step)
                lon, lat = np.meshgrid(lon, lat)
                if (resolution is None):
                    return None
                self.l, self.c = latlon2lc(lat, lon, resolution)  # 求标称全圆盘行列号
                self.l = rint(self.l).astype(np.uint16)
                self.c = rint(self.c).astype(np.uint16)
            # DISK全圆盘数据和REGC中国区域数据区别在起始行号和终止行号
            channel = self.h5file[NOMChannelname].value[self.l - self.l_begin, self.c]
            #暂时处理
            channel[channel == 65534] = np.nan
            channel[channel == 65535] = np.nan
            CALChannel = self.h5file[CALChannelname].value  # 定标表
            # self.channels[channelname] = CALChannel[channel]  # 缺测值
            self.channelsValues.append(CALChannel[channel])
        self.channelsValues = np.asarray(self.channelsValues)
