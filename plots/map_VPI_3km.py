import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

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

def makeColormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    import matplotlib.colors as mcolors

    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
tiles_df = gpd.read_file(tiles_pth)

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]
#tile_name_lst = ['X0061_Y0045','X0067_Y0046','X0056_Y0053','X0061_Y0058']

abr = 'VPI'
year = '2018'
tree = 'BROADLEAF'
endy = '9'

print(abr + '\n')
out_df = pd.DataFrame(index=tile_name_lst, columns=range(1,13))
#out_df_share = pd.DataFrame(index=tile_name_lst, columns=range(1,13))
tile_name = 'X0061_Y0045'
for tile_name in tile_name_lst:
    print(tile_name)

    ras_pth = r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\\' + year + '_BL-2013-201' + endy + '_' + abr + '.tif'
    msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-'+ tree + '_UNDISTURBED-2013_BUFF-01.tif'
    # msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_GRASSLAND.tif'

    ras = gdal.Open(ras_pth)
    msk_ras = gdal.Open(msk_pth)

    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()

    arr = ras.ReadAsArray()
    msk_arr = msk_ras.ReadAsArray()
    month = 0

    month_lst = []

    for month in range(12):
        arr_sub = arr[month,:,:]

        arr_sub[msk_arr == 0] = -32767  # no data value FORCE -32767
        arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_sub[arr_sub == -32767.0] = np.nan
        aggr_lst = []
        for i in range(100):
            sub_lst = []
            for j in range(100):
                x1 = i * 10
                x2 = x1 + 10
                y1 = j * 10
                y2 = y1 + 10

                #print('Y:', y1, y2 ,'\n', 'X:', x1, x2)

                arr_slc = arr_sub[y1:y2,x1:x2]
                mean_slc = np.nanmean(arr_slc)
                sub_lst.append(mean_slc)
            aggr_lst.append(sub_lst)
        aggr_arr = np.array(aggr_lst)
        month_lst.append(aggr_arr)

    gt_new = (gt[0], 300, 0, gt[3], -300, 0)

    year_arr = np.array(month_lst)
    year_arr[np.isnan(year_arr)] = -999

    out_pth = r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\\' + year + '_BL-2013-201' + endy + '_' + abr + '_300m.tif'
    writeRasterFloat(year_arr, out_pth, gt_new, pr, -999)
