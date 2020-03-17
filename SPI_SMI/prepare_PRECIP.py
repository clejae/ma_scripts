from osgeo import gdal, gdalconst
import ogr
import gdal
import pandas as pd
import numpy as np
import time
import joblib

#### ------------------------------ FUNCTIONS ----------------------------- ####

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

def writeRaster(in_array, out_path, gt, pr, no_data_value):

    import gdal
    from osgeo import gdal_array

    type_code = gdal_array.NumericTypeCodeToGDALTypeCode(in_array.dtype)

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, type_code)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        for b in range(0, nbands_out):
            band = out_ras.GetRasterBand(b + 1)
            arr_out = in_array[b, :, :]
            band.WriteArray(arr_out)
            band.SetNoDataValue(no_data_value)
            band.FlushCache()

        del (out_ras)

    if len(in_array.shape) == 2:
        nbands_out = 1
        x_res = in_array.shape[1]
        y_res = in_array.shape[0]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        band = out_ras.GetRasterBand( 1)
        band.WriteArray(in_array)
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        del (out_ras)

def writeRasterInt(in_array, out_path, gt, pr, no_data_value):

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Int16)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        for b in range(0, nbands_out):
            band = out_ras.GetRasterBand(b + 1)
            arr_out = in_array[b, :, :]
            band.WriteArray(arr_out)
            band.SetNoDataValue(no_data_value)
            band.FlushCache()

        del (out_ras)

    if len(in_array.shape) == 2:
        nbands_out = 1
        x_res = in_array.shape[1]
        y_res = in_array.shape[0]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Int16)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        band = out_ras.GetRasterBand(1)
        band.WriteArray(in_array)
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        del (out_ras)


#### ------------------------------ Resample to FORCE resolution ----------------------------- ####


# ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_1970-2018_3035.tif")
# arr = ras.ReadAsArray()[-12:,:,:]
#
# pth_sub = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_2018-2018_3035.tif'
# gt = ras.GetGeoTransform()
# pr = ras.GetProjection()
# writeRaster(arr, pth_sub, gt, pr, -999)
#
# print("Start Resampling")
# src_filename = pth_sub
# src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
# src_proj = src.GetProjection()
# src_geotrans = src.GetGeoTransform()
# src_bands = src.RasterCount
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
# dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_2018-2018_3035_resampled.tif'
# dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, src_bands, gdalconst.GDT_Float32)
# dst.SetGeoTransform( match_geotrans )
# dst.SetProjection( match_proj)
#
# # Do the work
# gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour)
# print("Resampling Done")
# del(dst)

#### ------------------------------ Slice to FORCE grid v1 ----------------------------- ####
# print("Start slicing to FORCE grid")
#
# with open(r'Y:\germany-drought\germany.txt') as file:
#     tile_name_lst = file.readlines()
# tile_name_lst = [item.strip() for item in tile_name_lst]
#
# def workFunc(tile_name):
#     print(tile_name)
#     dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_2018-2018_3035_resampled.tif'
#     ras = gdal.Open(dst_filename)
#
#     msk_bl_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'
#
#     corners = getCorners(msk_bl_pth)
#
#     x_min_ext = corners[0]
#     x_max_ext = corners[2]
#     y_min_ext = corners[1]
#     y_max_ext = corners[3]
#
#     output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\\' + tile_name + r'\\'
#     createFolder(output_path)
#     output_name_full = output_path + 'PRECIP_2018.tif'
#
#     ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
#     ras_cut = None
#     print(tile_name, 'done')
#
# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in tile_name_lst)

#### ------------------------------ Slice to FORCE grid v2 ----------------------------- ####

print("Start slicing to FORCE grid")

def workFunc(i):
    ras_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_2018-2018_3035_resampled.tif'
    ras = gdal.Open(ras_pth)
    shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp')
    lyr = shp.GetLayer()
    feat = lyr.GetFeature(i)

    geom = feat.geometry().Clone()
    name = feat.GetField('Name')


    if int(name[3:5]) > 57:
        print(i, name)
        extent = geom.GetEnvelope()

        x_min_ext = extent[0] + 30
        x_max_ext = extent[1] + 30
        y_min_ext = extent[2]
        y_max_ext = extent[3]

        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\\' + name + r'\\'
        createFolder(output_path)
        output_name_full = output_path + 'PRECIP_2018_v3.tif'

        # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]

        ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
        ras_cut = None
    else:
        print(i, name)
        extent = geom.GetEnvelope()

        x_min_ext = extent[0]
        x_max_ext = extent[1]
        y_min_ext = extent[2]
        y_max_ext = extent[3]

        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\\' + name + r'\\'
        createFolder(output_path)
        output_name_full = output_path + 'PRECIP_2018_v3.tif'

        # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]

        ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
        ras_cut = None

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in range(0,496))


#### ------------------------------ Set NA and change gdal datatype ----------------------------- ####
print('Set NA and change datatype')

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

def workFunc(tile_name):
    print(tile_name)
    ras_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\\' + tile_name + r'\PRECIP_2018_v3.tif'
    ras = gdal.Open(ras_pth)
    arr = ras.ReadAsArray()

    def searchNA(slice):
        if np.sum(slice) == 0:
            slice += -9999
        else:
            pass

    np.apply_along_axis(searchNA,0,arr)

    arr = arr.astype(int)
    out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\\' + tile_name + r'\PRECIP_2018_v3_int.tif'
    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()
    writeRasterInt(arr, out_pth, gt, pr, -9999)
    print(tile_name, 'done')

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in tile_name_lst)

#### ------------------------------ Set NA and change gdal datatype ----------------------------- ####

import glob
import os

l = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles\**\PRECIP_2018_v3.tif')
for i in l:
    os.remove(i)