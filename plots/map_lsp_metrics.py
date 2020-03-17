import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt

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

tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'

tiles_df = gpd.read_file(tiles_pth)

abr_lst = ['DEM', 'DSS', 'DRI', 'DPS', 'DFI', 'DES', 'DLM']
# 'LTS', 'LGS', 'VEM', 'VSS', 'VRI', 'VPS', 'VFI', 'VES', 'VLM', 'VBL', 'VSA', 'IST', 'IBL', 'IBT', 'IGS',
#            'RAR', 'RAF', 'RMR', 'RMF']

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

subset2 = ['X0061_Y0045','X0067_Y0046','X0056_Y0053','X0061_Y0058']

legend_dict = {'DEM' : [-365, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 365],
                'DSS': [-365, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 365],
                'DRI': [-365, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 365],
                'DPS': [-365, 0, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 365],
                'DFI': [-365, 0, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 365],
                'DES': [-365, 0, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 365],
                'DLM': [-365, 0, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 365]}

for abr in abr_lst:
    out_df_lst = []
    for j in range(5):
        out_df_lst.append(pd.DataFrame(index= tile_name_lst, columns=abr_lst))

    #abr = 'DPS'
    for tile_name in tile_name_lst:

        print(tile_name)

        ras_pth = r'Y:\germany-drought\level4\\' + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.tif'
        msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'

        ras = gdal.Open(ras_pth)
        msk_ras = gdal.Open(msk_pth)

        arr = ras.ReadAsArray()
        msk_arr = msk_ras.ReadAsArray() #

        for i in range(5):
            arr_sub = arr[i,:,:]

            arr_sub[msk_arr == 0] = -32767  # no data value FORCE -32767
            arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
            arr_sub[arr_sub == -32767.0] = np.nan

            # flatten (make 1-dimensional) to exclude all NaN cells afterwards
            arr_f = np.ndarray.flatten(arr_sub)
            arr_f = arr_f[np.logical_not(np.isnan(arr_f))]

            mean_st = np.mean(arr_f)

            out_df_lst[i].at[ tile_name,abr] = mean_st

    #### DOY measures
    ## the logic behind the raster values
    ## 2014 = 365    2015 = 365      2016 = 366      2017 = 365          2018 = 365
    ## 0 * 365 + x   1 * 365 + x     2 * 365 + x     3 * 365 + x + 1     4 * 365 + x + 1
    ## DOY = x       x - 365         x - 2*365       x - 3*365 - 1       x - 4 * 365 - 1
    i=1
    for i in range(5):
        out_df = out_df_lst[i].copy()
        out_df.index.name = 'Name'
        out_df.reset_index(inplace=True)
        if  i <= 2:
            out_df[abr] = out_df[abr] -  i * 365
        else:
            out_df[abr] = out_df[abr] - i * 365 - 1

        bin_list = legend_dict[abr]

        out_df["quant_cuts"] = pd.cut(out_df[abr], bins=bin_list, labels=bin_list[1:])

        merged_df = tiles_df.set_index('Name').join(out_df.set_index('Name'))
        merged_df['quant_cuts'] = merged_df['quant_cuts'].astype('int32')

        fig, ax = plt.subplots(1, figsize=(10,10))
        # merged_df.plot(ax=ax, column = "quant_cuts", categorical=True)
        merged_df.plot(ax=ax, column="quant_cuts", cmap='RdYlGn', linewidth=0.8,  edgecolor='k', legend=True, categorical=True)
        ax.set_title( abr + ' ' + str(i + 2014), fontdict = {'fontsize': '25', 'fontweight': '3'})
        # ax.legend(loc='center left')
        # plt.show()
        # vmin, vmax = merged_df[abr].min(), merged_df[abr].max()
        # sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # sm._A = []
        # cbar = fig.colorbar(sm)

        #plt.show()
        fig.savefig(r'Y:\germany-drought\maps\map_' + abr + '_' + str(i + 2014) + '.png', dpi = 300)
        plt.close()