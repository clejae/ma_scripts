import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

# tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
# tiles_df = gpd.read_file(tiles_pth)

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

spi_lst =[ '01', '24', '03', '48', '12', '18']

for spi in spi_lst:
    print(spi)
    #spi = '06'

    month_lst =[ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    out_df = pd.DataFrame(index=tile_name_lst, columns=month_lst)
    for tile_num, tile_name in enumerate(tile_name_lst):
        print(tile_num, '/', len(tile_name_lst) )
        for month in month_lst:
            descr = 'SPI_' + month + '2018_' + spi
            ras_pth = r'Y:\germany-drought\SPI\\' + tile_name + r'\\' + descr + '.tif'
            #msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-'+ tree + '_UNDISTURBED-2013_BUFF-01.tif'

            ras = gdal.Open(ras_pth)
            #msk_ras = gdal.Open(msk_pth)

            arr = ras.ReadAsArray()
            #msk_arr = msk_ras.ReadAsArray() #

            #arr[msk_arr == 0] = -32767  # no data value FORCE -32767
            arr = arr + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
            arr[arr == 0] = np.nan

            mean_st = np.nanmean(arr)

            out_df.at[tile_name, month] = mean_st

    col_name_lst = ['Name', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
    out_df.index.name = 'Name'
    out_df.reset_index(inplace=True)
    out_df.columns = col_name_lst

    # backup_df = out_df.copy()
    # out_df = backup_df.copy()
    out_df = out_df.fillna(-999)

    bin_list = [-900, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
    quant_df = pd.DataFrame(out_df['Name'].copy())
    for x, col in enumerate(col_name_lst[1:]):
        quant_df[col]  = pd.cut(out_df[col], bins=bin_list, labels=bin_list[1:])

    out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SPI_2018_' + spi + '.csv'
    out_df.to_csv(out_name, index=False, decimal=".", sep=",")
    out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SPI_2018_' + spi + '_categories.csv'
    quant_df.to_csv(out_name, index=False, decimal=".", sep=",")

# merged_df = tiles_df.set_index('Name').join(quant_df.set_index('Name'))
#
# fig, axs = plt.subplots(1, 12, figsize=(26, 4))
# x = 0
# col = '_01'
# c = mcolors.ColorConverter().to_rgb
# cmap =  matplotlib.cm.RdYlGn
#
# a = np.array([[-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]])
# norm = mcolors.BoundaryNorm(a[0], len(a[0])-1)
# merged_df.plot(column=col, cmap=cmap, norm=norm, ax=axs[x], linewidth=0.8, edgecolor='k', legend=True)
# axs[x].title.set_text(col[1:])
# axs[x].axis('off')
# fig.suptitle('SPI_2018_' + spi , fontsize=16)
# fig.show()
#







# for x, col in enumerate(col_name_lst[1:]):
#     print(x, col, ':')
#     cmap = matplotlib.cm.RdYlGn
#     cmap.set_under('w')
#     merged_df.plot(column=col, cmap=cmap, ax=axs[x], linewidth=0.8, edgecolor='k', legend=True)
#     axs[x].title.set_text(col[1:])
#     axs[x].axis('off')
# # sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=-2.5, vmax=2.5))
# # sm._A = []
# # divider = make_axes_locatable(axs[11])
# # cax = divider.append_axes("right", size="5%", pad = 0.05)
# # cbar = fig.colorbar(sm, cax= cax)
# fig.suptitle('SPI_2018_' + spi , fontsize=16)
# fig.show()
# fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\SPI_2018_' + spi +  '.png')
