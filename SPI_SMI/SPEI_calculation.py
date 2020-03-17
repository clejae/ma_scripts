
############################################ PACKAGES ############################################
import gdal
import numpy as np
import math
import glob

############################################ FUNCTIONS ############################################

def writeRasterInt(in_array, out_path, gt, pr, no_data_value):

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Int16)
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

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Int16)
        out_ras.SetGeoTransform(gt)
        out_ras.SetProjection(pr)

        band = out_ras.GetRasterBand( 1)
        band.WriteArray(in_array)
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        del (out_ras)

def StackRasterFromList(rasterList, outputPath):
    """
    Stacks the first band of n raster that are stored in a list
    rasterList - list containing the rasters that have the same dimensions and Spatial References
    outputPath - Path including the name to which the stack is written
    """

    import gdal

    input_ras_gt = rasterList[0].GetGeoTransform()

    # set output raster definitions
    x_min = input_ras_gt[0]
    y_max = input_ras_gt[3]
    x_max = x_min + input_ras_gt[1] * rasterList[0].RasterXSize
    y_min = y_max + input_ras_gt[5] * rasterList[0].RasterYSize
    x_res = rasterList[0].RasterXSize
    y_res = rasterList[0].RasterYSize
    pixel_width_x = input_ras_gt[1]
    pixel_width_y = input_ras_gt[5]

    target_ds = gdal.GetDriverByName('GTiff').Create(outputPath, x_res, y_res, len(rasterList), gdal.GDT_Float32)
    target_ds.SetGeoTransform((x_min, pixel_width_x, 0, y_max, 0, pixel_width_y))
    target_ds.SetProjection(rasterList[0].GetProjection())

    for i in range(0, len(rasterList)):
        band = target_ds.GetRasterBand(i + 1)
        band.WriteArray(rasterList[i].GetRasterBand(1).ReadAsArray())
        NoData_value = -999
        band.SetNoDataValue(NoData_value)
        band.FlushCache()

    del(target_ds)

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

############################################ GLOBAL VARIABLES ############################################

months_lst = ['01','02','03','04','05','06','07','08','09','10','11','12']

############################################ PROCESSING ############################################
#
# ##---------------------------------# Calculate difference between precip and evapo_p #---------------------------------#
#
# for year in range(2019,2020):
#     for month in months_lst[:]:
#
#         prp_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\{0}\RSMS_{0}_{1}_01.tif'.format(month,year)
#         pet_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_evapo_p\download\grids_germany_monthly_evapo_p_{1}{0}.tif'.format(month,year)
#
#         ras_prp = gdal.Open(prp_pth)
#         ras_pet = gdal.Open(pet_pth)
#
#         gt = ras_prp.GetGeoTransform()
#         pr = ras_prp.GetProjection()
#
#         arr_prp = ras_prp.ReadAsArray()
#         arr_pet = ras_pet.ReadAsArray()
#
#         arr_dif = arr_prp - arr_pet / 10
#         arr_dif[ras_prp == -999] = -999
#         arr_dif[arr_pet == -9999] = -999
#
#         out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\{0}\P-PET-DIFF_{1}{0}.tif'.format(month,year)
#
#         writeRasterInt(arr_dif, out_pth, gt, pr, -999)
#
# ##----------------------------------------------# Stack monthly raster #----------------------------------------------#
# ## --> ..., June 2017, June 2018
#
#
# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\\'
# for month in months_lst:
#
#     wd_temp = wd + month + r'\\*.tif'
#     ras_path_list = glob.glob(wd_temp)
#     ras_list = []
#     for ras_path in ras_path_list:
#         ras = gdal.Open(ras_path)
#         ras_list.append(ras)
#
#     out_pth =r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\stacks\DIFF_stack_{0}.tif'.format(month)
#
#     stack = StackRasterFromList(ras_list, out_pth)
#
#     del(stack)
#
# ##------------------------------------------- create complete time series #-------------------------------------------#
# # --> ..., Jan 2018, Feb 2018, ..., Apr 2019
#
# wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\\'
#
# pth_lst = []
#
# for year in range(1991,2019):
#     for month in months_lst:
#         if year == 2019 and month == '09':
#             break
#         else:
#             pth = wd + r'{0}\P-PET-DIFF_{1}{0}.tif'.format(month,year)
#             pth_lst.append(pth)
#
# ras_list = [gdal.Open(file) for file in pth_lst]
#
# out_pth =r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018.tif'
#
# stack = StackRasterFromList(ras_list, out_pth)
#
# del(stack)
#
# ##--------------------------------------# reproject time series raster to 3035 #--------------------------------------#
#
# out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_3035.tif'
# in_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018.tif'
#
# repr = gdal.Warp(out_pth, in_pth, dstSRS='EPSG:3035')
# del repr
#
# ##---------------------# Calculate running sum of monthly difference between precip and evapo_p #---------------------#
#
# ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_3035.tif')
#
# month_lst = [3,6,12,24]
# #month_lst = [6]
#
# for n_months in month_lst:
#     print("-------------------------------------------------------------------------------------------------------")
#     print("Start calculating running sum over", n_months, "months.\n")
#
#     if n_months < 10:
#         output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_0' + str(n_months) + '_3035.tif'
#     else:
#         output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_' + str(n_months) + '_3035.tif'
#
#     print('Output path:', output_path)
#     arr = ras.ReadAsArray()
#
#     nbands_orig = ras.RasterCount
#     x_res = ras.RasterXSize
#     y_res = ras.RasterYSize
#
#     gt = ras.GetGeoTransform()
#     pr = ras.GetProjection()
#
#     nbands = nbands_orig - n_months + 1
#
#     arr_list = []
#
#     for arr_i in range(nbands):
#         arr_sub = arr[arr_i: arr_i + n_months, :, :]
#         arr_sum = np.sum(arr_sub, axis=0) # np.sum
#         arr_sum[arr_sub[0,:,:] == -999] = -9999
#         arr_list.append(arr_sum)
#
#     arr_running_sum = np.array(arr_list)
#
#     running_sum_ds = writeRasterInt(arr_running_sum,output_path,gt,pr,-9999)
#
#     del(running_sum_ds)
#
#     print("Calculating running sum over", n_months, "months finished.\n")
#
#     #### 2. Reorder complete time series to monthly ordered time series
#
#     print("Start reordering running sum time series to monthly ordered time series.\n")
#
#     lookup_sub = ['01','02','03','04','05','06','07','08','09','10','11','12']*10
#
#     lookup_arr = np.array([lookup_sub[i:i+27] for i in range(12)])
#
#     for m in range(1,13):
#         month_str = lookup_arr[m - 1, n_months - 1]
#         print("Running sum months:", n_months, "| i:", m , "| Month:", month_str)
#         monthly_arr_list = []
#         j = m - 1
#         year = 1990
#
#         while j < nbands:
#             year = year + 1
#             #print("Year", year, "J:", j)
#             arr_sub = arr_running_sum[j, :, :]
#             monthly_arr_list.append(arr_sub)
#             j = j + 12
#
#         arr_ordered = np.array(monthly_arr_list)
#
#         month_str = lookup_arr[m-1 ,n_months-1]
#
#         if n_months < 10:
#             output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\monthly_aggr\DIFF_ts_' + month_str + '_0' + str(n_months) + '_3035.tif'
#         else:
#             output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\monthly_aggr\DIFF_ts_' + month_str + '_' + str(n_months) + '_3035.tif'
#
#         print("Shape of ordered array:", arr_ordered.shape)
#
#         nbands_out = arr_ordered.shape[0]
#         x_res = arr_ordered.shape[2]
#         y_res = arr_ordered.shape[1]
#
#         gt = ras.GetGeoTransform()
#         pr = ras.GetProjection()
#
#         ordered_ds = writeRasterInt(arr_ordered, output_path, gt, pr, -9999)
#
#         del(ordered_ds)
#
#         print( m, "of 12 months done.")
#
#     print("\nReordering of all time series with running sum of",n_months,"done!")

##---------------------# export raster to txt files with each row representing one file #---------------------#
ts_norm_ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_3035.tif")
ts_norm_arr = ts_norm_ras.ReadAsArray()

for x in range(666):
    print(str(round((x/666) * 100,3)) + ' %')
    lst = []
    for y in range(874):
        s = ts_norm_arr[:,y,x]
        s= list(s)
        lst.append(s)
    file = open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\ts as txt\D-ts_1991-2018_row{0:03d}.txt'.format(x), 'w+')
    for i in range(len(lst)):
        line = str(lst[i])
        line = line.replace("[","")
        line = line.replace("]", "")
        file.write(line + "\n")
    file.close()


##---------------------# calculate SPEI on example time series #---------------------#

ts_norm_ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_3035.tif")

ts_norm6_ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\time_series\DIFF_ts_1991-2018_06_3035.tif")
ts_month_ras = gdal.Open(r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\monthly_aggr\DIFF_ts_06_06_3035.tif")

ts_norm_arr = ts_norm_ras.ReadAsArray()
ts_norm6_arr = ts_norm6_ras.ReadAsArray()
ts_month_arr = ts_month_ras.ReadAsArray()
ts_norm_arr.shape # x = 666, y = 874

# y = 9, x = 190

slice_norm = ts_norm_arr[:,9,190]
slice_norm6 = ts_norm6_arr[:,9,190]
slice_month = ts_month_arr[:,9,190]

ts = slice_month

# calculate spei

from scipy.stats import gamma
import math
import numpy as np

# define no-data value
no_data_value = -999

# count occurences of 0 and no_data_value
unique, counts = np.unique(ts, return_counts=True)
count_dict = dict(zip(unique, counts))
m = 0
if no_data_value in ts:
    m = count_dict[no_data_value]

num_years = ts.shape[0]

n = num_years - m

ts_ordered = np.sort(ts)
ts_i = np.array(range(1,n+1))

inner_w0 = (1 - (ts_i - 0.35)/n)**0
w0 = sum(ts_ordered * inner_w0) / n
inner_w1 = (1 - (ts_i - 0.35)/n)**1
w1 = sum(ts_ordered * inner_w1) / n
inner_w2 = (1 - (ts_i - 0.35)/n)**2
w2 = sum(ts_ordered * inner_w2) / n

beta = (2*w1 - w0) / (6*w1 - w0 - 6*w2)
alpha = ((w0 - 2*w1) * beta) / math.gamma(1 + 1/beta)* math.gamma(1-1/beta)
gamm = w0 - alpha* math.gamma(1 + 1/beta) * math.gamma(1-1/beta)

def fx(x):
    (1+ (alpha/(x-gamm)**beta))**-1

c0 = 2.515517
c1 = 0.802853
c2 = 0.010328
d1 = 1.432788
d2 = 0.189269
d3 = 0.001308


# Jan           Feb           Mar           Apr           May           Jun           Jul           Aug           Sep           Oct           Nov
# 1             NA            NA            NA            NA            NA  0.7540761954 -0.0802103783  0.0305510222 -0.4517298306 -0.7689742729 -0.5453168688
# 2  -0.9973928718 -1.1585466017 -0.6581427632 -0.1488489990 -1.0564645664 -1.8366784614 -1.6834444011 -1.5853941120 -1.6276678866 -1.1103430777 -0.0287264301
# 3   1.3943181488  1.3834876970  1.5397392118  0.8246216588 -0.4963934244 -0.8534218432 -0.9928363564 -0.4470418876  0.2616502051  0.3088862470  0.3720464536
# 4   0.8046285180  0.9674457731  1.3342536520  1.7935472788  1.6834739557  1.4583320133 -0.0613738362  0.3608846074  0.5953578149  0.6042816837  0.1067043047
# 5   1.6940639948  1.6410658467  1.3898729896  1.7254721705  1.9234427297  2.1456951096  0.5818787085 -0.6343409883 -0.1582405714 -0.7153083819 -1.1891990082
# 6  -1.4981735310 -1.3253456402 -2.2648521667 -2.1039832170 -1.7618087547 -1.3391981305 -0.9563051722 -1.3843356095 -1.2409102951 -0.9747345674 -1.0524102858
# 7  -1.3784319756 -1.2261293370 -0.9531578640 -0.9436794669 -0.4149314707 -0.2204305573  0.5149373812 -0.9785601547 -1.1856443844 -1.1103430777 -1.6794330392
# 8  -1.4590402037 -1.1243236025 -0.8805161163  0.1442832785  0.5788944807  0.5652696219  0.8582903769  0.2628770657  0.3782380538  0.3602519125  0.5392297292
# 9  -0.1846973269  0.6555411039  1.2312435466  0.3700096306  0.5788944807  1.2366393464  1.0982517138  0.6562430146  0.7945551073  1.0334605928  0.8368340294
# 10  1.1637551711  1.5149045478  1.0510184749  1.2501168821  1.4565344259  0.3182276723  0.4928282574 -0.3229017286 -0.6259911509 -0.5716844532  0.1817215128
# 11 -0.1000732556  0.8020985876  1.2659996868  1.4471643638  0.2568998086  0.4425267533  0.6270059926  0.9105200515  1.5107173040  0.9589112858  1.0558854740
# 12  0.7933006412  0.9091183527 -0.1851079441  0.3510861488  0.9229363656  1.1129997845  2.1762955731  1.6756188866  0.7945551073  1.0086793944  1.1326785533
# 13 -0.1425587348 -0.2672664886  0.1353253427 -0.6727589060 -0.5784424512  0.0308205528 -0.0802103783 -0.8426961347 -0.5597309913 -0.5941590472 -1.0435747779
# 14 -0.8117989735  0.0232139659  0.1504014688  0.1070493576  0.5139503132  0.8212978003  0.0542635095 -0.1395651916 -0.0001744687 -0.0340979388 -0.0651321633
# 15 -0.6774294271 -0.6291453219 -0.6881383011 -0.5768049984 -0.2145682757 -0.3972965364  0.6954228086  0.3805380358 -0.2574756076 -0.7689742729 -0.8209396102
# 16 -1.3577764322 -1.5264245467 -1.1659692556 -0.6251304942 -0.1165483990 -0.7055785446 -1.2981114172 -0.2867728614 -1.0368776296 -0.7368809349 -0.6916017193
# 17  1.0635664707  0.9674457731  1.5707686486  0.7869485847  1.1343190051  1.1129997845  1.7609852539  0.2433404243  0.1595905061  0.0539042203 -0.6193650146
# 18 -1.2874161420 -1.3144490732 -0.7775178122 -0.3596116522 -0.9103988792 -1.4916078125 -1.5667584413 -0.1952516693 -0.5060263691  0.2704110907  0.9272456721
# 19  0.8612003045 -0.2541224092 -0.1390441451 -1.4003542274 -1.3065804709 -0.9808234512 -0.6470683969 -0.5504244434 -0.8311060928 -0.3871610524 -0.0892661962
# 20 -0.1107262994  0.2600087862  0.4314582665  0.3700096306  0.3449196419 -0.3269252485  0.4489240642  1.6756188866  1.5230890919  1.4429501872  1.1964076091
# 21  0.3850418020 -0.4499446940 -0.9386944198 -1.6771653594 -2.0909053976 -1.5051077407 -0.2964572248  1.2358091435  1.2432917006  1.3130227905  0.5392297292
# 22  0.1501028363 -0.6669734146 -1.0817993406 -0.8856768492 -0.1360221323  0.0668489772  0.2986760174  1.4035603832  1.6329803447  1.8945162917  2.0585200299
# 23  1.0635664707  0.6307111728  0.0748027545 -0.6727589060  0.1114310045  0.1928323221 -0.6026036889 -1.0795684417  0.2616502051  0.2319939794  0.3720464536
# 24  0.2167334943  1.0249487503  0.1654540400  0.0146265638 -0.3542867575 -0.5189661337 -1.1311703944  0.0688977526 -0.1153598262  0.2192036672 -0.4474824024
# 25  0.5322168288 -0.2672664886  0.4169635203 -0.2729022608  1.2081859686  0.2466757215  0.6270059926  1.4035603832  0.8645867374  0.3602519125  0.3337144231
# 26  0.1390447243 -0.1750744871 -0.4000115297  0.5976773766 -0.0971427972  0.0308205528 -0.2791259261 -0.4818214462 -0.8311060928 -1.3871204554 -1.0435747779
# 27 -1.4258392297 -1.3253456402 -0.8805161163 -0.3767509307 -0.4963934244  0.5652696219  0.7879517986  0.5971901881  1.2823893486  1.2891302143  1.4485453067
# 28  0.9851497675  0.9558458680  0.3878638658  0.7680838680 -0.3542867575 -0.9808234512 -1.8441213717 -2.1510761158 -1.9793276407 -2.2740414273 -2.0407078548
#              Dec
# 1  -1.0674811804
# 2   0.7249740139
# 3   1.1578360700
# 4   0.2756158321
# 5  -1.4920106640
# 6  -1.1251481517
# 7  -1.4635387082
# 8   0.2142446414
# 9   1.3655552954
# 10 -0.0909360269
# 11  0.8719253169
# 12  0.5027797652
# 13 -1.1671633221
# 14 -0.4210478293
# 15 -0.8824065895
# 16  0.0119260146
# 17 -0.9540151126
# 18  0.9936823768
# 19  0.2142446414
# 20  1.0072866026
# 21  1.0072866026
# 22  1.6608653359
# 23 -0.2766910303
# 24  0.1778143909
# 25  0.5156613050
# 26 -1.3687154010
# 27  0.9258835175
# 28 -1.7359336474