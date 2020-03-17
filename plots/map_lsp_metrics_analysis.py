import numpy as np
import pandas as pd
import geopandas as gpd
import gdal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

abr_lst = ['DPS', 'DEM', 'DSS', 'DRI', 'DFI', 'DES', 'DLM']
# 'LTS', 'LGS', 'VEM', 'VSS', 'VRI', 'VPS', 'VFI', 'VES', 'VLM', 'VBL', 'VSA', 'IST', 'IBL', 'IBT', 'IGS',
#            'RAR', 'RAF', 'RMR', 'RMF']

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

subset2 = ['X0061_Y0045','X0067_Y0046','X0056_Y0053','X0061_Y0058']

for abr in abr_lst:
    out_df = pd.DataFrame(index= tile_name_lst, columns=[abr])

    #abr = 'DPS'
    for tile_name in tile_name_lst:

        print(abr, tile_name)

        ras_pth = r'Y:\germany-drought\level4_analysis\\' + tile_name + r'\COMP-2014-2017-TO-2018_' + abr + '.tif'
        msk_pth = r'Y:\germany-drought\masks\\' + tile_name + r'\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'

        ras = gdal.Open(ras_pth)
        msk_ras = gdal.Open(msk_pth)

        arr = ras.ReadAsArray()
        msk_arr = msk_ras.ReadAsArray() #

        arr[msk_arr == 0] = -32767  # no data value FORCE -32767
        arr = arr + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr[arr == -32767.0] = np.nan
        arr[arr > 500.0] = np.nan
        arr[arr < -500.0] = np.nan

        # flatten (make 1-dimensional) to exclude all NaN cells afterwards
        arr_f = np.ndarray.flatten(arr)
        arr_f = arr_f[np.logical_not(np.isnan(arr_f))]

        mean_st = np.mean(arr_f)

        out_df.at[tile_name,abr] = mean_st

    #### DOY measures
    ## the logic behind the raster values
    ## 2014 = 365    2015 = 365      2016 = 366      2017 = 365          2018 = 365
    ## 0 * 365 + x   1 * 365 + x     2 * 365 + x     3 * 365 + x + 1     4 * 365 + x + 1
    ## DOY = x       x - 365         x - 2*365       x - 3*365 - 1       x - 4 * 365 - 1

    out_df.index.name = 'Name'
    out_df.reset_index(inplace=True)

    bin_list = [-500,-25,-20,-15,-10,-5, 0, 5, 10, 15, 20, 25, 500]

    out_df["quant_cuts"] = pd.cut(out_df[abr], bins=bin_list, labels=bin_list[1:])

    merged_df = tiles_df.set_index('Name').join(out_df.set_index('Name'))
    merged_df['quant_cuts'] = merged_df['quant_cuts'].astype('int32')
    merged_df[abr] = merged_df[abr].astype('float32')

    merged_df.to_file(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\\' + abr + '_analysis_2018-avg14-17.shp')

    fig, ax = plt.subplots(1, figsize=(10,10))
    merged_df.plot(ax=ax, column="quant_cuts", cmap='RdYlGn', linewidth=0.8,  edgecolor='k', legend=True, categorical=True)
    ax.set_title( abr + r': 2018 - Avg(14-17)' , fontdict = {'fontsize': '25', 'fontweight': '3'})
    fig.show()

    vmin, vmax = merged_df[abr].min(), merged_df[abr].max()
    vrange = abs(vmin - vmax)
    vprop = float((vrange - abs(vmax))/vrange)
    vdivide1 = float(vprop/2)
    vdivide2 = float(0.97)
    c = mcolors.ColorConverter().to_rgb
    rvb = makeColormap([c('red'), c('yellow'), vdivide1, c('yellow'), c('blue'), vdivide2, c('blue')])
    rvb = makeColormap([c('red'), c('orange'), vdivide1, c('orange'), c('white'), vprop, c('white'), c('green'), vdivide2, c('green')])

    fig2, ax2 = plt.subplots(1,1, figsize=(10,10))
    merged_df.plot(column=abr, cmap=rvb, ax = ax2, linewidth=0.8,  edgecolor='k', legend=True)
    ax2.set_title(abr + r': 2018 - Avg(14-17)' , fontdict = {'fontsize': '25', 'fontweight': '3'})
    fig2.show()

    fig3, ax3 = plt.subplots(1, 1)
    merged_df.plot(column=abr, ax=ax3, cmap='RdYlGn', legend=True)
    ax3.set_title(abr + r': 2018 - Avg(14-17)', fontdict={'fontsize': '25', 'fontweight': '3'})
    vmin, vmax = merged_df[abr].min(), merged_df[abr].max()
    sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig3.colorbar(sm)
    fig3.show()

    fig.savefig(r'Y:\germany-drought\maps\map_metric_analysis' + abr + '.png', dpi = 300)
    plt.close()