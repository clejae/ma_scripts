import gdal
import numpy as np
import joblib
import os

#abr_lst = ['LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']
abr_lst = ['LGS', 'VPS', 'VES', 'VLM', 'VBL', 'VSA', 'IBL', 'IBT', 'IGS']


input_name = r'Y:\germany-drought\level4\X0063_Y0047\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_LGS.tif'

ras = gdal.Open(input_name)
output_name = r'Y:\germany-drought\level4_analysis\X0063_Y0047\COMP-2014-2017-TO-2018_withSTD_LGS.tif'

gt = ras.GetGeoTransform()
pr = ras.GetProjection()

x_res = ras.RasterXSize
y_res = ras.RasterYSize

arr = ras.ReadAsArray()

#### DOY measures
## the logic behind the raster values
## 2014 = 365    2015 = 365      2016 = 366      2017 = 365          2018 = 365
## 0 * 365 + x   1 * 365 + x     2 * 365 + x     3 * 365 + x + 1     4 * 365 + x + 1
## DOY = x       x - 365         x - 2*365       x - 3*365 - 1       x - 4 * 365 - 1

# ref_arr = (np.sum(arr[0:4,:,:], axis=0) - 6 * 365 - 1 ) / 4
# comp_arr = (arr[4,:,:] - 4 * 365 - 1) - ref_arr


#### non-accumulative measures
#ref_arr = np.mean(arr[0:4,:,:], axis=0)
ref_arr = np.mean(arr, axis=0)
comp_arr = arr[4,:,:] - ref_arr

std_dev_arr = np.std(arr, axis=0)

mask_arr = np.where(np.abs(comp_arr)>np.abs(std_dev_arr), np.full((ref_arr.shape[0],ref_arr.shape[1]), 1), np.full((ref_arr.shape[0],ref_arr.shape[1]), 0 ))

comp_arr_m = comp_arr * mask_arr
#output_path = job[2]

# try:
#     # Create target Directory
#     os.mkdir(output_path)
#     print("Directory " , output_path ,  " Created ")
# except FileExistsError:
#     print("Directory " , output_path ,  " already exists")

target_ds = gdal.GetDriverByName('GTiff').Create(output_name, x_res, y_res, 3, gdal.GDT_Int16)
target_ds.SetGeoTransform(gt)
target_ds.SetProjection(pr)

band = target_ds.GetRasterBand(1)
band.WriteArray(comp_arr)
band.SetNoDataValue(-999)
band.FlushCache()

band = target_ds.GetRasterBand(2)
band.WriteArray(std_dev_arr)
band.SetNoDataValue(-999)
band.FlushCache()

band = target_ds.GetRasterBand(3)
band.WriteArray(comp_arr_m)
band.SetNoDataValue(-999)
band.FlushCache()

del(target_ds)

