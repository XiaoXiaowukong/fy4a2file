from fy4aMain import FY4AMain

if __name__ == '__main__':
    # hdf5File = "/Volumes/pioneer/FY4/FY-4A/FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20181202040000_20181202041459_4000M_V0001.HDF,/Volumes/pioneer/FY4/FY-4A/FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20181202040000_20181202041459_4000M_V0001.HDF"
    hdf5File = "/Volumes/pioneer/FY4/FY-4A/FY4A-_AGRI--_N_REGC_1047E_L1-_FDI-_MULT_NOM_20181202111500_20181202111916_4000M_V0001.HDF"
    myFY4AMain = FY4AMain()
    myFY4AMain.initParams(hdf5_files=hdf5File,export_files="./a.img")
