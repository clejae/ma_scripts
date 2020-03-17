import gdal
import numpy as np

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



year = 2018
bl =  '2013-2017'

out_descr = str(year) + '_BL-' + bl + '_VCI'
ext = '_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_FBM.tif'

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]
tiles_lst = [tiles_lst[0]]

for tile in tiles_lst:
    print('\n' + tile + '\n')
    ndvi_ras = gdal.Open(r'Y:\germany-drought\VCI\\' + tile + r'\\' + str(year) + '-' + str(year) + ext)
    min_ras = gdal.Open(r'Y:\germany-drought\VCI\\' + tile + r'\\'+ bl +'_NDVI_MIN.tif')
    max_ras = gdal.Open(r'Y:\germany-drought\VCI\\' + tile + r'\\'+ bl +'_NDVI_MAX.tif')

    gt = ndvi_ras.GetGeoTransform()
    pr = ndvi_ras.GetProjection()

    ndvi_arr = ndvi_ras.ReadAsArray()
    min_arr = min_ras.ReadAsArray()
    max_arr = max_ras.ReadAsArray()

    vci_out_lst = []
    print('Derive VCI per month')
    for month in range(12):
        curr_ndvi = ndvi_arr[month, :, :]
        curr_min = min_arr[month, :, :]
        curr_max = max_arr[month, :, :]

        curr_ndvi = curr_ndvi + 0.0
        curr_min = curr_min + 0.0
        curr_max= curr_max + 0.0

        nan_merge = np.ones(curr_ndvi.shape)
        nan_merge[curr_ndvi == -32767] = -32767
        nan_merge[curr_min == -32767] = -32767
        nan_merge[curr_max == -32767] = -32767

        curr_ndvi[curr_ndvi == -32767] = np.nan
        curr_min[curr_min == -32767] = np.nan
        curr_max[curr_max == -32767] = np.nan

        vci_arr = 100 * (curr_ndvi - curr_min) / (curr_max - curr_min)
        vci_arr[nan_merge == -32767] = -32767

        vci_out_lst.append(vci_arr)

    vci_out_arr = np.array(vci_out_lst)

    print('Writing raster to disc.')
    out_pth = r'Y:\germany-drought\VCI\\' + tile + r'\\' + out_descr + '.tif'
    writeRasterInt(vci_out_arr, out_pth, gt, pr, -32767)
