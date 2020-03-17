# derive monthly SMI values per force-tile

import numpy as np
import pandas as pd
import geopandas as gpd
import gdal

tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
tiles_df = gpd.read_file(tiles_pth)

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

out_df = pd.DataFrame(index=tile_name_lst, columns=range(1,13))
#out_df_share = pd.DataFrame(index=tile_name_lst, columns=range(1,13))

abr = 'SMI'
year = '2018'

month_lst = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
col_lst = ['_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']

out_df_bl = pd.DataFrame(index=tile_name_lst, columns=col_lst)
out_df_con = pd.DataFrame(index=tile_name_lst, columns=col_lst)
out_df_gra = pd.DataFrame(index=tile_name_lst, columns=col_lst)

for i, month in enumerate(month_lst):
    for tile_name in tile_name_lst:
        print(month, tile_name)

        ras_pth = r'Y:\germany-drought\SMI\\' + tile_name + r'\\'+abr+'_' + month + year + '_Gesamtboden.tif'
        msk_bl_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'
        msk_con_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-CONIFER_UNDISTURBED-2013_BUFF-01.tif'
        msk_gra_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_GRASSLAND.tif'

        ras = gdal.Open(ras_pth)
        msk_bl_ras = gdal.Open(msk_bl_pth)
        msk_con_ras = gdal.Open(msk_con_pth)
        msk_gra_ras = gdal.Open(msk_gra_pth)

        arr_bl = ras.ReadAsArray()
        arr_con = arr_bl.copy()
        arr_gra = arr_bl.copy()

        msk_bl_arr = msk_bl_ras.ReadAsArray()
        msk_con_arr = msk_con_ras.ReadAsArray()
        msk_gra_arr = msk_gra_ras.ReadAsArray()

        arr_bl[msk_bl_arr == 0] = -32767  # no data value FORCE -32767
        arr_bl = arr_bl + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_bl[arr_bl == -32767] = np.nan

        arr_con[msk_con_arr == 0] = -32767  # no data value FORCE -32767
        arr_con = arr_con + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_con[arr_con == -32767] = np.nan

        arr_gra[msk_gra_arr == 0] = -32767  # no data value FORCE -32767
        arr_gra = arr_gra + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_gra[arr_gra == -32767] = np.nan

        mean_bl = np.nanmean(arr_bl)
        mean_con = np.nanmean(arr_con)
        mean_gra = np.nanmean(arr_gra)
        # mean_share = mean_st * lc_share

        out_df_bl.at[tile_name, col_lst[i]] = mean_bl
        out_df_con.at[tile_name, col_lst[i]] = mean_con
        out_df_gra.at[tile_name, col_lst[i]] = mean_gra

col_name_lst = ['Name', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']

out_name_bl.index.name = 'Name'
out_name_bl.reset_index(inplace=True)
out_name_bl.columns = col_name_lst

out_name_con.index.name = 'Name'
out_name_con.reset_index(inplace=True)
out_name_con.columns = col_name_lst

out_name_gra.index.name = 'Name'
out_name_gra.reset_index(inplace=True)
out_name_gra.columns = col_name_lst

out_name_bl = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_broadleaf.csv'
out_df_bl.to_csv(out_name_bl, index=False, decimal=".", sep=",")

out_name_con = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_conifer.csv'
out_df_con.to_csv(out_name_con, index=False, decimal=".", sep=",")

out_name_gra = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\'+abr+'_' + year + '_grass.csv'
out_df_gra.to_csv(out_name_gra, index=False, decimal=".", sep=",")