import gdal
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import random
from numpy.random import seed
from numpy.random import rand

def findBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

num_seg_lst = [os.path.basename(x) for x in glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')]
num_seg_lst.sort()
num_seg_lst = num_seg_lst[:-3]

abr_lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM']
#'LTS', 'LGS', , 'IST', 'IBL', 'IBT', 'IGS','RAR', 'RAF', 'RMR', 'RMF'
abr_lst = ['VEM', 'VSS', 'VRI', 'VPS', 'VFI', 'VES', 'VLM', 'VBL', 'VSA']

abr = abr_lst[0]

for abr in abr_lst:
    print('\n' + abr)

    seg_lst = ['04','06','08','10','12']
    scn_lst = ['20','40','60','ALL']


    fig, axs = plt.subplots( len(seg_lst), len(scn_lst),  sharex=True, figsize=(20, 20))
    fig2, axs2 = plt.subplots(len(seg_lst), len(scn_lst), sharex=True, figsize=(20, 20))
    num = 0
    x = 0

    for seg in seg_lst:

        val_lst = []
        obs_lst = []
        col_lst = []
        y = 0

        for num_scn in scn_lst:


            seed(1)
            num_seg_folder = num_scn + '_OBS-' + seg + '_LSP_SEG'
            print(num_seg_folder)

            # create lists with paths
            input_pth_lst = [r'Y:\germany-drought\level4_sensitivity\metrics\\' + num_seg_folder + r'\\' + item + r'\\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.tif' for item in tiles_lst]
            mask_pth_lst = [r'Y:\germany-drought\masks\\'  + item + r'\\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif' for item in tiles_lst]
            cso_pth_lst = [r'Y:\germany-drought\cso\\' + num_scn + r'\\' + item + r'\\2018-2018_12M_CSO-STATS_LNDLG_NUM.tif' for item in tiles_lst]

            # open rasters of tiles and masks and cso
            ras_lst = [gdal.Open(input_pth) for input_pth in input_pth_lst]
            mask_lst = [gdal.Open(mask_pth) for mask_pth in mask_pth_lst]
            cso_lst = [gdal.Open(cso_pth) for cso_pth in cso_pth_lst]

            # read arrays of the tiles and the masks with help of indices
            arr_lst = [ras_lst[i].ReadAsArray() for i in range(len(ras_lst))]
            mask_arr_lst = [mask_lst[i].ReadAsArray() for i in range(len(mask_lst))]
            cso_arr_lst = [cso_lst[i].ReadAsArray() for i in range(len(cso_lst))]
            col_arr_lst = [np.ones(arr_lst[i].shape) * i for i in range(len(ras_lst))]

            # mask out all non-broadleaf trees
            for i in range(len(arr_lst)):
                arr_lst[i][mask_arr_lst[i] == 0] = -32767 # no data value FORCE -32767
                cso_arr_lst[i][mask_arr_lst[i] == 0] = -32767

            # concatenate the masked tiles and set NaN
            # 1. for the normal tiles
            conc_arr = np.concatenate(arr_lst, axis = 0)
            conc_arr = conc_arr + 0.0 # trick to convert dtype of arr to float, normal way didn't work
            conc_arr[conc_arr == -32767.0] = np.nan
            #conc_arr[conc_arr < 0.0] = np.nan

            # flatten (make 1-dimensional) to exclude all NaN cells afterwards
            val_arr_f = np.ndarray.flatten(conc_arr)
            val_arr_f = val_arr_f[np.logical_not(np.isnan(val_arr_f))]

            # 2. for the cso tiles
            cso_conc_arr = np.concatenate(cso_arr_lst, axis=0)
            cso_conc_arr = cso_conc_arr + 0.0

            # Use normal tiles arr to set the NaN vals, so that both concatenated arrs have them at the same places
            cso_conc_arr[np.isnan(conc_arr)] = np.nan
            # conc_arr[conc_arr < 0.0] = np.nan

            # flatten (make 1-dimensional) to exclude all NaN cells afterwards
            cso_arr_f = np.ndarray.flatten(cso_conc_arr)
            cso_arr_f = cso_arr_f[np.logical_not(np.isnan(cso_arr_f))]

            # 2. for the cso tiles
            col_conc_arr = np.concatenate(col_arr_lst, axis=0)
            col_conc_arr = col_conc_arr + 0.0

            # Use normal tiles arr to set the NaN vals, so that both concatenated arrs have them at the same places
            col_conc_arr[np.isnan(conc_arr)] = np.nan
            # conc_arr[conc_arr < 0.0] = np.nan

            # flatten (make 1-dimensional) to exclude all NaN cells afterwards
            col_arr_f = np.ndarray.flatten(cso_conc_arr)
            col_arr_f = cso_arr_f[np.logical_not(np.isnan(cso_arr_f))]

            seed(1)
            rnd_ind = random.sample(range(val_arr_f.shape[0]), 100000)
            val_arr_r = val_arr_f[rnd_ind]
            cso_arr_r = cso_arr_f[rnd_ind]
            col_arr_r = col_arr_f[rnd_ind]

            # val_lst.append(conc_arr_r)
            # obs_lst.append(cso_arr_r)
            # col_lst.append(col_arr_r)
            # num += 1
            #
            # val_arr = np.concatenate(val_lst, axis=0)
            # obs_arr = np.concatenate(obs_lst, axis=0)
            # col_arr = np.concatenate(col_lst, axis=0)

            print("Plotting subplot", y, x)
            #a
            # axs[y,x].set_ylim(0, 100)
            # axs[y,x].scatter(val_arr, obs_arr, marker='o')
            # axs[y,x].set_xlabel(abr)
            # #axs[y,x].set_ylabel('clear sky observations')
            # axs[y, 0].set_ylabel(num_scn + " Scenes", fontsize=24)
            # axs[0, x].set_title(seg + " Splits", fontsize=24)

            #b
            axs[x,y].set_ylim(0, 100)
            axs[x, y].set_xlim(-2500, 10000)
            axs[x,y].scatter(val_arr_r, cso_arr_r, marker='o', s = 0.1)
            axs[x,y].set_xlabel(abr)
            #axs[y,x].set_ylabel('clear sky observations')
            axs[0 ,y].set_title(num_scn + " Scenes", fontsize=24)
            axs[x, 0].set_ylabel(seg + " Splits", fontsize=24)

            axs2[x, y].set_ylim(0, 40000)
            axs2[x,y].hist(val_arr_r, bins=30)
            axs2[x,y].set_xlabel(abr)
            #axs2[y,x].set_ylabel('clear sky observations')
            axs2[0 ,y].set_title(num_scn + " Scenes", fontsize=24)
            axs2[x, 0].set_ylabel(seg + " Splits", fontsize=24)

            y += 1
        x += 1

    fig.suptitle('date sensitivity vs. cso ' + abr, fontsize=30)
    print('Export Plot:', 'date sensitivity vs. cso ' + abr)
    fig.savefig(r'Y:\germany-drought\level4_sensitivity\plots\date_sens-cso_' + abr + '.png')

    fig2.suptitle('histogram ' + abr, fontsize=30)
    print('Export Plot:', 'histogram ' + abr)
    fig2.savefig(r'Y:\germany-drought\level4_sensitivity\plots\histogram_' + abr + '.png')

print("Done!")