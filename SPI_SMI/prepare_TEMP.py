import gdal, gdalconst
import numpy as np
import glob
import joblib
import ogr

#### ------------------------------ FUNCTIONS ----------------------------- ####

def StackRasterFromList(rasterList, outputPath):
    """
    Stacks the first band of n raster that are stored in a list
    rasterList - list containing the rasters that have the same dimensions and Spatial References
    outputPath - Path including the name to which the stack is written
    """

    import gdal

    input_ras_gt = rasterList[0].GetGeoTransform()

    # set output raster definitions
    x_min = input_ras_gt[0]
    y_max = input_ras_gt[3]
    x_max = x_min + input_ras_gt[1] * rasterList[0].RasterXSize
    y_min = y_max + input_ras_gt[5] * rasterList[0].RasterYSize
    x_res = rasterList[0].RasterXSize
    y_res = rasterList[0].RasterYSize
    pixel_width_x = input_ras_gt[1]
    pixel_width_y = input_ras_gt[5]

    target_ds = gdal.GetDriverByName('GTiff').Create(outputPath, x_res, y_res, len(rasterList), gdal.GDT_Float32)
    target_ds.SetGeoTransform((x_min, pixel_width_x, 0, y_max, 0, pixel_width_y))
    target_ds.SetProjection(rasterList[0].GetProjection())

    for i in range(0, len(rasterList)):
        band = target_ds.GetRasterBand(i + 1)
        band.WriteArray(rasterList[i].GetRasterBand(1).ReadAsArray())
        NoData_value = -999
        band.SetNoDataValue(NoData_value)
        band.FlushCache()

    del(target_ds)

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

        band = out_ras.GetRasterBand( 1)
        band.WriteArray(in_array)
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        del (out_ras)

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

#### ------------------------------ Stack month of 2018 ----------------------------- ####
# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\download\\'
#
# pth_lst = []
#
# for year in range(2018,2019):
#     for month in range(1,13):
#         pth = wd + r'TAMM_{0:02d}_{1}_01.tif'.format(month, year)
#         pth_lst.append(pth)
#
# ras_list = [gdal.Open(file) for file in pth_lst]
#
# out_pth =r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018.tif'
#
# stack = StackRasterFromList(ras_list, out_pth)
#
# del(stack)

#### ------------------------------ Reproject to 3035 ----------------------------- ####
#
# in_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018.tif'
# out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018_3035.tif'
#
# repr = gdal.Warp(out_pth, in_pth, dstSRS='EPSG:3035')
# del repr
#### ------------------------------ Resample to FORCE resolution ----------------------------- ####
#
# print("Start Resampling")
# src_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018_3035.tif'
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
# dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018_3035_resampled.tif'
# dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, src_bands, gdalconst.GDT_Float32)
# dst.SetGeoTransform( match_geotrans )
# dst.SetProjection( match_proj)
#
# # Do the work
# gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour)
# print("Resampling Done")
# del(dst)

#### ------------------------------ Slice to FORCE grid v2 ----------------------------- ####

print("Start slicing to FORCE grid")

def workFunc(i):
    ras_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\times_series\TEMP_2018_3035_resampled.tif"
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

        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles\\' + name + r'\\'
        createFolder(output_path)
        output_name_full = output_path + 'TEMP_2018.tif'

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

        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles\\' + name + r'\\'
        createFolder(output_path)
        output_name_full = output_path + 'TEMP_2018.tif'

        # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]

        ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
        ras_cut = None

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in range(0,496))

# #### ------------------------------ Set NA and change gdal datatype ----------------------------- ####
print('Set NA and change datatype')

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

def workFunc(tile_name):
    print(tile_name)
    ras_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles\\' + tile_name + r'\TEMP_2018.tif'
    ras = gdal.Open(ras_pth)
    arr = ras.ReadAsArray()

    def searchNA(slice):
        if np.sum(slice) == 0:
            slice += -9999
        else:
            pass

    np.apply_along_axis(searchNA,0,arr)

    arr = arr.astype(int)
    out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles\\' + tile_name + r'\TEMP_2018_int.tif'
    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()
    writeRasterInt(arr, out_pth, gt, pr, -9999)
    print(tile_name, 'done')

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in tile_name_lst)

#### ------------------------------ Set NA and change gdal datatype ----------------------------- ####

import glob
import os

l = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles\**\*.xml')
print(len(l))
for i in l:
    os.remove(i)
