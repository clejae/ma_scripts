import gdal
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import math
import pandas as pd

folder_lst = glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')
folder_lst.sort()
folder_lst = [folder_lst[i] for i in (22,23,24,25,28,29,30,31,32,33,34)]

#folder_lst = ['LIN-ITPL_02-SEG_16-INT','LIN-ITPL_03-SEG_16-INT','LIN-ITPL_04-SEG_16-INT','RBF-ITPL_02-SEG_32-INT_SIG8','RBF-ITPL_03-SEG_32-INT_SIG8','RBF-ITPL_04-SEG_32-INT_SIG8']

# j = 1
# folder = folder_lst[0]
plt.rcParams.update({'font.size':16})
fig, axs = plt.subplots( 3, 4,  sharex=True, figsize=(20, 20),  sharey=True)
fig2, axs2 = plt.subplots( 3, 4,  sharex=True, figsize=(20, 20))
# fig, axs = plt.subplots( 3, 2,  sharex=True, figsize=(20, 20),  sharey=True)
# fig2, axs2 = plt.subplots( 3, 2,  sharex=True, figsize=(20, 20))

#for j, item in enumerate(folder_lst):
for j, folder in enumerate(folder_lst):
    #folder = r'Y:\germany-drought\level4_sensitivity\metrics\\' + item
    print(j, folder)
    tail_folder = os.path.split(folder)[1]

    file = glob.glob(folder + r'\\**\*DRI.tif')

    ras = gdal.Open(file[0])
    arr = ras.ReadAsArray()

    arr_nan = np.ones((1000,1000))
    arr_nan[arr > -32767] = 0
    num_nan_tot = np.sum(arr_nan)

    msk = gdal.Open(r'Y:\germany-drought\masks\X0056_Y0053\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif')
    msk_arr = msk.ReadAsArray()

    arr[msk_arr == 0] = -32767  # no data value FORCE -32767
    arr = arr + 0.0  # trick to convert dtype of arr to float, normal way didn't work
    arr[arr == -32767.0] = np.nan

    arr_f = np.ndarray.flatten(arr)
    arr_f = arr_f[np.logical_not(np.isnan(arr_f))]

    num_tree_pxl = np.sum(msk_arr)

    num_nan_bl = num_tree_pxl - arr_f.shape[0]

    arr_neg = arr_f[arr_f < 0]

    # derive x and y indices from current index of main loop
    x_ind = j // 3
    factor = math.floor(j / 3)
    y_ind = j - factor * 3

    # axs[y_ind, x_ind] .hist(arr_f, bins = 50)
    # axs[y_ind, x_ind].set_title(tail_folder, fontsize=18)
    # axs[y_ind, x_ind].text( -200, 50000, 'negative DOYs:\n' + str(arr_neg.shape[0]) ,  fontsize=18)
    # axs[y_ind, x_ind].text(-200, 30000, 'num nodata pxl brdl:\n' + str(num_nan_bl), fontsize=18)
    # axs[y_ind, x_ind].text(-200, 10000, 'num nodata pxl total:\n' + str(num_nan_tot), fontsize=18)
    #
    # axs2[y_ind, x_ind].scatter( arr_f, range(arr_f.shape[0]), marker='o', s = 0.6)
    # axs2[y_ind, x_ind].set_title(tail_folder, fontsize=18)
    # axs2[y_ind, x_ind].text( -200, 50000, 'negative DOYs:\n' + str(arr_neg.shape[0]) ,  fontsize=18)
    # axs2[y_ind, x_ind].text(-200, 30000, 'num nodata pxl brdl:\n' + str(num_nan_bl), fontsize=18)
    # axs2[y_ind, x_ind].text(-200, 10000, 'num nodata pxl total:\n' + str(num_nan_tot), fontsize=18)
    #
    axs[y_ind, x_ind] .hist(arr_f, bins = 50)
    axs[y_ind, x_ind].set_title(tail_folder, fontsize=18)
    axs[y_ind, x_ind].text( -220, 70000, 'negative DOYs:\n' + str(arr_neg.shape[0]) ,  fontsize=18)
    axs[y_ind, x_ind].text(-220, 60000, 'num nodata pxl brdl:\n' + str(num_nan_bl), fontsize=18)
    axs[y_ind, x_ind].text(-220, 50000, 'num nodata pxl total:\n' + str(num_nan_tot), fontsize=18)

    axs2[y_ind, x_ind].scatter( arr_f, range(arr_f.shape[0]), marker='o', s = 0.6)
    axs2[y_ind, x_ind].set_title(tail_folder, fontsize=18)
    # axs2[y_ind, x_ind].text( -200, 50000, 'negative DOYs:\n' + str(arr_neg.shape[0]) ,  fontsize=18)
    # axs2[y_ind, x_ind].text(-200, 30000, 'num nodata pxl brdl:\n' + str(num_nan_bl), fontsize=18)
    # axs2[y_ind, x_ind].text(-200, 10000, 'num nodata pxl total:\n' + str(num_nan_tot), fontsize=18)

fig.show()
fig2.show()

fig.savefig(r'Y:\germany-drought\level4_sensitivity\plots\sens2_histogram_2.png')
fig2.savefig(r'Y:\germany-drought\level4_sensitivity\plots\sens2_data-distribution_2.png')

