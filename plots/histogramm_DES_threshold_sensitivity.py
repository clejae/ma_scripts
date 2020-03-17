import gdal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

wd = r'Y:\germany-drought\level4_v3\X0061_Y0046\\'

cut_lst = [0, 150, 200, 250, 300, 325, 350, 365, 500]

for t in range(20, 51, 5):
    des_pth = '{0}2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_DES-LSP_0{1}.tif'.format(wd,t)
    des_ras = gdal.Open(des_pth)
    des_arr = des_ras.ReadAsArray()

    msk_pth = r'Y:\germany-drought\masks\X0061_Y0046\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'
    msk_ras = gdal.Open(msk_pth)
    msk_arr = msk_ras.ReadAsArray()

    des_arr[msk_arr == 0] = -9999
    des_arr = des_arr + 0.0
    des_arr[des_arr == -9999] = np.nan

    count_lst = []

    for i in range(len(cut_lst) - 1):
        val = np.nansum((cut_lst[i] < des_arr) & (des_arr <= cut_lst[i + 1]))
        count_lst.append(val)

    col_lst = []
    for i, item in enumerate(cut_lst[:-1]):
        col_lst.append(str(item + 1) + '_to_' + str(cut_lst[i + 1]))

    label_lst = []
    for i, item in enumerate(cut_lst[:-1]):
        label_lst.append(str(item + 1) + ' to ' + str(cut_lst[i + 1]))

    fig, ax = plt.subplots(figsize=(8, 7))
    rects = ax.bar(label_lst, count_lst)
    plt.xticks(rotation=45, ha='right')
    plt.title('Histogramm Thres: 0.{0}'.format(t))
    plt.tight_layout()
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(format(int(height), ',')),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    ax.get_yaxis().set_major_formatter(
        tick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.gcf().subplots_adjust(left=0.15)
    fig.show()

    fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\Histogramm_Thres0{0}.png'.format(t))