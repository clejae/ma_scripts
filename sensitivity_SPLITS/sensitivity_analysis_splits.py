import gdal
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import math
import pandas as pd

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


with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

num_seg_lst = [os.path.basename(x) for x in glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')]
num_seg_lst.sort()
num_seg_lst = num_seg_lst[:-3]

abr_lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM']
#abr_lst = ['DSS']


abr = abr_lst[0]
for abr in abr_lst:
    print(abr)

    # create main figure with a grid of 4x5
    fig, axs = plt.subplots(5, 4, sharey=True, figsize=(20, 20))

    # create output dataframe for aggregate of all tiles
    out_df = pd.DataFrame(index=['4-SEG', '6-SEG', '8-SEG', '10-SEG', '12-SEG'], columns=['20-SCENES', '40-SCENES', '60-SCENES', 'ALL-SCENES'])
    var_df = pd.DataFrame(columns=['metric','num_scenes','num_seg','variance'])

    # create list of output dataframes for each tile
    out_df_lst = [pd.DataFrame(index=['4-SEG', '6-SEG', '8-SEG', '10-SEG', '12-SEG'], columns=['20-SCENES', '40-SCENES', '60-SCENES', 'ALL-SCENES']) for i in range(len(tiles_lst))]

    num_seg_folder = num_seg_lst[0]

    for num, num_seg_folder in enumerate(num_seg_lst):
        print(num_seg_folder)

        # create lists with paths
        input_pth_lst = [r'Y:\germany-drought\level4_sensitivity\metrics\\' + num_seg_folder + r'\\' + item + r'\\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.tif' for item in tiles_lst]
        mask_pth_lst = [r'Y:\germany-drought\masks\\' + item + r'\\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif' for item in tiles_lst]

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
            pymin = int((ymax_com - ras_gt_lst[i][3]) / ras_gt_lst[i][5])  # raster coordinates count from S to N, but array count from T to B, thus pymin = ymax
            pxmax = int((xmax_com - ras_gt_lst[i][0]) / ras_gt_lst[i][1])
            pymax = int((ymin_com - ras_gt_lst[i][3]) / ras_gt_lst[i][5])

            p_lst = [pymin, pymax, pxmin, pxmax]
            ras_index_lst.append(p_lst)

            pxmin = int((xmin_com - mask_gt_lst[i][0]) / mask_gt_lst[i][1])
            pymin = int((ymax_com - mask_gt_lst[i][3]) / mask_gt_lst[i][5])  # raster coordinates count from S to N, but array count from T to B, thus pymin = ymax
            pxmax = int((xmax_com - mask_gt_lst[i][0]) / mask_gt_lst[i][1])
            pymax = int((ymin_com - mask_gt_lst[i][3]) / mask_gt_lst[i][5])

            p_lst = [pymin, pymax, pxmin, pxmax]
            mask_index_lst.append(p_lst)

        # read arrays of the tiles and the masks with help of indices
        arr_lst = [ras_lst[i].ReadAsArray()[ras_index_lst[i][0]:ras_index_lst[i][1],ras_index_lst[i][0]:ras_index_lst[i][1]] for i in range(len(ras_lst))]
        mask_arr_lst = [mask_lst[i].ReadAsArray()[mask_index_lst[i][0]:mask_index_lst[i][1], mask_index_lst[i][0]:mask_index_lst[i][1]]for i in range(len(mask_lst))]

        # mask out all non-broadleaf trees
        for i in range(len(arr_lst)):
            arr_lst[i][mask_arr_lst[i] == 0] = -32767 # no data value FORCE -32767


        # concatenate the masked tiles and set NaN
        conc_arr = np.concatenate(arr_lst, axis = 0)
        conc_arr = conc_arr + 0.0 # small trick to convert data type of array to float, normal way didn't work somehow
        conc_arr[conc_arr == -32767.0] = np.nan
        #conc_arr[conc_arr < 0.0] = np.nan

        # flatten (make 1-dimensional) to exclude all NaN cells afterwards
        conc_arr_f = np.ndarray.flatten(conc_arr)
        conc_arr_f = conc_arr_f[np.logical_not(np.isnan(conc_arr_f))]


        # calculate some statistics
        mean_st = np.mean(conc_arr_f)
        min_st = np.min(conc_arr_f)
        max_st = np.max(conc_arr_f)
        std_st = np.std(conc_arr_f)

        var_st = np.var(conc_arr_f)

        # derive x and y indices from the current index of the 2nd main loop
        # which loops over folders
        # so from counting from 0 to 19 get 4 times the counting from 0 to 4
        x_ind = num // 5
        factor = math.floor(num / 5)
        y_ind = num - factor * 5

        # fill output dataframe with statistics
        out_df.iloc[y_ind, x_ind] = mean_st

        # fill main figure

        axs[y_ind,x_ind].hist(conc_arr_f, bins = 30)
        axs[y_ind,0].set_ylabel(num_seg_folder[7:], fontsize=24)
        axs[0,x_ind].set_title(num_seg_folder[:7], fontsize=24)

        for i, arr in enumerate(arr_lst):
            arr = arr + 0.0
            arr[arr == -32767.0] = np.nan
            # conc_arr[conc_arr < 0.0] = np.nan

            arr_f = np.ndarray.flatten(arr)
            arr_f = arr_f[np.logical_not(np.isnan(arr_f))]

            tile = tiles_lst[i]

            # axs[num,i].hist(arr_f, bins = 30)
            # axs[num,i].set_title(tile)
            # axs[num, i].set_ylabel(num_seg_folder)
            # #plt.title()

            mean_sub = np.mean(arr_f)
            min_sub = np.min(arr_f)
            max_sub = np.max(arr_f)
            std_sub = np.std(arr_f)

            out_df_lst[i].iloc[y_ind, x_ind] = mean_sub


    fig.suptitle('sensitivity_tiles-aggregated' + abr, fontsize=30)
    plt.savefig(r'Y:\germany-drought\level4_sensitivity\plots\histogramm_sensitivity_tiles-aggregated_' + abr + '.png')
    plt.close()

    fig2, ax2 = plt.subplots(figsize=(10, 10))
    for column in out_df:
        ax2.plot(out_df.index.values, out_df[column], marker ='o', label=column)

    legend = ax2.legend( shadow=True, title = 'Input Tiles', fontsize=18)
    ax2.set_ylabel('Mean of ' + abr)
    plt.savefig(r'Y:\germany-drought\level4_sensitivity\plots\line_sensitivity_tiles-aggregated_' + abr + '.png')
    #plt.show()
    plt.close()

    loop_lst = list(out_df.columns.values)

    fig3, axs = plt.subplots(1, len(loop_lst), sharey=True, figsize=(40, 10))
    for j, col_name in enumerate(loop_lst):
        #fig3, ax3 = plt.subplots(figsize=(10, 10))

        for i, df in enumerate(out_df_lst):
            tile_name = tiles_lst[i]
            axs[j].plot(df.index.values, df[col_name], marker='o',  linestyle='dashed',label=tile_name)
            plt.xticks(rotation='vertical')
            #axs.title(tile_name)
        axs[j].plot(out_df.index.values, out_df[col_name], marker='o',label='MEAN', linewidth = 2, color= 'black')
        axs[j].title.set_text(col_name)
        #axs[j].title.text(col_name, fontsize=18)
        plt.xticks(rotation='vertical')

        #plt.ylim(-30, 100)
        #plt.title(col_name)
    legend = axs[len(loop_lst)-1].legend(shadow=True, fontsize=18)

    axs[0].set_ylabel('Mean of ' + abr, fontsize=18)
    plt.savefig(r'Y:\germany-drought\level4_sensitivity\plots\line_sensitivity_' + col_name + '_' + abr + '.png')
    #plt.show()
    plt.close()

