import os
import glob
import gdal
import numpy as np

### create text file containing the download links PRECIPITATION
#txt_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\download_links_dwd_precipitation.txt'
txt_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\download_links_dwd_temperature_mean.txt'
#link_pre = 'ftp://ftp-cdc.dwd.de/pub/CDC/grids_germany/monthly/precipitation/'
link_pre = 'https://opendata.dwd.de/climate_environment/CDC/grids_germany/monthly/air_temperature_mean/'

months_lst = ['01_Jan','02_Feb','03_Mar','04_Apr','05_May','06_Jun','07_Jul','08_Aug','09_Sep','10_Oct','11_Nov','12_Dec']
with open(txt_path, "w") as f:
    for year in range(1949,2020):
        for month in months_lst:
            #link = link_pre + month + '/grids_germany_monthly_precipitation_' + str(year) + month[0:2] + '.asc.gz\n'
            link = link_pre + month + '/grids_germany_monthly_air_temp_mean_' + str(year) + month[0:2] + '.asc.gz\n'
            print(link)
            f.write(link)
f.close


# sort file based on number indicating the month

file_lst = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\*')

for file_pth in file_lst:
    month = file_pth[-9:-7]
    file_name = file_pth[-49:]
    print(file_name)
    os.rename(file_pth, r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\' + month + r'\\' + file_name )

#####-------------------------------------------------------------------------------------------------------------------
# create text file containing the download links POTENTIAL EVAPOTRANSPIRATION
txt_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\download_links_dwd_evapo_p.txt'

link_pre = 'https://opendata.dwd.de/climate_environment/CDC/grids_germany/monthly/evapo_p/'

months_lst = ['01','02','03','04','05','06','07','08','09','10','11','12']
with open(txt_path, "w") as f:
    for year in range(1991,2020):
        for month in months_lst:
            link = link_pre + 'grids_germany_monthly_evapo_p_' + str(year) + month + '.asc.gz\n'
            print(link)
            f.write(link)
f.close


# sort file based on number indicating the month

file_lst = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\*')

for file_pth in file_lst:
    month = file_pth[-9:-7]
    file_name = file_pth[-49:]
    print(file_name)
    os.rename(file_pth, r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\' + month + r'\\' + file_name )

#####-------------------------------------------------------------------------------------------------------------------
# # transform ascii files to tif PRECIPITATION
# months_lst = ['01','02','03','04','05','06','07','08','09','10','11','12']
# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\'
#
# for month_num in months_lst:
#     wd_temp = wd + month_num + r'\\*.asc'
#     file_lst = glob.glob(wd_temp)
#     for file in file_lst:
#         out_name = file[:-3] + 'tif'
#         # ras = gdal.Open(file)
#         # gt = ras.GetGeoTransform()
#         # ncols = ras.RasterXSize
#         # nrows = ras.RasterYSize
#         # pixel_width = gt[1]
#         # x_min = gt[0]
#         # y_max = gt[3]
#         # x_max = x_min + pixel_width * ncols
#         # y_min = y_max + -1*pixel_width * nrows
#
#         # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]
#         # projWin = [x_min, y_max, x_max, y_min], projWinSRS = 'EPSG:31467',
#         ds = gdal.Translate(out_name, file, options=gdal.TranslateOptions( outputSRS ='EPSG:31467' ))
#
#         del(ds)

#####-------------------------------------------------------------------------------------------------------------------
# transform ascii files to tif EVAOPO_P
wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\download'

wd_temp = wd  + r'\\*.asc'
file_lst = glob.glob(wd_temp)
for file in file_lst:
    out_name = file[:-3] + 'tif'
    ds = gdal.Translate(out_name, file, options=gdal.TranslateOptions( outputSRS ='EPSG:31467' ))

    del(ds)

#####-------------------------------------------------------------------------------------------------------------------

# stack monthly rasters --> ..., June 2017, June 2018, June 2019

# def StackRasterFromList(rasterList, outputPath):
#     """
#     Stacks the first band of n raster that are stored in a list
#     rasterList - list contatining the rasters that have the same dimensions and Spatial References
#     outputPath - Path including the name to which the stack is written
#     """
#
#     import gdal
#
#     input_ras_gt = rasterList[0].GetGeoTransform()
#
#     # set output raster definitions
#     x_min = input_ras_gt[0]
#     y_max = input_ras_gt[3]
#     x_max = x_min + input_ras_gt[1] * rasterList[0].RasterXSize
#     y_min = y_max + input_ras_gt[5] * rasterList[0].RasterYSize
#     x_res = rasterList[0].RasterXSize
#     y_res = rasterList[0].RasterYSize
#     pixel_width_x = input_ras_gt[1]
#     pixel_width_y = input_ras_gt[5]
#
#     target_ds = gdal.GetDriverByName('GTiff').Create(outputPath, x_res, y_res, len(rasterList), gdal.GDT_Float32)
#     target_ds.SetGeoTransform((x_min, pixel_width_x, 0, y_max, 0, pixel_width_y))
#     target_ds.SetProjection(rasterList[0].GetProjection())
#
#     for i in range(0, len(rasterList)):
#         band = target_ds.GetRasterBand(i + 1)
#         band.WriteArray(rasterList[i].GetRasterBand(1).ReadAsArray())
#         NoData_value = -999
#         band.SetNoDataValue(NoData_value)
#         band.FlushCache()
#
#     del(target_ds)
#
# months_lst = ['01','02','03','04','05','06','07','08','09','10','11','12']
# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\'
#
# for month_num in months_lst:
#     print('RSMS_' + month_num + '_01.tif')
#     wd_temp = wd + month_num + r'\\*.tif'
#     ras_path_list = glob.glob(wd_temp)
#     ras_list = []
#     for ras_path in ras_path_list:
#         ras = gdal.Open(ras_path)
#         ras_list.append(ras)
#
#     stack = StackRasterFromList(ras_list, r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS_' + month_num + '_01.tif')
#
#     del(stack)

#####-------------------------------------------------------------------------------------------------------------------

# create complete time series --> ..., Jan 2018, Feb 2018, ..., Apr 2019, Mar 2019 ...

# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\\'

# output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS_01-12_1970-2018.tif'
#
# file_list = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS_*01.tif')
# ras_list = [gdal.Open(file) for file in file_list]
#
# out_arr_list = []
#
# for i in range(49):
#     for ras in ras_list:
#         arr = ras.ReadAsArray()[i,:,:]
#         out_arr_list.append(arr)
#
# arr_final = np.array(out_arr_list)
#
# nbands = arr_final.shape[0]
# x_res = ras_list[0].RasterXSize
# y_res = ras_list[0].RasterYSize
#
# gt = ras_list[0].GetGeoTransform()
# pr = ras_list[0].GetProjection()
#
# target_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, nbands, gdal.GDT_Float32)
# target_ds.SetGeoTransform(gt)
# target_ds.SetProjection(pr)
#
# for i in range(0, nbands):
#     band = target_ds.GetRasterBand(i + 1)
#     arr_out = arr_final[i, :, :]
#     band.WriteArray(arr_out)
#     no_data_value = -999
#     band.SetNoDataValue(no_data_value)
#     band.FlushCache()
#
# print('Done!')


#####-------------------------------------------------------------------------------------------------------------------
# #!!!!!!!!!!!!! output order is fucked up, needs fixing!!!!!!!!!!!!!!!!!!!!!
#
# # reorder complete time series to monthly ordered time series (after calculating running mean/sum)
# # --> from ..., Jan 2018, Feb 2018, ..., Apr 2019, Mar 2019 ...
# # --> to ..., June 2017, June 2018, June 2019 etc.
#
# #!!!!!!!!!!!!! output order is fucked up, needs fixing!!!!!!!!!!!!!!!!!!!!!
#
# # order that it assigns
# # 01 02 03 04 05 06 07 08 09 10 11 12
# # order that would be correct
# # 06 07 08 09 10 11 12 01 02 03 04 05
#
# # #!!!!!!!!!!!!! output order is fucked up, needs fixing!!!!!!!!!!!!!!!!!!!!!
#
# ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_01-12_1970-2018_mean06.tif')
# arr = ras.ReadAsArray()
# nbands_in = ras.RasterCount
#
# for i in range(1,13):
#     print("Month",i)
#     monthly_arr_list = []
#     j = i - 1
#     year = 1969
#
#     while j < nbands_in:
#         year = year + 1
#         print("Year", year, "J:", j)
#         arr_sub = arr[j,:,:]
#         monthly_arr_list.append(arr_sub)
#         j = j + 12
#
#     arr_final = np.array(monthly_arr_list)
#
#     if i < 10:
#         output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_0' + str(i) + '_06.tif'
#     else:
#         output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_' + str(i) + '_06.tif'
#
#     print(arr_final.shape)
#
#     nbands_out = arr_final.shape[0]
#     x_res = arr_final.shape[2]
#     y_res = arr_final.shape[1]
#
#     gt = ras.GetGeoTransform()
#     pr = ras.GetProjection()
#
#     target_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
#     target_ds.SetGeoTransform(gt)
#     target_ds.SetProjection(pr)
#
#     for b in range(0, nbands_out):
#         band = target_ds.GetRasterBand(b + 1)
#         arr_out = arr_final[b, :, :]
#         band.WriteArray(arr_out)        no_data_value = -999
#         band.SetNoDataValue(no_data_value)
#         band.FlushCache()
#
#     print("Band", i, "done.")
#
# print("Done!")