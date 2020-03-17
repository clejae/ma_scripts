import gdal
import numpy as np
import joblib
import os

def writeArrayToRaster(in_array, out_path, gt, pr, no_data_value):

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

wd =  r'Y:\germany-drought\level4'

with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]

def workFunc(tile):
# for tile in tiles_lst:
    print("Start: " + tile)

    abr_lst = ['DES-LSP_040', 'RAF-LSP']

    for abr in abr_lst:
        file_name_2016 = r'{0}\{1}\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_{2}.tif'.format(wd,tile,abr)
        file_name_2017 = r'{0}\{1}\2016-2018_001-365_LEVEL4_TSA_LNDLG_NDV_{2}.tif'.format(wd,tile,abr)
        file_name_2018 = r'{0}\{1}\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_{2}.tif'.format(wd,tile,abr)

        ras16 = gdal.Open(file_name_2016)
        ras17 = gdal.Open(file_name_2017)
        ras18 = gdal.Open(file_name_2018)

        gt = ras18.GetGeoTransform()
        pr = ras18.GetProjection()

        arr16 = ras16.ReadAsArray()
        arr17 = ras17.ReadAsArray()
        arr18 = ras18.ReadAsArray()

        arr16 = arr16 + 0.0
        arr17 = arr17 + 0.0
        arr18 = arr18 + 0.0

        arr16[arr16 < 0] = np.nan
        arr16[arr16 > 365] = np.nan

        arr17[arr17 < 0] = np.nan
        arr17[arr17 > 365] = np.nan

        arr18[arr18 < 0] = np.nan
        arr18[arr18 > 365] = np.nan

        ref_arr = (arr16 + arr17) / 2
        comp_arr = arr18 - ref_arr

        comp_arr[np.isnan(arr16)] = np.nan
        comp_arr[np.isnan(arr17)] = np.nan
        comp_arr[np.isnan(arr18)] = np.nan

        out_pth =  r'{0}\{1}\COMP-2018_TO_MEAN16_17-{2}-LSP.tif'.format(wd,tile,abr)

        writeArrayToRaster(comp_arr,out_pth,gt,pr,-32767)

    print("Done: " + tile)

if __name__ == '__main__':
    joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in tiles_lst)