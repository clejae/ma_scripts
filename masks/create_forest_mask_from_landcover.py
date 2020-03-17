### 1. Resample LC raster to pheno-pixel-grid

# from osgeo import gdal, gdalconst
# # Source
# #src_filename = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\europe_landcover_2015_RSE-GER.tif'
# src_filename = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\non-disturbed-forest-since-2008.tif'
# src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
# src_proj = src.GetProjection()
# src_geotrans = src.GetGeoTransform()
#
# # We want a section of source that matches this:
# match_filename = r'Y:\germany-drought\vrt\pheno-metrics\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DSS.vrt'
# match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
# match_proj = match_ds.GetProjection()
# match_geotrans = match_ds.GetGeoTransform()
# wide = match_ds.RasterXSize
# high = match_ds.RasterYSize
#
# # Output / destination
# dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\non-disturbed-forest-since-2008_resampled.tif'
# dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Byte)
# dst.SetGeoTransform( match_geotrans )
# dst.SetProjection( match_proj)
#
# # Do the work
# gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour)
#
# del dst # Flush


#### 2a. Reclassify forest raster to mask

# import gdal
# import numpy as np
#
# in_ras_path = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\europe_landcover_2015_RSE-GER_resampled.tif'
# out_ras_path = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\grassland_mask_2015.tif'
#
# in_ras = gdal.Open(in_ras_path)
#
# in_ras_gt = in_ras.GetGeoTransform()
# in_ras_pr = in_ras.GetProjection()
#
# in_arr = in_ras.ReadAsArray()
#
# # 0	unclassified
# # 1	artificial land
# # 2	cropland seasonal
# # 3	cropland perennial
# # 4	forest broadleaved
# # 5	forest coniferous
# # 6	forest mixed
# # 7	shrubland
# # 8	grassland
# # 9	bare land
# # 10	water
# # 11	wetland
# # 12	snow ice
#
# in_arr[(in_arr == 0)  ] = 0
# in_arr[(in_arr == 1)  ] = 0
# in_arr[(in_arr == 2)  ] = 0
# in_arr[(in_arr == 3)  ] = 0
# in_arr[(in_arr == 4)  ] = 0
# in_arr[(in_arr == 5)  ] = 0
# in_arr[(in_arr == 6)  ] = 0
# in_arr[(in_arr == 7)  ] = 0
# in_arr[(in_arr == 8)  ] = 1
# in_arr[(in_arr == 9)  ] = 0
# in_arr[(in_arr == 10)  ] = 0
# in_arr[(in_arr == 11)  ] = 0
# in_arr[(in_arr == 12)  ] = 0
#
# x_res = in_ras.RasterXSize
# y_res = in_ras.RasterYSize
#
# out_ras = gdal.GetDriverByName('GTiff').Create(out_ras_path, x_res, y_res, 1, gdal.GDT_Int16)
# out_ras.SetGeoTransform(in_ras_gt)
# out_ras.SetProjection(in_ras_pr)
#
# band = out_ras.GetRasterBand(1)
# NoData_value = -999
# band.SetNoDataValue(NoData_value)
# band.WriteArray(in_arr)
#
# del(out_ras)
# del(in_ras)


#### 2b. multiply forest raster with disturbance raster

# import gdal
# import numpy as np
#
# ras_dist = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\non-disturbed-forest-since-2013_resampled.tif')
# ras_for = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\forest_coniferous_mask_2015.tif')
#
# out_ras_path = r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\forest_coniferous_mask_2015_undist_since_2013.tif'
#
# in_ras_gt = ras_for.GetGeoTransform()
# in_ras_pr = ras_for.GetProjection()
#
# arr_dist = ras_dist.ReadAsArray()
# arr_for = ras_for.ReadAsArray()
#
# arr_out = arr_dist * arr_for
#
# x_res = ras_for.RasterXSize
# y_res = ras_for.RasterYSize
#
# out_ras = gdal.GetDriverByName('GTiff').Create(out_ras_path, x_res, y_res, 1, gdal.GDT_Byte)
# out_ras.SetGeoTransform(in_ras_gt)
# out_ras.SetProjection(in_ras_pr)
#
# band = out_ras.GetRasterBand(1)
# NoData_value = -999
# band.SetNoDataValue(NoData_value)
# band.WriteArray(arr_out)
#
# del(out_ras)
# del(ras_dist)
# del(ras_for)


# ### 3. cut raster to FORCE grid
#
# def createFolder(directory):
#     import os
#     try:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#     except OSError:
#         print ('Error: Creating directory. ' + directory)
#
#
# import gdal
# import ogr
#
# ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\forest_broadleaf_mask_2015_undist_since_2013.tif')
#
# shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp')
# lyr = shp.GetLayer()
#
# gt = ras.GetGeoTransform()
# pr = ras.GetProjection()
#
# arr = ras.ReadAsArray()
# i = 0
# for feat in lyr:
#     geom = feat.geometry().Clone()
#     name = feat.GetField('Name')
#
#     i += 1
#     print(i, name)
#
#     extent = geom.GetEnvelope()
#
#     x_min_ext = extent[0]
#     x_max_ext = extent[1]
#     y_min_ext = extent[2]
#     y_max_ext = extent[3]
#
#     # slice input raster array to common dimensions
#     px_min = int((x_min_ext - gt[0]) / gt[1])
#     px_max = int((x_max_ext - gt[0]) / gt[1])
#
#     py_max = int((y_min_ext - gt[3]) / gt[5])  # raster coordinates count from S to N, but array count from T to B, thus pymax = ymin
#     py_min = int((y_max_ext - gt[3]) / gt[5])
#
#     geom_arr = arr[py_min: py_max, px_min: px_max]
#
#     createFolder(r'Y:\germany-drought\masks\\' + name)
#
#     output_name = r'Y:\germany-drought\masks\\' + name + r'\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013.tif'
#
#     # write arr img to disc
#     output_ds = gdal.GetDriverByName('ENVI').Create(output_name, geom_arr.shape[1], geom_arr.shape[0], 1,
#                                                     gdal.GDT_Byte)
#
#     output_ds.SetGeoTransform((x_min_ext, gt[1], 0, y_max_ext, 0, gt[5]))
#     output_ds.SetProjection(ras.GetProjection())
#
#     band = output_ds.GetRasterBand(1)
#     band.WriteArray(geom_arr)
#     band.SetNoDataValue(-999)
#     band.FlushCache()
#     del(output_ds)
#
## 3b. cut raster to FORCE grid

print('cut raster to FORCE grid\n')

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def getCorners(path):
    ds = gdal.Open(path)
    gt = ds.GetGeoTransform()
    width = ds.RasterXSize
    height = ds.RasterYSize
    minx = gt[0]
    miny = gt[3] + width * gt[4] + height * gt[5]
    maxx = gt[0] + width * gt[1] + height * gt[2]
    maxy = gt[3]
    return [minx, miny, maxx, maxy]


import gdal
import ogr
import joblib

abr = 'ALL'

with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]

ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\forest_all_mask_2015.tif")
arr = ras.ReadAsArray()
i = 0

gt = ras.GetGeoTransform()
pr = ras.GetProjection()

for tile in tiles_lst:
# def workFunc(tile):

    print("Start: " + tile[0])

    print(tile)

    tile_pth = 'Y:/germany-drought/level4/' + tile + '/2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_DES-LSP_040.tif'
    print(tile_pth)
    i += 1

    extent = getCorners(tile_pth)

    x_min_ext = extent[0]
    x_max_ext = extent[2]
    y_min_ext = extent[1]
    y_max_ext = extent[3]

    # slice input raster array to common dimensions
    px_min = int((x_min_ext - gt[0]) / gt[1])
    px_max = int((x_max_ext - gt[0]) / gt[1])

    py_max = int((y_min_ext - gt[3]) / gt[5])  # raster coordinates count from S to N, but array count from T to B, thus pymax = ymin
    py_min = int((y_max_ext - gt[3]) / gt[5])

    geom_arr = arr[py_min: py_max, px_min: px_max]

    createFolder(r'O:\Student_Data\CJaenicke\JANOSCH\\' + tile)

    output_name = r'O:\Student_Data\CJaenicke\JANOSCH\\' + tile + r'\2015_MASK_FOREST.tif'

    # write arr img to disc
    output_ds = gdal.GetDriverByName('ENVI').Create(output_name, geom_arr.shape[1], geom_arr.shape[0], 1,
                                                    gdal.GDT_Byte)

    output_ds.SetGeoTransform((x_min_ext, gt[1], 0, y_max_ext, 0, gt[5]))
    output_ds.SetProjection(ras.GetProjection())

    band = output_ds.GetRasterBand(1)
    band.WriteArray(geom_arr)
    band.SetNoDataValue(-999)
    band.FlushCache()
    del(output_ds)

# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in tiles_lst)

# # #### 4. buffer mask
# ## !!!! There is a problem with convolve2d-function. Either, it doesn't work in O:  !!!!
# ## !!!! or it doesn't work with too big raster data  !!!!
#
# print('buffer mask\n')
#
# import gdal
# from scipy.signal import convolve2d
# import numpy as np
# import joblib
# import glob
#
# abr = 'CONIFER'
#
# with open(r'Y:\germany-drought\germany.txt') as file:
#     tiles_lst = file.readlines()
#
# tiles_lst = [item.strip() for item in tiles_lst]
# input_lst = [r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_FOREST-' + abr + '_UNDISTURBED-2013.tif' for item in tiles_lst]
# output_lst = [r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_FOREST-' + abr + '_UNDISTURBED-2013_BUFF-01.tif' for item in tiles_lst]
# # input_lst = [r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_GRASSLAND.tif' for item in tiles_lst]
# # output_lst = [r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_GRASSLAND_BUFF-01.tif' for item in tiles_lst]
#
# job_lst = [[input_lst[i], output_lst[i]] for i in range (len(input_lst))]
#
# ## Optional check job list
# # for i, job in enumerate(job_lst):
# #    print(i+1)
# #    print(job)
#
# def workFunc(job):
#     print("Start: " + job[0])
#
#     #ras_lst = glob.glob('Y:/germany-drought/level4/**/*' + abr + '*.tif')
#     ras = gdal.Open(job[0])
#     out_path_full = job[1]
#
#     arr = ras.ReadAsArray()
#     arr[arr == 1] = 2
#     arr[arr == 0] = 1
#     arr[arr == 2] = 0
#
#     kernel = np.ones((3,3))
#
# # !!!! There is a problem with convolve2d-function. Either, it doesn't work in O:  !!!!
# # !!!! or it doesn't work with too big raster data  !!!!
#     arr_buff = np.int64(convolve2d(arr, kernel, mode = 'same') > 0)
#
#     arr_buff[arr_buff == 1] = 2
#     arr_buff[arr_buff == 0] = 1
#     arr_buff[arr_buff == 2] = 0
#
#     num_bands = 1
#     gt = ras.GetGeoTransform()
#     pr = ras.GetProjection()
#     rows = ras.RasterYSize
#     cols = ras.RasterXSize
#
#     target_ds = gdal.GetDriverByName('GTiff').Create(out_path_full, cols, rows, num_bands, gdal.GDT_Byte)
#     target_ds.SetGeoTransform(gt)
#     target_ds.SetProjection(pr)
#
#     band = target_ds.GetRasterBand(1)
#     band.WriteArray(arr_buff)
#     band.SetNoDataValue(-999)
#     band.FlushCache()
#
#     del(target_ds)
#
#     print("Done: " + job[0])

# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in job_lst)