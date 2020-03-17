import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import datetime
import pandas as pd

##########################################################
# tile_name = 'X0061_Y0045'
# wd = r'Y:\germany-drought\level4_sensitivity\metrics\\'
# wd_ext = r'ALL_OBS-08_LSP_SEG\\'
# seg = '8'
#
# ras_tss = gdal.Open(wd + r'TSS\\' + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSS.tif')
# arr_tss = ras_tss.ReadAsArray()
#
# ras_tsi = gdal.Open(wd + r'TSS\\' + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSI.tif')
# arr_tsi = ras_tsi.ReadAsArray()
#
# ras_dss = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DSS.tif')
# arr_dss = ras_dss.ReadAsArray()
#
# ras_dps = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DPS.tif')
# arr_dps = ras_dps.ReadAsArray()
#
# ras_des = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DES.tif')
# arr_des = ras_des.ReadAsArray()
#
# ras_dfi = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DFI.tif')
# arr_dfi = ras_dfi.ReadAsArray()
#
# ras_dri = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DRI.tif')
# arr_dri = ras_dri.ReadAsArray()
#
# ras_lgs = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_LGS.tif')
# arr_lgs = ras_lgs.ReadAsArray()
#
# ras_igs = gdal.Open(wd + wd_ext + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_IGS.tif')
# arr_igs = ras_igs.ReadAsArray()
#
# header_tss = wd + r'TSS\\' +tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSS.hdr'
# with open(header_tss, 'r') as f:
#     tss_file = f.readlines()
#
#     line = tss_file[20].split(" = ")
#     dates = line[0][:-2]
#     dates_lst = dates.split(", ")
#
#     line = tss_file[25].split(" = ")
#     sensors = line[0][:-2]
#     sensors_lst = sensors.split(", ")
# dates_lst = [float(i) for i in dates_lst]
#
# header_tsi = wd + r'TSS\\' + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSI.hdr'
# with open(header_tsi, 'r') as f:
#     tsi_file = f.readlines()
#     line = tsi_file[20].split(" = ")
#     dates = line[0][:-2]
#     dates_lst_tsi = dates.split(", ")
# dates_lst_tsi = [float(i) for i in dates_lst_tsi]
#
#
# def plotTimeSeries(x,y, title):
#     slice_tss = arr_tss[:, y, x]
#     slice_tss = slice_tss / 10000.0
#     slice_tss[slice_tss == -3.2767] = np.nan
#     slice_tsi = arr_tsi[:,y,x]
#     slice_tsi = slice_tsi / 10000.0
#     slice_tsi[slice_tsi == -3.2767] = np.nan
#     dss = arr_dss[ y, x]
#     #dss = dss - (4 * 365-1)
#     dss_x = dss/366
#     dss_frac = 2018 + dss_x
#
#     dri = arr_dri[y, x]
#     #dri = dri - (4 * 365 - 1)
#     dri_x = dri / 366
#     dri_frac = 2018 + dri_x
#
#     dps = arr_dps[y, x]
#     #dps = dps - (4 * 365 - 1)
#     dps_x = dps / 366
#     dps_frac = 2018 + dps_x
#
#     dfi = arr_dfi[y, x]
#     #dfi = dfi - (4 * 365 - 1)
#     dfi_x = dfi / 366
#     dfi_frac = 2018 + dfi_x
#
#     des = arr_des[y, x]
#     #des = des - (4 * 365 - 1)
#     des_x = des / 366
#     des_frac = 2018 + des_x
#
#     lgs = arr_lgs[y, x]
#     igs = arr_igs[y, x]
#     igs = igs/10000
#
#     plt.rcParams.update({'font.size':14})
#     fig, ax = plt.subplots(figsize=(10, 5))
#     legend_elements = [Line2D([0], [0], color='C0', lw=2, label='RBF-Interpolation'),
#                        Line2D([0], [0], marker='o', color='grey', alpha=0.5, label='Satellite observation',
#                               markerfacecolor='black', markersize=5, linestyle='None')]
#                        # Line2D([0], [0], color='red', lw=2, label='Day of Start of Season'),
#                        # Line2D([0], [0], color='orange', lw=2, label='Day of Peak of Season'),
#                        # Line2D([0], [0], color='yellow', lw=2, label='Day of End of Season')]
#
#
#     ax.scatter(dates_lst, slice_tss, color='grey', alpha=0.5)
#     #ax.scatter(dss_frac, 0.6, marker='x', color='red', s=30)
#     ax.axvline(x=dss_frac, ymin=0.18, ymax=1, color='black', ls = '--')
#     ax.axvline(x=dri_frac, ymin=0.12, ymax=1, color='black', ls = '--')
#     ax.axvline(x=dps_frac, ymin=0.18, ymax=1, color='black', ls = '--')
#     ax.axvline(x=dfi_frac, ymin=0.12, ymax=1, color='black', ls = '--')
#     ax.axvline(x=des_frac, ymin=0.18, ymax=1, color='black', ls = '--')
#
#     ax.plot(dates_lst_tsi, slice_tsi)
#
#     ax.annotate('DSS\n' + str(dss), xy=(dss_frac-0.05, 0.09), fontsize=11, color='black')
#     ax.annotate('DRI\n' + str(dri), xy=(dri_frac-0.05, 0.01), fontsize=11, color='black')
#     ax.annotate('DPS\n' + str(dps), xy=(dps_frac-0.05, 0.09), fontsize=11, color='black')
#     ax.annotate('DFI\n' + str(dfi), xy=(dfi_frac-0.05, 0.01), fontsize=11, color='black')
#     ax.annotate('DES\n' + str(des), xy=(des_frac-0.05, 0.09), fontsize=11, color='black')
#
#     ax.annotate('LGS: ' + str(lgs), xy=(2020.0, 0.80), fontsize=13, color='black')
#     ax.annotate('IGS: ' + str(igs), xy=(2020.0, 0.75), fontsize=13, color='black')
#
#     ax.axvspan(2018.0, 2019.0, color='C2', alpha=0.2)
#     ax.legend(handles=legend_elements,loc='lower right')
#     ax.set_ylabel('NDVI')
#     ax.set_ylim(0,1)
#     ax.set_xlim(2017,2020.5)
#     ax.title.set_text(title + ' -- x={0} y={1}'.format(x,y))
#     fig.show()
#     return fig
#
# f1 = plotTimeSeries(x=514,y=472, title= 'Ex01 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex01-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=533,y=466, title= 'Ex02 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex02-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=545,y=466, title= 'Ex03 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex03-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=710,y=374, title= 'Ex04 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex04-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=749,y=365, title= 'Ex05 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex05-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=131,y=255, title= 'Ex06 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex06-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=561,y=23, title= 'Ex07 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex07-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=562,y=25, title= 'Ex08 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex08-'+seg+'Segments-5DayInterp-' + tile_name + '.png')
#
# f1 = plotTimeSeries(x=78,y=177, title= 'Ex09 -- '+seg+' Segments -- 5_Day Interp -- ' + tile_name)
# f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v2\'Ex09-'+seg+'Segments-5DayInterp-' + tile_name + '.png')

#################################################################################################

tile_name = 'X0067_Y0045'
wd = r'Y:\germany-drought\level4\\'

################################################################################
ras_tss = gdal.Open(wd + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSS.tif')
arr_tss = ras_tss.ReadAsArray()

ras_tsi = gdal.Open(wd + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSI.tif')
arr_tsi = ras_tsi.ReadAsArray()

ras_dss = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DSS.tif')
arr_dss = ras_dss.ReadAsArray()

ras_dps = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DPS.tif')
arr_dps = ras_dps.ReadAsArray()

ras_des = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DES.tif')
arr_des = ras_des.ReadAsArray()

ras_dfi = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DFI.tif')
arr_dfi = ras_dfi.ReadAsArray()

ras_dri = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DRI.tif')
arr_dri = ras_dri.ReadAsArray()

ras_lgs = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_LGS.tif')
arr_lgs = ras_lgs.ReadAsArray()

ras_igs = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_IGS.tif')
arr_igs = ras_igs.ReadAsArray()

ras_vss = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_VSS.tif')
arr_vss = ras_vss.ReadAsArray()

ras_vps = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_VPS.tif')
arr_vps = ras_vps.ReadAsArray()

ras_ves = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_VES.tif')
arr_ves = ras_ves.ReadAsArray()

ras_vfi = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_VFI.tif')
arr_vfi = ras_vfi.ReadAsArray()

ras_vri = gdal.Open(wd + tile_name + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_VRI.tif')
arr_vri = ras_vri.ReadAsArray()

header_tss = wd + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSS.hdr'
with open(header_tss, 'r') as f:
    tss_file = f.readlines()

    line = tss_file[20].split(" = ")
    dates = line[0][:-2]
    dates_lst = dates.split(", ")

    line = tss_file[25].split(" = ")
    sensors = line[0][:-2]
    sensors_lst = sensors.split(", ")
dates_lst = [float(i) for i in dates_lst]

header_tsi = wd + tile_name + r'\2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FAVG_TM_C95T_TSI.hdr'
with open(header_tsi, 'r') as f:
    tsi_file = f.readlines()
    line = tsi_file[20].split(" = ")
    dates = line[0][:-2]
    dates_lst_tsi = dates.split(", ")
dates_lst_tsi = [float(i) for i in dates_lst_tsi]

############################################################################################

title= '     lowVCI'

def plotTimeSeries(x,y, title):
    slice_tss = arr_tss[:, y, x]
    slice_tss = slice_tss / 10000.0
    slice_tss[slice_tss == -3.2767] = np.nan
    slice_tsi = arr_tsi[:,y,x]
    slice_tsi = slice_tsi / 10000.0
    slice_tsi[slice_tsi == -3.2767] = np.nan
    dss = arr_dss[4, y, x]
    dss = dss - (4 * 365-1)
    dss_x = dss/366
    dss_frac = 2018 + dss_x

    dri = arr_dri[4, y, x]
    dri = dri - (4 * 365 - 1)
    dri_x = dri / 366
    dri_frac = 2018 + dri_x

    dps = arr_dps[4, y, x]
    dps = dps - (4 * 365 - 1)
    dps_x = dps / 366
    dps_frac = 2018 + dps_x

    dfi = arr_dfi[4, y, x]
    dfi = dfi - (4 * 365 - 1)
    dfi_x = dfi / 366
    dfi_frac = 2018 + dfi_x

    des = arr_des[4, y, x]
    des = des - (4 * 365 - 1)
    des_x = des / 366
    des_frac = 2018 + des_x

    lgs = arr_lgs[4, y, x]
    igs = arr_igs[4, y, x]
    igs = igs/10000

    vss = arr_vss[4, y, x]/10000
    vri = arr_vri[4, y, x]/10000
    vps = arr_vps[4, y, x]/10000
    vfi = arr_vfi[4, y, x]/10000
    ves = arr_ves[4, y, x]/10000

    plt.rcParams.update({'font.size':14})
    fig, ax = plt.subplots(figsize=(10, 5))
    legend_elements = [Line2D([0], [0], color='C0', lw=2, label='RBF-Interpolation'),
                       Line2D([0], [0], marker='o', color='grey', alpha=0.5, label='Satellite observation',
                              markerfacecolor='black', markersize=5, linestyle='None')]
                       # Line2D([0], [0], color='red', lw=2, label='Day of Start of Season'),
                       # Line2D([0], [0], color='orange', lw=2, label='Day of Peak of Season'),
                       # Line2D([0], [0], color='yellow', lw=2, label='Day of End of Season')]


    ax.scatter(dates_lst, slice_tss, color='grey', alpha=0.5)

    # ax.axvline(x=dss_frac, ymin=0.18, ymax=1, color='black', ls = '-')
    # ax.axvline(x=dri_frac, ymin=0.12, ymax=1, color='black', ls = '-')
    # ax.axvline(x=dps_frac, ymin=0.18, ymax=1, color='black', ls = '-')
    # ax.axvline(x=dfi_frac, ymin=0.12, ymax=1, color='black', ls = '-')
    # ax.axvline(x=des_frac, ymin=0.18, ymax=1, color='black', ls = '-')

    ax.axvline(x=2018.0, ymin=0.0, ymax=1, color='black', alpha=0.4, ls='-')
    ax.axvline(x=2019.0, ymin=0.0, ymax=1, color='black', alpha=0.4, ls = '-')

    ax.plot(dates_lst_tsi, slice_tsi)

    bbox_props = dict(boxstyle="square,pad=0.2", fc="white")
    ax.annotate('DSS ' + str(dss), xy=(dss_frac+0.03, vss), fontsize=11, color='black',
            bbox=bbox_props)
    ax.annotate('DRI ' + str(dri), xy=(dri_frac+0.03, vri), fontsize=11, color='black',
            bbox=bbox_props)
    ax.annotate('DPS ' + str(dps), xy=(dps_frac+0.03, vps), fontsize=11, color='black',
            bbox=bbox_props)
    ax.annotate('DFI ' + str(dfi), xy=(dfi_frac+0.03, vfi), fontsize=11, color='black',
            bbox=bbox_props)
    ax.annotate('DES ' + str(des), xy=(des_frac+0.03, ves), fontsize=11, color='black',
            bbox=bbox_props)

    ax.annotate('LGS: ' + str(lgs), xy=(2020.0, 0.80), fontsize=13, color='black',
            bbox=bbox_props)
    ax.annotate('IGS: ' + str(igs), xy=(2020.0, 0.75), fontsize=13, color='black',
            bbox=bbox_props)

    ax.scatter(dss_frac, vss, marker='o', color='black')
    ax.scatter(dri_frac, vri, marker='o', color='black')
    ax.scatter(dps_frac, vps, marker='o', color='black')
    ax.scatter(dfi_frac, vfi, marker='o', color='black')
    ax.scatter(des_frac, ves, marker='o', color='black')

    ax.axvspan(2018.584, 2018.665, color='C2', alpha=0.2)
    ax.legend(handles=legend_elements,loc='lower right')
    ax.set_ylabel('NDVI')
    ax.set_ylim(0,1)
    ax.set_xlim(2017,2020.5)
    ax.title.set_text(title + '    x={0} y={1}'.format(x,y))
    fig.show()
    return fig

f1 = plotTimeSeries(x=282,y=276, title=  tile_name + '     low VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex01-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=494,y=211, title= tile_name + '     medium VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex02-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=758,y=864, title= tile_name + '     low VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex03-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=156,y=912, title= tile_name + '     low VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex04-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=847,y=742, title= tile_name + '     medium VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex05-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=919,y=954, title= tile_name + '     medium VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex06-8Segments-' + tile_name + '.png')

f1 = plotTimeSeries(x=919,y=947, title= tile_name + '     low VCI')
f1.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\ts_v3\'Ex07-8Segments-' + tile_name + '.png')


# #positve DSS
# #x=787,y=406
# #x=760,y=395
# #x=526,y=593
# #x=161,y=693
#
# #negative DSS
# #(x=258,y=257
# # x=58,y=185
# #x=149,y=178
# #x=22,y=136
# #x=160,y=693
#
# slice_tss = arr_tss[:,185, 58]
# slice_tss = arr_tss[:,406, 787]
# slice_tss = arr_tss[:,138, 147]
# slice_dates = np.array(dates_lst)
# doy_frac_slice = slice_dates - np.floor(slice_dates)
# doy_slice = np.round(doy_frac_slice * 365)
#
# ts_show = np.empty((203,2))
# ts_show[:,0] = slice_dates
# ts_show[:,1] = slice_tss
#
# ts_df = pd.DataFrame(ts_show)
# ts_df['DOYDate'] = doy_slice
#
#
#
def doyToStr(frac_doy):
    doy = frac_doy * 365
    doy = round(doy)
    doy = int(doy)

    date_str = '2018 {0}'.format(doy)

    # datetime.datetime(2018, 1, 1) + datetime.timedelta(186 - 1)
    d = datetime.datetime.strptime(date_str, '%Y %j')
    date = d.strftime('%d/%m/%Y')

    return date

doyToStr(.584)
doyToStr(.665)

