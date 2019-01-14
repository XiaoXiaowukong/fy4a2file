# fy4HDF2file fy4AHDF数据转换为img(HFA)格式

## 运行环境
* python 2.7

## 依赖库
* numpy 版本:1.15.3 
* h5py  版本:2.7.1 
* gdal 版本:>=2.1

# 内部调用
## 使用说明（带*为必传参数）
* ***hdf5_files** 输入HDF文件，多个用","隔开
* ***export_files** 输出文件，多个用","隔开
* channel_names 要提取的通道名 默认14个通道
* geo_range 提取数据范围及步长 例如"10,54,70,140,0.05" 默认是"10,54,70,140,0.05"
* nodata 设置nodata值，默认None
* resolution 原始数据分辨率 ("0500M", "1000M", "2000M", "4000M") 默认"4000M"

## 调用示例
```angular2html
    myFY4AMain = FY4AMain()
    myFY4AMain.initParams(hdf5_files="a.HDF,b.HDF",export_files="c.img,d.img")

```
# 外部调用
## 使用说明（带*为必传参数）
* ***--hdf5_files** 输入HDF文件，多个用","隔开
* ***--export_files** 输出文件，多个用","隔开
* --channel_names 要提取的通道名 默认14个通道
* --geo_range 提取数据范围及步长 例如"10,54,70,140,0.05" 默认是"10,54,70,140,0.05"
* --nodata 设置nodata值，默认None
* --resolution 原始数据分辨率 ("0500M", "1000M", "2000M", "4000M") 默认"4000M"
## 调用示例
```angular2html
python fy4aMain.py --hdf5_files a.HDF,b.HDF \
                    --export_files ./c.img,./d.img
```