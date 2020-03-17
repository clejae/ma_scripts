import gdal
import numpy as np
import joblib
import time
from scipy.stats import norm

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("Start time " + str(starttime))

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

# #### -----------------------------------------------------------------------------------------------------------#### #

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
job_lst = [item.strip() for item in tiles_lst]
#job_lst = ['X0056_Y0053']

def workFunc(job):
    tile = job
    print('Start: ' + tile)

    curr_year = 2018
    bl = '2013-2018'

    ############################################
    #### 1. Derive monthly min and max values ####
    #### 2. Calculate VPI in parallel ####

    out_descr = str(curr_year) + '_BL-' + bl
    #out_descr = '{0}_BL-{1}'.format(curr_year, bl)
    ext = '_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_FBM.tif'

    ndvi_ras = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + str(curr_year) + '-' + str(curr_year) + ext)
    ndvi_arr = ndvi_ras.ReadAsArray()

    gt = ndvi_ras.GetGeoTransform()
    pr = ndvi_ras.GetProjection()

    arr_lst = []
    ## Open monthly-NDVI raster per year
    for year in range(2013, 2019):

        ras = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + str(year) + '-' + str(year) + ext)
        arr = ras.ReadAsArray()

        gt = ras.GetGeoTransform()
        pr = ras.GetProjection()

        arr_lst.append(arr)

    month_min_lst = []
    month_max_lst = []

    vpi_out_lst = []
    vci_out_lst = []
    #avg_lst = []
    #std_lst = []
    ## Derive statistics (min, max, avg, std) and calculate VPI
    for month in range(0, 12):
        #print('Month:', month)

        monthly_lst = []
        for arr in arr_lst:
            monthly_arr = arr[month, :, :]
            monthly_arr = monthly_arr + 0.0
            monthly_arr[monthly_arr == -32767] = np.nan
            monthly_lst.append(monthly_arr)
        monthly_stack = np.array(monthly_lst)

        # Derive statistics necessary for VPI and VCI calculation
        min_arr = np.nanmin(monthly_stack, axis=0) #VCI
        max_arr = np.nanmax(monthly_stack, axis=0) #VCI

        mean_ts = np.nanmean(monthly_stack, axis=0) #VPI
        std_ts = np.nanstd(monthly_stack, axis=0, ddof=1) #VPI

        # create NDVI-array of current month
        ndvi_slice = ndvi_arr[month, :, :]
        ndvi_slice = ndvi_slice + 0.0
        ndvi_slice[ndvi_slice == -32767] = np.nan

        # Calculate VPI
        vpi = norm.cdf(ndvi_slice, scale=std_ts, loc=mean_ts)
        vpi_out_lst.append(vpi)

        # Calculate VPI
        nan_merge = np.ones(ndvi_slice.shape)
        nan_merge[np.isnan(ndvi_slice)] = -32767
        nan_merge[np.isnan(min_arr)] = -32767
        nan_merge[np.isnan(max_arr)] = -32767
        
        vci_arr = 100 * (ndvi_slice - min_arr) / (max_arr - min_arr)
        vci_arr[nan_merge == -32767] = -32767
        vci_arr[np.isinf(vci_arr)] = -32767

        vci_out_lst.append(vci_arr)
        
        month_min_lst.append(min_arr)
        month_max_lst.append(max_arr)
        # avg_lst.append(mean_ts)
        # std_lst.append(std_ts)

    min_arr = np.array(month_min_lst)
    max_arr = np.array(month_max_lst)
    # avg_out = np.array(avg_lst)
    # std_out = np.array(std_lst)
    
    vpi_out_arr = np.array(vpi_out_lst)
    vpi_out_arr = 100 * vpi_out_arr
    vci_out_arr = np.array(vci_out_lst)

    # write VCI array to disc
    out_pth_vci = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + out_descr + '_VCI.tif'
    writeRasterInt(vci_out_arr, out_pth_vci, gt, pr, -32767)

    ## Write VPI array to disc
    out_pth_vpi = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + out_descr + '_VPI.tif'
    writeRasterInt(vpi_out_arr, out_pth_vpi, gt, pr, -32767)

    ## Optional: Writing statistic arrays to disc
    # out_pth_min = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_MIN.tif'
    # writeRasterInt(min_arr, out_pth_min, gt, pr, -32767)
    # out_pth_max = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_MAX.tif'
    # writeRasterInt(max_arr, out_pth_max, gt, pr, -32767)
    # out_pth_std = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_STD.tif'
    # writeRasterFloat(out_pth_std, out_pth, gt, pr, -32767)
    # out_pth_avg = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + bl + '_NDVI_AVG.tif'
    # writeRasterFloat(out_pth_avg, out_pth, gt, pr, -32767)

    print('Done: ' + tile)

if __name__ == '__main__':
    joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in job_lst)

endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

print("Start time " + str(starttime))
print("End time " + str(endtime))