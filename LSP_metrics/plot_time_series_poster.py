import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ras_tss = gdal.Open(r'Y:\germany-drought\level4\X0063_Y0046\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TY_C95T_TSS.tif')
arr_tss = ras_tss.ReadAsArray()

ras_tsi = gdal.Open(r'Y:\germany-drought\level4\X0063_Y0046\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TY_C95T_TSI.tif')
arr_tsi = ras_tsi.ReadAsArray()

header_tss = r'Y:\germany-drought\level4\X0063_Y0046\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TY_C95T_TSS.hdr'
with open(header_tss, 'r') as f:
    tss_file = f.readlines()

    line = tss_file[20].split(" = ")
    dates = line[0][:-2]
    dates_lst = dates.split(", ")

    line = tss_file[25].split(" = ")
    sensors = line[0][:-2]
    sensors_lst = sensors.split(", ")
dates_lst = [float(i) for i in dates_lst]

header_tsi = r'Y:\germany-drought\level4\X0063_Y0046\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TY_C95T_TSI.hdr'
with open(header_tsi, 'r') as f:
    tsi_file = f.readlines()
    line = tsi_file[20].split(" = ")
    dates = line[0][:-2]
    dates_lst_tsi = dates.split(", ")
dates_lst_tsi = [float(i) for i in dates_lst_tsi]


def plotTimeSeries(x,y, annotation, title):
    slice_tss = arr_tss[:, y, x]
    slice_tss = slice_tss / 10000.0
    slice_tss[slice_tss == -3.2767] = np.nan
    slice_tsi = arr_tsi[:,y,x]
    slice_tsi = slice_tsi / 10000.0
    slice_tsi[slice_tsi == -3.2767] = np.nan

    color_dict = { 'LND08':'black', 'LND07':'black', 'SEN2A':'grey', 'SEN2B':'grey' }

    plt.rcParams.update({'font.size':16})
    fig, ax = plt.subplots(figsize=(10, 5))
    legend_elements = [Line2D([0], [0], color='C0', lw=2, label='RBF-Interpolation'),
                       Line2D([0], [0], marker='o', color='black', label='Landsat observation',
                              markerfacecolor='black', markersize=5, linestyle='None'),
                       Line2D([0], [0], marker='o', color='grey', label='Sentinel-2 observation',
                              markerfacecolor='grey', markersize=5, linestyle='None')]

    #0,4153005464480874
    #0,4945355191256831

    ax.scatter(dates_lst, slice_tss, color=[color_dict[i] for i in sensors_lst ])
    ax.plot(dates_lst_tsi, slice_tsi)
    ax.axvspan(2013.582, 2013.664, color='C2', alpha=0.2)
    ax.axvspan(2014.582, 2014.664, color='C2', alpha=0.2)
    ax.axvspan(2015.582, 2015.664, color='C2', alpha=0.2)
    ax.axvspan(2016.584, 2016.667, color='C2', alpha=0.2)
    ax.axvspan(2017.582, 2017.664, color='C2', alpha=0.2)
    ax.axvspan(2018.582, 2018.664, color='C1', alpha=0.2)
    ax.axvspan(2019.582, 2019.664, color='C2', alpha=0.2)
    ax.legend(handles=legend_elements,loc=3)
    ax.annotate(annotation, xy=(2013, .95), fontsize=16)
    ax.set_ylabel('NDVI')
    ax.set_ylim(0,1)
    ax.set_xlim(2013,2020)
    ax.title.set_text(title)
    fig.show()
    return fig



f1 = plotTimeSeries(x=280,y=758, annotation="Broadleaf", title= 'Combined Landsat-Sentinel-2 NDVI time-series')
f2 = plotTimeSeries(x=89,y=846, annotation="Broadleaf", title= 'Combined Landsat-Sentinel-2 NDVI time-series')
f3 = plotTimeSeries(x=670,y=380, annotation="Conifer", title= 'Combined Landsat-Sentinel-2 NDVI time-series')
f4 = plotTimeSeries(x=664,y=399, annotation="Conifer", title= 'Combined Landsat-Sentinel-2 NDVI time-series')

f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\NDVI-times-series\Combined Landsat-Sentinel NDVI time-series - Broadleaf - low VCI 2.png')
f2.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\NDVI-times-series\Combined Landsat-Sentinel NDVI time-series - Broadleaf - high VCI 2.png')
f3.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\NDVI-times-series\Combined Landsat-Sentinel NDVI time-series - Conifer - low VCI 2.png')
f4.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\NDVI-times-series\Combined Landsat-Sentinel NDVI time-series - Conifer - high VCI 2.png')