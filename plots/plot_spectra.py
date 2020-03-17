import gdal
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import math

fig, axs = plt.subplots(3, 5, figsize=(20, 20), sharey=True)
plt.tight_layout()
plt.rcParams.update({'font.size':16})

folders = glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')
folders.sort()
folders = folders[20:35]

#folder_lst = ['LIN-ITPL_02-SEG_16-INT','LIN-ITPL_03-SEG_16-INT','LIN-ITPL_04-SEG_16-INT','RBF-ITPL_02-SEG_32-INT_SIG8','RBF-ITPL_03-SEG_32-INT_SIG8','RBF-ITPL_04-SEG_32-INT_SIG8']


x = 19
y = 9

for j, folder in enumerate(folders):
    print(j, folder)
    tail_folder = os.path.split(folder)[1]

    tsi_file = glob.glob(folder + r'\\**\*TSI.tif')
    header = glob.glob(folder + r'\\**\*TSI.hdr')
    tsi_ras = gdal.Open(tsi_file[0])
    tsi_arr = tsi_ras.ReadAsArray()

    dss_file = glob.glob(folder + r'\\**\*DSS.tif')
    dss_ras = gdal.Open(dss_file[0])
    dss_arr = dss_ras.ReadAsArray()

    with open(header[0], 'r') as f:
        tsi_file = f.readlines()
        line = tsi_file[20].split(" = ")
        dates = line[0][:-2]
        dates_lst = dates.split(", ")

    tsi_slice = tsi_arr[:, y, x]
    tsi_slice = tsi_slice + 0.0
    tsi_slice[tsi_slice == -32767.0] = np.nan

    doy = dss_arr[y,x]

    x_ind = j // 5
    factor = math.floor(j / 5)
    y_ind = j - factor * 5

    axs[x_ind, y_ind].plot(range(len(tsi_slice)), tsi_slice, label=dates_lst)
    axs[x_ind, y_ind].title.set_text(tail_folder)
    axs[x_ind, y_ind].text(1, 1000, 'DSS:' + str(doy), fontsize=18)

fig.show()
fig.savefig(r'Y:\germany-drought\level4_sensitivity\plots\spectra-comparison.png')