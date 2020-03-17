import gdal
import numpy as np
import math



# output_folder = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\'
#
#
# if j < 10:
#     ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_0' + str(j) + '_01.tif')
#
#     if n_months < 10:
#         output_path = output_folder + r'\RSMS\RSMS_0' + str(j) + '_0' + str(n_months) + '_mean.tif'
#     else:
#         output_path = output_folder + r'\RSMS\RSMS_0' + str(j) + '_' + str(n_months) + '_mean.tif'
#
# else:
#     ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_' + str(j) + '_01.tif')
#
#     if n_months < 10:
#         output_path = output_folder + r'\RSMS\RSMS_' + str(j) + '_0' + str(n_months) + '_mean.tif'
#     else:
#         output_path = output_folder + r'\RSMS\RSMS_' + str(j) + '_' + str(n_months) + '_mean.tif'

ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_01-12_1970-2018.tif')

n_months = 6
if n_months < 10:
    output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_01-12_1970-2018_mean0' + str(n_months) + '.tif'
else:
    output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_01-12_1970-2018_mean' + str(n_months) + '.tif'

print('Start:', output_path)
arr = ras.ReadAsArray()

nbands = ras.RasterCount
x_res = ras.RasterXSize
y_res = ras.RasterYSize

gt = ras.GetGeoTransform()
pr = ras.GetProjection()

nbands_out = nbands - n_months + 1

arr_list = []

for i in range(nbands_out):
    arr_sub = arr[i : i+n_months,:,:]
    arr_mean = np.mean(arr_sub, axis=0) # np.sum
    arr_mean[arr_mean < 0] = -999
    arr_list.append(arr_mean)

arr_final = np.array(arr_list)

target_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
target_ds.SetGeoTransform(gt)
target_ds.SetProjection(pr)

for i in range(0, nbands_out ):
    band = target_ds.GetRasterBand(i + 1)
    arr_out = arr_final[i,:,:]
    band.WriteArray(arr_out)
    no_data_value = -999
    band.SetNoDataValue(no_data_value)
    band.FlushCache()

del(target_ds)