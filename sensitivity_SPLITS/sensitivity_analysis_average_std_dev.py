import gdal
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def findBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

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

with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

num_seg_lst = [os.path.basename(x) for x in glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')]
num_seg_lst.sort()
num_seg_lst = num_seg_lst[:-3]

abr_lst = []
abr_lst = ['DEM', 'DSS', 'DRI', 'DPS', 'DFI', 'DES', 'DLM','LTS', 'LGS', 'VEM', 'VSS', 'VRI', 'VPS', 'VFI', 'VES', 'VLM', 'VBL', 'VSA', 'IST', 'IBL', 'IBT', 'IGS',
           'RAR', 'RAF', 'RMR', 'RMF']

out_lst = []

abr = abr_lst[0]
for abr in abr_lst:
    print(abr)

    # create main figure with a grid of 4x5
    #fig, axs = plt.subplots(5, 4, sharey=True, figsize=(20, 20))

    # # create output dataframe for aggregate of all tiles
    # out_df = pd.DataFrame(index=['4-SEG', '6-SEG', '8-SEG', '10-SEG', '12-SEG'],
    #                       columns=['20-SCENES', '40-SCENES', '60-SCENES', 'ALL-SCENES'])
    #
    # # create list of output dataframes for each tile
    # out_df_lst = [pd.DataFrame(index=['4-SEG', '6-SEG', '8-SEG', '10-SEG', '12-SEG'],
    #                            columns=['20-SCENES', '40-SCENES', '60-SCENES', 'ALL-SCENES']) for i in
    #               range(len(tiles_lst))]

    num_seg_folder = num_seg_lst[0]

    for num, num_seg_folder in enumerate(num_seg_lst):
        print(num_seg_folder)

        # create lists with paths
        input_pth_lst = [
            r'Y:\germany-drought\level4_sensitivity\metrics\\' + num_seg_folder + r'\\' + item + r'\\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.tif'
            for item in tiles_lst]
        mask_pth_lst = [
            r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif' for item
            in tiles_lst]

        # open rasters of tiles and masks and cso
        ras_lst = [gdal.Open(input_pth) for input_pth in input_pth_lst]
        mask_lst = [gdal.Open(mask_pth) for mask_pth in mask_pth_lst]

        # get geo transform of input rasters and masks
        ras_gt_lst = [ras.GetGeoTransform() for ras in ras_lst]
        mask_gt_lst = [mask.GetGeoTransform() for mask in mask_lst]

        # for each tile-mask pair derive the common extent
        ras_ext_lst = [getCorners(input_pth) for input_pth in input_pth_lst]
        mask_ext_lst = [getCorners(mask_pth) for mask_pth in mask_pth_lst]

        common_ext_lst = []
        for i in range(len(ras_ext_lst)):
            ext_lst = []
            ext_lst.append(max(ras_ext_lst[i][0], mask_ext_lst[i][0]))  # x_min
            ext_lst.append(max(ras_ext_lst[i][1], mask_ext_lst[i][1]))  # y_min
            ext_lst.append(min(ras_ext_lst[i][2], mask_ext_lst[i][2]))  # x_max
            ext_lst.append(min(ras_ext_lst[i][3], mask_ext_lst[i][3]))  # y_max
            common_ext_lst.append(ext_lst)

        ras_index_lst = []
        mask_index_lst = []
        # a cso_index_lst as I assume that they correspond perfectly with the normal tiles

        for i, lst in enumerate(common_ext_lst):
            xmin_com = lst[0]
            ymax_com = lst[3]
            xmax_com = lst[2]
            ymin_com = lst[1]

            pxmin = int((xmin_com - ras_gt_lst[i][0]) / ras_gt_lst[i][1])
            pymin = int((ymax_com - ras_gt_lst[i][3]) / ras_gt_lst[i][
                5])  # raster coordinates count from S to N, but array count from T to B, thus pymin = ymax
            pxmax = int((xmax_com - ras_gt_lst[i][0]) / ras_gt_lst[i][1])
            pymax = int((ymin_com - ras_gt_lst[i][3]) / ras_gt_lst[i][5])

            p_lst = [pymin, pymax, pxmin, pxmax]
            ras_index_lst.append(p_lst)

            pxmin = int((xmin_com - mask_gt_lst[i][0]) / mask_gt_lst[i][1])
            pymin = int((ymax_com - mask_gt_lst[i][3]) / mask_gt_lst[i][
                5])  # raster coordinates count from S to N, but array count from T to B, thus pymin = ymax
            pxmax = int((xmax_com - mask_gt_lst[i][0]) / mask_gt_lst[i][1])
            pymax = int((ymin_com - mask_gt_lst[i][3]) / mask_gt_lst[i][5])

            p_lst = [pymin, pymax, pxmin, pxmax]
            mask_index_lst.append(p_lst)

        # read arrays of the tiles and the masks with help of indices
        arr_lst = [
            ras_lst[i].ReadAsArray()[ras_index_lst[i][0]:ras_index_lst[i][1], ras_index_lst[i][0]:ras_index_lst[i][1]]
            for i in range(len(ras_lst))]
        mask_arr_lst = [mask_lst[i].ReadAsArray()[mask_index_lst[i][0]:mask_index_lst[i][1],
                        mask_index_lst[i][0]:mask_index_lst[i][1]] for i in range(len(mask_lst))]

        # mask out all non-broadleaf trees
        for i in range(len(arr_lst)):
            arr_lst[i][mask_arr_lst[i] == 0] = -32767  # no data value FORCE -32767

        # concatenate the masked tiles and set NaN
        conc_arr = np.concatenate(arr_lst, axis=0)
        conc_arr = conc_arr + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        conc_arr[conc_arr == -32767.0] = np.nan
        # conc_arr[conc_arr < 0.0] = np.nan

        # flatten (make 1-dimensional) to exclude all NaN cells afterwards
        conc_arr_f = np.ndarray.flatten(conc_arr)
        conc_arr_f = conc_arr_f[np.logical_not(np.isnan(conc_arr_f))]

        # calculate some statistics
        # mean_st = np.mean(conc_arr_f)
        # min_st = np.min(conc_arr_f)
        # max_st = np.max(conc_arr_f)
        std_st = np.std(conc_arr_f)
        #conc_arr_t = np.transpose(conc_arr_f)
        #var_st = np.var(conc_arr_f, ddof=1)

        num_scenes = num_seg_folder[:7]
        num_scenes = num_scenes.replace("_OBS","")
        num_scenes = num_scenes.replace("-", "")
       #re.sub(r'[A-Z]+', '', num_scenes, re.I)

        num_seg = findBetween(num_seg_folder,'-','_')
        #re.sub(r'[a-z]+', '', num_seg, re.I)
        app_lst = [abr,num_scenes,num_seg,std_st]

        out_lst.append(app_lst)


var_df = pd.DataFrame(out_lst, columns=['metric', 'num_scenes', 'num_seg', 'std_dev'])

var_df.to_csv(r'Y:\germany-drought\level4_sensitivity\std_dev_all_metrics.csv', index=False)
# scaler = MinMaxScaler()
# scaled_values = scaler.fit_transform(df['std_dev'])
# df.loc[:,:] = scaled_values

print('done')

#'metric', 'num_scenes', 'num_seg', 'variance'