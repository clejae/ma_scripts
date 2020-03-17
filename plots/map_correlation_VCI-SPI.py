import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

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

abr = 'VCI'
year = '2018'
tree = 'BROADLEAF'
spi_str = '03'
monat = '06'

print(abr + '\n')
out_df = pd.DataFrame(index=tile_name_lst, columns=range(1,13))

for tile_name in tile_name_lst:
    print(tile_name)

    ras_pth = r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\\' + year + '_BL-2013-2019_' + abr + '.tif'
    spi_pth = r'Y:\germany-drought\SPI\\' + tile_name + r'\SPI_'+monat+'2018_'+spi_str+'.tif'
    msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_GRASSLAND.tif'

    ras = gdal.Open(ras_pth)
    spi_ras = gdal.Open(spi_pth)
    msk_ras = gdal.Open(msk_pth)

    arr = ras.ReadAsArray()
    spi_bu = spi_ras.ReadAsArray()
    msk_arr = msk_ras.ReadAsArray() #

    for month in range(12):

        spi = spi_bu.copy()
        arr_sub = arr[month,:,:]

        arr_sub[msk_arr == 0] = -32767  # no data value FORCE -32767
        arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_sub[arr_sub == -32767.0] = np.nan

        arr_sub[arr_sub < -15.0] = -15.0
        arr_sub[arr_sub > 100.0] = 100.0

        spi[spi == 0] = -999
        spi[msk_arr == 0] = -999
        spi = spi + 0.0
        spi[spi == -999] = np.nan

        arr_sub[np.isnan(spi)] = np.nan
        spi[np.isnan(arr_sub)] = np.nan

        arr_f = np.ndarray.flatten(arr_sub)
        arr_f = arr_f[np.logical_not(np.isnan(arr_f))]

        spi_f = np.ndarray.flatten(spi)
        spi_f = spi_f[np.logical_not(np.isnan(spi_f))]


        if np.nansum(arr_sub) != 0:
            print('correlate')
            corr_coef = np.corrcoef(arr_f, spi_f)
            corr = corr_coef[0, 1]
            out_df.at[tile_name, month+1] = corr
        else:
            out_df.at[tile_name, month+1] = ''

col_name_lst = ['Name', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']

out_df.index.name = 'Name'
out_df.reset_index(inplace=True)
out_df.columns = col_name_lst

out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\CORR_of_VCI-SPI-' + spi_str + '_'+monat+'-2018.csv'
out_df.to_csv(out_name, index=False, decimal=".", sep=",")

merged_df = tiles_df.set_index('Name').join(out_df.set_index('Name'))

fig, axs = plt.subplots(1, 7, figsize=(26, 4))
c = mcolors.ColorConverter().to_rgb
for x, col in enumerate(col_name_lst[6:]):
    print(x, col, ':')
    merged_df[col] = pd.to_numeric(merged_df[col])
    vmin, vmax = merged_df[col].min(), merged_df[col].max()
    if vmin < 0 and vmax > 0:
        vrange = abs(vmin) + abs(vmax)
        vmid = abs(vmin)/vrange # zero
        vdiv1 = vmid - 0.99 * (vmid)
        vdiv2 = vmid + 0.99 * (1-vmid)
    elif vmin > 0  and vmax > 0:
        vmid = 0.5
        vdiv1 = 0.01
        vdiv2 = 0.99
    elif vmin < 0 and vmax < 0:
        vmid = 0.5
        vdiv1 = 0.01
        vdiv2 = 0.99
    cmap = makeColormap([c('#d7191c'), vdiv1, c('#d7191c'), c('#ffffbf'), vmid, c('#ffffbf'), c('#2c7bb6'), vdiv2, c('#2c7bb6')])
    merged_df.plot(column=col, cmap=cmap, ax=axs[x], linewidth=0.8, edgecolor='k', legend=True)
    axs[x].title.set_text(col[1:])
    axs[x].axis('off')
fig.suptitle('Correlation of VCI and SPI-' + spi_str + '_'+monat+'-2018', fontsize=16)
fig.show()
fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\CORR_of_VCI-SPI-' + spi_str + '_'+monat+'-2018.png')

