import gdal
import numpy as np
import time
import joblib

start = time.time()

with open('Y:/germany-drought/germany.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

input_lst = ['Y:/germany-drought/level4/' + item + '/2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TY_C95T_TSI.tif' for item in tiles_lst]
out_name_lst = [r'Y:/germany-drought/level4/' + item + r'/VCI_2018_001-365.tif'  for item in tiles_lst]

job_lst = [[input_lst[i], out_name_lst[i]] for i in range (len(input_lst))]

## Optional check job list
for i, job in enumerate(job_lst):
   print(i+1)
   print(job)

def workFunc(job):
    print("Start: " + job[0])

    input_name = job[0]

    ras = gdal.Open(input_name)
    output_name = job[1]

    start = time.time()
    arr = ras.ReadAsArray()
    end = time.time()
    print("Reading Array:", end - start)

    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()

    no_data_value = -32767
    arr_2018 = arr[366:366 + 73, :, :]
    i = 0

    vci_fill = arr_2018.copy() * 0
    vci_list = []
    for i in range(73):
        index_lst = [i, i + 73, i + 2 * 73, i + 3 * 73, i + 4 * 73]
        doy_ts = arr[index_lst, :, :]

        doy_ts[doy_ts == no_data_value] = 10001
        arr_min = np.min(doy_ts)

        doy_ts[doy_ts == 10001] = no_data_value
        arr_max = np.max(doy_ts)

        doy_2018 = arr_2018[i, :, :]
        vci = (doy_2018 - arr_min) / (arr_max + arr_min)

        vci_list.append(vci)

    vci_output = np.array(vci_list)

    nbands = vci_output.shape[0]
    x_res = vci_output.shape[2]
    y_res = vci_output.shape[1]

    target_ds = gdal.GetDriverByName('GTiff').Create(output_name, x_res, y_res, nbands, gdal.GDT_Float32)
    target_ds.SetGeoTransform(gt)
    target_ds.SetProjection(pr)

    for i in range(nbands):
        band = target_ds.GetRasterBand(i + 1)
        vci_output_sub = vci_output[i, :, :]
        band.WriteArray(vci_output_sub)
        band.SetNoDataValue(-9999)
        band.FlushCache()

    del target_ds

    print("Done: " + job[0])


if __name__ == '__main__':
    joblib.Parallel(n_jobs=4)(joblib.delayed(workFunc)(i) for i in job_lst)

end = time.time()
print("Duration:", end - start)

# def unmaskArray(masked_arr):
#     arr = np.ma.MaskedArray.tolist(masked_arr)
#     arr = np.array(arr)
#
#     return arr
#
# # slow but no division by zero
# def calculateVCI_(ts, no_data_value):
#
#     ts_ma = np.ma.masked_where(ts == no_data_value, ts)
#     #ts_ma.astype(float)
#
#     ndvi_min = np.min(ts_ma)
#     ndvi_max = np.max(ts_ma)
#
#     vci = (ts_ma - ndvi_min) / (ndvi_max + ndvi_min)
#
#     return vci
#
# # faster, but division by zero
# def calculateVCI(ts, no_data_value):
#
#     ts_ma = np.copy(ts)
#     ts_ma = ts_ma.astype(float)
#     ts_ma[ts_ma == no_data_value] = np.nan
#
#     ndvi_min = np.nanmin(ts_ma)
#     ndvi_max = np.nanmax(ts_ma)
#
#     vci = (ts_ma - ndvi_min) / (ndvi_max + ndvi_min)
#
#     return vci
#
# # faster, but division by zero
# def calculateVCI3(ts, no_data_value):
#
#     ts_ma = np.copy(ts)
#     ts_ma[ts_ma == no_data_value] = 10001
#     ndvi_min = np.min(ts_ma)
#
#     ts_ma[ts_ma == 10001] = no_data_value
#     ndvi_max = np.max(ts_ma)
#
#     ts_bool = np.where(ts_ma == no_data_value,0, 1)
#
#     vci = (ts_ma - ndvi_min) / (ndvi_max + ndvi_min)
#     #vci = vci * ts_bool
#     vci[ts_bool == 0] = -9999
#
#     return vci



#
# vci_arr = np.apply_along_axis(arr=arr_sub, axis=0, func1d=calculateVCI3, no_data_value = -32767)
# vci_arr1 = np.apply_along_axis(arr=arr_sub, axis=0, func1d=calculateVCI_, no_data_value = -32767)
# vci_arr1 = unmaskArray(vci_arr1)
#
# slice_i = 0
# year_i = 1
# for year_i in range(1,8):
#     year = year_i + 2012
#     year_arr = vci_arr[slice_i : slice_i + 73,:,:]
#
#     slice_i =  slice_i + 73
#
#     output_name_year = output_name + str(year) + "_001-365.tif"
#
#     nbands = year_arr.shape[0]
#     x_res = year_arr.shape[2]
#     y_res = year_arr.shape[1]
#
#     target_ds = gdal.GetDriverByName('GTiff').Create(output_name_year, x_res, y_res, nbands, gdal.GDT_Float32)
#     target_ds.SetGeoTransform(gt)
#     target_ds.SetProjection(pr)
#
#     for i in range(nbands):
#         band = target_ds.GetRasterBand(i+1)
#         year_arr_sub = year_arr[i,:,:]
#         band.WriteArray(year_arr_sub)
#         band.SetNoDataValue(-9999)
#         band.FlushCache()
#
#     del target_ds







#
#     gt = ras.GetGeoTransform()
#     pr = ras.GetProjection()
#
#     x_res = ras.RasterXSize
#     y_res = ras.RasterYSize
#
#     arr = ras.ReadAsArray()
#
#     vci_arr = np.apply_along_axis(arr=arr, axis=0, func1d=calculateVCI_, no_data_value = -32767)
#
#     nbands = vci_arr.shape[0]
#
#     target_ds = gdal.GetDriverByName('GTiff').Create(output_name, x_res, y_res, nbands, gdal.GDT_Int16)
#     target_ds.SetGeoTransform(gt)
#     target_ds.SetProjection(pr)
#
#     for i in range(nbands):
#         band = target_ds.GetRasterBand(i+1)
#         vci_arr_sub = vci_arr[i,:,:]
#         band.WriteArray(vci_arr_sub)
#         band.SetNoDataValue(-9999)
#         band.FlushCache()
#
#     del target_ds
#
#     print("Done: " + job[0])
#

#
# end = time.time()
# print(end - start)