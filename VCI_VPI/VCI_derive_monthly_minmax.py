import gdal
import numpy as np

def writeRaster(in_array, out_path, gt, pr, no_data_value):

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


out_descr = '2013-2017_NDVI'

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]
tiles_lst = [tiles_lst[0]]

ext = '_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_FBM.tif'

for tile in tiles_lst:
    print('\n' + tile + '\n')
    ras_lst = []
    arr_lst = []
    print('Open yearly rasters')
    for year in range(2013,2018):
        print('Year:', year)
        ras = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + str(year) + '-' + str(year) + ext)
        arr = ras.ReadAsArray()

        gt = ras.GetGeoTransform()
        pr = ras.GetProjection()

        #ras_lst.append(ras)
        arr_lst.append(arr)

    month_min_lst = []
    month_max_lst = []
    print('Derive minimum and maximum values per month')
    for month in range(0,12):
        print('Month:', month)

        monthly_lst = []
        for arr in arr_lst:
            monthly_arr = arr[month,:,:]
            monthly_arr = monthly_arr + 0.0
            monthly_arr[monthly_arr == -32767] = np.nan
            monthly_lst.append(monthly_arr)
        monthly_stack = np.array(monthly_lst)
        min_arr = np.nanmin(monthly_stack, axis= 0)
        max_arr = np.nanmax(monthly_stack, axis= 0)
        month_min_lst.append(min_arr)
        month_max_lst.append(max_arr)

    out_min_arr = np.array(month_min_lst)
    out_max_arr = np.array(month_max_lst)

    print('Writing raster to disc.')
    out_pth_min = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + out_descr + '_MIN.tif'
    writeRaster(out_min_arr,out_pth_min, gt, pr, -32767)
    out_pth_max = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\\' + out_descr + '_MAX.tif'
    writeRaster(out_max_arr,out_pth_max, gt, pr, -32767)

print('Done!')




# derive max and min ndvi

