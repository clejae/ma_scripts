import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
tiles_df = gpd.read_file(tiles_pth)

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

abr = 'DSS'
year = '2016'
tree = 'BROADLEAF'
endy = '9'

# DRI & DSS
if abr == 'DSS' or abr == 'DRI':
    cut_lst = [-32768, -32767, -50, -25, 0, 25, 50, 75, 100, 125, 150, 10000]
# DES & DFI
if abr == 'DES' or abr == 'DFI':
    cut_lst = [-32768, -32767, 0, 150, 200, 250, 300, 325, 350, 365, 10000]
if abr == 'DPS':
    cut_lst = [-32768, -32767, 0, 100, 125, 150, 175, 200, 225, 250, 365, 10000]
if abr == 'LGS':
    cut_lst = [-32768, -32767, 0, 150, 175, 200, 225, 250, 275, 300, 365, 10000]

year_ind_dict = {'2014':0,
                 '2015':1,
                 '2016':2,
                 '2017':3,
                 '2018':4}

hist_lst_brd = []
hist_lst_gra = []

print(abr, '\n')

tile_name = tile_name_lst[50]
for tile_name in tile_name_lst:
    print(tile_name)

    ras_pth = r'Y:\germany-drought\level4\\' + tile_name + r'\\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.tif'
    brd_msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-' + tree + '_UNDISTURBED-2013_BUFF-01.tif'
    gra_msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_GRASSLAND.tif'

    ras = gdal.Open(ras_pth)
    brd_msk_ras = gdal.Open(brd_msk_pth)
    gra_msk_ras = gdal.Open(gra_msk_pth)

    arr = ras.ReadAsArray()
    brd_msk_arr = brd_msk_ras.ReadAsArray() #
    gra_msk_arr = gra_msk_ras.ReadAsArray()  #

    #### DOY measures
    ## the logic behind the raster values
    ## 2014 = 365    2015 = 365      2016 = 366      2017 = 365          2018 = 365
    ## 0 * 365 + x   1 * 365 + x     2 * 365 + x     3 * 365 + x + 1     4 * 365 + x + 1
    ## DOY = x       x - 365         x - 2*365       x - 3*365 - 1       x - 4 * 365 - 1

    year_ind = year_ind_dict[year]

    arr_slice = arr[year_ind,:,:]
    if abr == 'DSS' or abr == 'DRI' or abr == 'DFI' or abr == 'DPS' or abr == 'DES':
        if year == '2017' or year == '2018':
            arr_sub = arr_slice - (year_ind * 365-1)
        else:
            arr_sub = arr_slice - (year_ind * 365)
    else:
        arr_sub = arr_slice.copy()
    arr_sub[arr_slice == -32767] = -32767

    brd_sub = arr_sub.copy()
    gra_sub = arr_sub.copy()

    brd_sub[brd_msk_arr == 0] = -32767  # no data value FORCE -32767
    gra_sub[gra_msk_arr == 0] = -32767  # no data value FORCE -32767

    count_lst_brd = []
    count_lst_gra = []
    for i in range(len(cut_lst) - 1):
        val_brd = ((cut_lst[i] < brd_sub) & (brd_sub <= cut_lst[i + 1])).sum()
        val_gra = ((cut_lst[i] < gra_sub) & (gra_sub <= cut_lst[i + 1])).sum()
        count_lst_brd.append(val_brd)
        count_lst_gra.append(val_gra)

    hist_lst_brd.append(count_lst_brd)
    hist_lst_gra.append(count_lst_gra)

col_lst = []
for i, item in enumerate(cut_lst[:-1]):
    col_lst.append(abr + '_' + str(item+1) + '_to_' + str(cut_lst[i+1]))

out_df_brd = pd.DataFrame(hist_lst_brd)
out_df_brd.columns = col_lst
out_df_brd['Tile'] = tile_name_lst

out_df_gra = pd.DataFrame(hist_lst_gra)
out_df_gra.columns = col_lst
out_df_gra['Tile'] = tile_name_lst

out_df_brd.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\tables\tile_counts_lsp_metrics\tile_counts_lsp_metrics' + year + '_' + abr + '_' + tree + '.csv', index=False)
out_df_gra.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\tables\tile_counts_lsp_metrics\tile_counts_lsp_metrics' + year + '_' + abr + '_' + 'GRASSLAND' + '.csv', index=False)

hist_counts_brd = []
hist_counts_gra = []
for i in range(1,len(cut_lst)-1):
    val_brd = 0
    val_gra = 0
    for item in hist_lst_brd:
        val_brd = val_brd + item[i]
    hist_counts_brd.append(val_brd)
    for item in hist_lst_gra:
        val_gra = val_gra + item[i]
    hist_counts_gra.append(val_gra)

label_lst = []
for i, item in enumerate(cut_lst[1:-1]):
    label_lst.append(str(item + 1) + ' to ' + str(cut_lst[i+2]))

fig, ax = plt.subplots(figsize=(8,7))
rects = ax.bar(label_lst, hist_counts_brd)
plt.xticks(rotation=45, ha='right')
plt.title('Histogramm ' + abr + ' ' + tree + ' ' + year)
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
#fig.show()
fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\Histogramm_'+year+'_' + abr + '-' + tree + '.png')

fig2, ax2 = plt.subplots(figsize=(8,7))
rects = ax2.bar(label_lst, hist_counts_gra)
plt.xticks(rotation=45, ha='right')
plt.title('Histogramm ' + abr + ' ' + 'GRASSLAND ' + year)
plt.tight_layout()
for rect in rects:
    height = rect.get_height()
    ax2.annotate('{}'.format(format(int(height), ',')),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
ax2.get_yaxis().set_major_formatter(
    tick.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.gcf().subplots_adjust(left=0.15)
#fig2.show()
fig2.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\Histogramm_'+year+'_' + abr + '-' + 'GRASSLAND' + '.png')