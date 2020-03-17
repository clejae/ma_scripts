import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib
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

def deleteQuotesInTxt(text_file):
    f_in = open(text_file, "rt")
    f_out = open(text_file[:-4] + '_r.csv', "wt")

    for line in f_in:
        f_out.write(line.replace('"', ''))

    f_in.close()
    f_out.close()


tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
tiles_df = gpd.read_file(tiles_pth)

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]
#tile_name_lst = ['X0061_Y0045','X0067_Y0046','X0056_Y0053','X0061_Y0058']

abr = 'VCI'
year = '2017'
tree = 'BROADLEAF'
endy = '9'
print(abr + '\n')
out_df = pd.DataFrame(index=tile_name_lst, columns=range(1,13))
for tile_name in tile_name_lst:
    print(tile_name)

    ras_pth = r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\\' + year + '_BL-2013-201' + endy + '_' + abr + '.tif'
    msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-'+ tree + '_UNDISTURBED-2013_BUFF-01.tif'
    #msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_GRASSLAND.tif'

    ras = gdal.Open(ras_pth)
    msk_ras = gdal.Open(msk_pth)

    arr = ras.ReadAsArray()
    msk_arr = msk_ras.ReadAsArray() #

    for month in range(12):
        arr_sub = arr[month,:,:]

        arr_sub[msk_arr == 0] = -32767  # no data value FORCE -32767
        arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_sub[arr_sub == -32767.0] = np.nan
        if abr == 'VCI':
            arr_sub[arr_sub < -15.0] = -15.0
            arr_sub[arr_sub > 100.0] = 100.0

        mean_st = np.nanmean(arr_sub)

        out_df.at[ tile_name,month+1] = mean_st

col_name_lst = ['Name', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
out_df.index.name = 'Name'
out_df.reset_index(inplace=True)
out_df.columns = col_name_lst

# backup_df = out_df.copy()
# out_df = backup_df.copy()
out_df = out_df.fillna(-999)

bin_list = [-900, 0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
quant_df = pd.DataFrame(out_df['Name'].copy())
for x, col in enumerate(col_name_lst[1:]):
    quant_df[col]  = pd.cut(out_df[col], bins=bin_list, labels=bin_list[1:])

out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_'+ tree + '_BL-13-1' + endy + '.csv'
#out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_GRASSLAND_BL-13-1' + endy + '.csv'
out_df.to_csv(out_name, index=False, decimal=".", sep=",")

# out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_'+ tree + '_BL-13-1' + endy + '_categories.csv'
# quant_df.to_csv(out_name, index=False, decimal=".", sep=",")

merged_df = tiles_df.set_index('Name').join(quant_df.set_index('Name'))

fig, axs = plt.subplots(1, 12, figsize=(26, 4))
#fig, axs = plt.subplots(1, 8, figsize=(17.3, 4))
#for x, col in enumerate(col_name_lst[1:9]):
for x, col in enumerate(col_name_lst[1:]):
    print(x, col, ':')
    cmap = matplotlib.cm.RdYlGn
    cmap.set_under('w')
    merged_df.plot(column=col, cmap=cmap, ax=axs[x], linewidth=0.8, edgecolor='k',legend=True)
    axs[x].title.set_text(col[1:])
    axs[x].axis('off')
# sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=0, vmax=100))
# sm._A = []
# #divider = make_axes_locatable(axs[11])
# divider = make_axes_locatable(axs[7])
# cax = divider.append_axes("right", size="5%", pad = 0.05)
# cbar = fig.colorbar(sm, cax= cax)
# fig.suptitle(abr + ': ' + year + ' '+ tree + ' BL-2013-201' + endy , fontsize=16)
fig.suptitle(abr + ': ' + year + '_grass_BL-13-1' + endy , fontsize=16)
fig.show()
# fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\\' + abr + '-' + year + '_grass_BL-13-1' + endy + '.png')
fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\\' + abr + '-' + year + '_'+ tree + '_BL-2013-201' + endy + '.png')

    # for col_name in col_name_lst[1:]:
    #     out_df[col_name] = out_df[col_name].astype('float32')

    # merged_df = tiles_df.set_index('Name').join(out_df.set_index('Name'))
    # merged_df.to_file(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\VCI_2018_BL-13-17.shp')
    # out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\VCI_2018_BL-13-17.csv'
    # out_df.to_csv(out_name, index=False, decimal=",", na_rep=-9999,sep=";")
    # out_df.to_csv(out_name, index=False, decimal=".", sep=",")

#     col = '_01'
#
#     fig, axs = plt.subplots(1, 12, figsize=(24, 6))
#
#     for x, col in enumerate(col_name_lst[1:]):
#         print(x, col,':')
#         vmin, vmax = merged_df[col].min(), merged_df[col].max()
#         print(vmin,vmax)
#         c = mcolors.ColorConverter().to_rgb
#         first_div = 50/vmax
#         sec_div = 90/vmax
#         print(first_div, sec_div)
#         rvb = makeColormap([c('red'), c('yellow'), 0.10, c('yellow'), c('blue'), sec_div, c('blue')])
#         rvb.set_bad(color='white')
#         merged_df.plot(column=col, cmap=rvb, ax=axs[x], linewidth=0.8, edgecolor='k', legend=True)
#         # if x < len(col_name_lst[1:])-1:
#         #     merged_df.plot(column=col, cmap=rvb, ax=axs[x], linewidth=0.8, edgecolor='k')
#         # elif x == len(col_name_lst)-1:
#         #     merged_df.plot(column=col, cmap=rvb, ax=axs[x], linewidth=0.8, edgecolor='k', legend=True)
#         axs[x].title.set_text(col[1:])
#         axs[x].axis('off')
#     #fig.title(abr + ':' + col[1:] + ' 2018 BL-2013-2017')
#     fig.show()
#
#     fig.savefig(r'Y:\germany-drought\maps\map_' + abr + '_' + str(i + 2014) + '.png', dpi = 300)
#     plt.close()
#
# fig2, ax2 = plt.subplots(1, 1, figsize=(10, 10))
# merged_df.plot(column=col, cmap=rvb, ax=ax2, linewidth=0.8, edgecolor='k', legend=True)
# ax2.set_title(abr + ':' + col[1:] + ' 2018 BL-2013-2017', fontdict={'fontsize': '25', 'fontweight': '3'})
# fig2.show()

# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# merged_df.plot(column=col, cmap='RdYlGn', ax=ax, linewidth=0.8, edgecolor='k', legend=True)
# ax.set_title(abr + ':' + col[1:] + ' 2018 BL-2013-2017', fontdict={'fontsize': '25', 'fontweight': '3'})
# fig.show()