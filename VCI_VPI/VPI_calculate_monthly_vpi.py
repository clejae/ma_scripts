import gdal
import numpy as np
from scipy.stats import norm

def writeRasterFloat(in_array, out_path, gt, pr, no_data_value):

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
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

year = 2018
bl =  '2000-2017'

out_descr = str(year) + '_BL-' + bl + '_VPI'
ext = '_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_FBM.tif'

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]
tiles_lst = [tiles_lst[0]]

for tile in tiles_lst:
    print('\n' + tile + '\n')
    ndvi_ras = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + str(year) + '-' + str(year) + ext)
    ndvi_arr = ndvi_ras.ReadAsArray()

    arr_lst = []
    print('Open yearly rasters')
    for year in range(2000,2018):
        print('Year:', year)
        ras = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + str(year) + '-' + str(year) + ext)
        arr = ras.ReadAsArray()

        gt = ras.GetGeoTransform()
        pr = ras.GetProjection()

        arr_lst.append(arr)

    vpi_lst = []
    avg_lst = []
    std_lst = []

    print('Derive mean and stdev values per month')
    for month in range(0,12):

        print('Month:', month + 1)

        monthly_lst = []

        for arr in arr_lst:
            monthly_arr = arr[month,:,:]
            monthly_arr = monthly_arr + 0.0
            monthly_arr[monthly_arr == -32767] = np.nan
            monthly_lst.append(monthly_arr)
        monthly_stack = np.array(monthly_lst)

        mean_ts = np.nanmean(monthly_stack, axis = 0)
        std_ts = np.nanstd(monthly_stack, axis = 0, ddof = 1)

        avg_lst.append(mean_ts)
        std_lst.append(std_ts)

        ndvi_slice = ndvi_arr[month,:,:]
        ndvi_slice = ndvi_slice + 0.0
        ndvi_slice[ndvi_slice == -32767] = np.nan

        vpi = norm.cdf(ndvi_slice, scale = std_ts, loc = mean_ts)
        vpi_lst.append(vpi)

    vpi_out = np.array(vpi_lst)
    avg_out = np.array(avg_lst)
    std_out = np.array(std_lst)

    out_pth = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + out_descr + '.tif'
    writeRasterFloat(vpi_out, out_pth, gt, pr, -32767)

    out_pth = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_AVG.tif'
    writeRasterFloat(avg_out, out_pth, gt, pr, -32767)

    out_pth = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_STD.tif'
    writeRasterFloat(std_out, out_pth, gt, pr, -32767)