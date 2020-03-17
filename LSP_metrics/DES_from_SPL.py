import gdal
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def getDateList(ras):
    import gdal
    import re

    options = gdal.InfoOptions(allMetadata=True)
    info = gdal.Info(ras, options=options)
    out_lst = re.findall('Date=(.*)T', info)
    return out_lst

def dateListToDoyList(date_lst, appendYear):
    import datetime

    if appendYear == False:
        doy_lst = []
        for i in date_lst:
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            doy = date_time.strftime('%j')
            doy_lst.append(doy)
    elif appendYear == True:
        doy_lst = []
        for i in date_lst:
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            doy = date_time.strftime('%Y-%j')
            doy_lst.append(doy)

    return doy_lst

def dateListToFracDoyList(date_lst, appendYear):
    import datetime

    if appendYear == False:
        doy_lst = []
        for i in date_lst:
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            doy = date_time.strftime('%j')
            frac_doy = int(doy) / 365
            doy_lst.append(frac_doy)
    elif appendYear == True:
        doy_lst = []
        for i in date_lst:
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            doy = date_time.strftime('%j')
            frac_doy = int(doy) / 365
            year = date_time.strftime('%Y')
            frac_doy_year = int(year) + frac_doy
            doy_lst.append(frac_doy_year)

    return doy_lst

def dateListToYearList(date_lst):
    import datetime
    year_lst = []
    for i in date_lst:
        date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
        year = date_time.strftime('%Y')
        year_lst.append(year)
    return year_lst

def writeArrayToRaster(in_array, out_path, gt, pr, no_data_value):

    import gdal
    from osgeo import gdal_array

    type_code = gdal_array.NumericTypeCodeToGDALTypeCode(in_array.dtype)

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, type_code)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        for b in range(0, nbands_out):
            band = out_ras.GetRasterBand(b + 1)
            arr_out = in_array[b, :, :]
            band.WriteArray(arr_out)
            band.SetNoDataValue(no_data_value)
            band.FlushCache()

        del (out_ras)

    if len(in_array.shape) == 2:
        nbands_out = 1
        x_res = in_array.shape[1]
        y_res = in_array.shape[0]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        band = out_ras.GetRasterBand( 1)
        band.WriteArray(in_array)
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        del (out_ras)

pth_spl = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_SPL.tif"
ras_spl = gdal.Open(pth_spl)
arr_spl = ras_spl.ReadAsArray()
del pth_spl
thresh = 0.4

gt = ras_spl.GetGeoTransform()
pr = ras_spl.GetProjection()

date_lst = getDateList(ras_spl)
doy_lst = dateListToFracDoyList(date_lst, appendYear=True)
doy_arr = np.array(doy_lst[100:160])

def calcDES(spl_ts, doy_ts, thresh):
    ts = spl_ts[100:160]
    rng_ts = np.max(ts) - np.min(ts)
    thresh_val = np.min(ts) + rng_ts * thresh
    f2 = interp1d(ts, doy_arr, kind='linear')
    if thresh_val >= np.min(ts) and thresh_val <= np.max(ts):
        des = f2(thresh_val)
    else:
        des = -32767
    return(des)

des_arr = np.apply_along_axis(arr= arr_spl, axis=0, func1d=calcDES, doy_ts = doy_arr, thresh = thresh)
des_doy_arr = (des_arr - 2016) * 366
des_doy_arr = des_doy_arr.astype(int)

writeArrayToRaster(des_doy_arr, out_path=r'Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_DES-LSP_calc.tif', gt = gt, pr = pr, no_data_value= -32767)



# pth_vbl = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_VBL-LSP.tif"
# ras_vbl = gdal.Open(pth_vbl)
# arr_vbl = ras_vbl.ReadAsArray()
#
# pth_vps = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_VPS-LSP.tif"
# ras_vps = gdal.Open(pth_vps)
# arr_vps = ras_vps.ReadAsArray()
#
# des_pth = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_DES-LSP.tif"
# des_ras = gdal.Open(des_pth)
# des_arr = des_ras.ReadAsArray()
# rng_arr = arr_vps - arr_vbl
# thresh_arr = arr_vbl + rng_arr*thresh
# arr_spl.shape
# fill_arr = np.empty(shape=thresh_arr.shape)
# for x in range(1000):
#     for y in range(1000):
#         ts = arr_spl[100:160, y, x]
#         f2 = interp1d(ts, doy_arr, kind='linear')
#         curr_max = np.max(ts)
#         curr_min = np.min(ts)
#         curr_val = thresh_arr[y,x]
#         if curr_val >= curr_min and curr_val <= curr_max:
#             des = f2(curr_val)
#         else:
#             des = -32767
#         fill_arr[y,x] = des

# t0 = arr_spl[110:160, 0, 0]
# f2 = interp1d(t0, doy_lst, kind='cubic')
# t1 = arr_spl[110:160, 1, 0]
# f2 = interp1d(t1, doy_lst, kind='cubic')
# t2 = arr_spl[110:160, 2, 0]
# f2 = interp1d(t2, doy_lst, kind='linear')


# plt.plot( doy_arr_r, t2_r, '-')
# plt.show()

### EXAMPLE CALCULATION

# pth_spl = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_SPL.tif"
# ras_spl = gdal.Open(pth_spl)
# arr_spl = ras_spl.ReadAsArray()
#
# pth_vbl = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_VBL-LSP.tif"
# ras_vbl = gdal.Open(pth_vbl)
# arr_vbl = ras_vbl.ReadAsArray()
#
# pth_vps = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_VPS-LSP.tif"
# ras_vps = gdal.Open(pth_vps)
# arr_vps = ras_vps.ReadAsArray()
#
# des_pth = r"Y:\germany-drought\level4\X0052_Y0045\2015-2017_001-365_LEVEL4_TSA_LNDLG_NDV_DES-LSP.tif"
# des_ras = gdal.Open(des_pth)
# des_arr = des_ras.ReadAsArray()


# date_lst = getDateList(ras)
# doy_lst = dateListToDoyList(date_lst, appendYear=False)
# year_lst = dateListToYearList(date_lst)
#
# doy_lst_2016 = []
# for i, year in enumerate(year_lst):
#     if year == '2016':
#         doy_lst_2016.append(doy_lst[i])
#
#
#
# y = 325
# x = 562
# ex_des = des_arr[y,x] # DES 335
# ex_spl = arr_spl[:,y,x]
# ex_vbl = arr_vbl[y,x]
# ex_vps = arr_vps[y,x]
#
# calc_range = ex_vps - ex_vbl
# calc_t040 = ex_vbl + 0.4 * calc_range # 6470.6
#
# ex_spl_lst = list(ex_spl)
#
# ex_spl_lst_2016 = []
# for i, year in enumerate(year_lst):
#     if year == '2016':
#         ex_spl_lst_2016.append(ex_spl_lst[i])
#
# for i, item in enumerate(doy_lst_2016):
#     print(item, ex_spl_lst_2016[i])

# date_lst = getDateList(ras_spl)
# doy_lst = dateListToFracDoyList(date_lst, appendYear=True)
# doy_lst = doy_lst[110:160]
#
# y = 325
# x = 562
# ex_spl = arr_spl[110:160,y,x]
# f2 = interp1d(ex_spl, doy_lst, kind='cubic')
#
# plt.plot(doy_lst, ex_spl, 'o',f2(ex_spl),ex_spl, '-')
# plt.plot(f2(6470.6), 6470.6, 'o', ms = 10)
# plt.show()
