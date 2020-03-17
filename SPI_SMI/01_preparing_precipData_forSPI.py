#### ------------------------------ PACKAGES ----------------------------- ####

import gdal
import numpy as np
import math

#### ------------------------------ PROCESSING ----------------------------- ####

#### 1. Calculate running mean

ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_1970-2018_3035.tif')

#n_months = 6
month_lst = [1,3,6,12,18,24,48]
#month_lst = [6]

for n_months in month_lst:
    print("-------------------------------------------------------------------------------------------------------")
    print("Start calculating running mean over", n_months, "months.\n")

    if n_months < 10:
        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_1970-2018_0' + str(n_months) + '_3035.tif'
    else:
        output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\time_series\RSMS_01-12_1970-2018_' + str(n_months) + '_3035.tif'

    print('Output path:', output_path)
    arr = ras.ReadAsArray()

    nbands_orig = ras.RasterCount
    x_res = ras.RasterXSize
    y_res = ras.RasterYSize

    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()

    nbands = nbands_orig - n_months + 1

    arr_list = []

    for arr_i in range(nbands):
        arr_sub = arr[arr_i: arr_i + n_months, :, :]
        arr_mean = np.mean(arr_sub, axis=0) # np.sum
        arr_mean[arr_mean < 0] = -999
        arr_list.append(arr_mean)

    arr_running_mean = np.array(arr_list)

    running_mean_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, nbands, gdal.GDT_Int16)
    running_mean_ds.SetGeoTransform(gt)
    running_mean_ds.SetProjection(pr)

    for band_i in range(0, nbands):
        band = running_mean_ds.GetRasterBand(band_i + 1)
        arr_out = arr_running_mean[band_i, :, :]
        band.WriteArray(arr_out)
        no_data_value = -999
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

    del(running_mean_ds)

    print("Calculating running mean over", n_months, "months finished.\n")

    #### 2. Reorder complete time series to monthly ordered time series


    print("Start reordering running mean time series to monthly ordered time series.\n")

    lookup_sub = ['01','02','03','04','05','06','07','08','09','10','11','12']*10

    lookup_arr = np.array([lookup_sub[i:i+48] for i in range(12)])

    for m in range(1,13):
        month_str = lookup_arr[m - 1, n_months - 1]
        print("Running mean months:", n_months, "| i:", m , "| Month:", month_str)
        monthly_arr_list = []
        j = m - 1
        year = 1969

        while j < nbands:
            year = year + 1
            #print("Year", year, "J:", j)
            arr_sub = arr_running_mean[j, :, :]
            monthly_arr_list.append(arr_sub)
            j = j + 12

        arr_ordered = np.array(monthly_arr_list)

        month_str = lookup_arr[m-1 ,n_months-1]

        if n_months < 10:
            output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\monthly\RSMS_' + month_str + '_0' + str(n_months) + '_3035.tif'
        else:
            output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\monthly\RSMS_' + month_str + '_' + str(n_months) + '_3035.tif'

        print("Shape of ordered array:", arr_ordered.shape)

        nbands_out = arr_ordered.shape[0]
        x_res = arr_ordered.shape[2]
        y_res = arr_ordered.shape[1]

        gt = ras.GetGeoTransform()
        pr = ras.GetProjection()

        ordered_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, nbands_out, gdal.GDT_Int16)
        ordered_ds.SetGeoTransform(gt)
        ordered_ds.SetProjection(pr)

        for b in range(0, nbands_out):
            band = ordered_ds.GetRasterBand(b + 1)
            arr_out = arr_ordered[b, :, :]
            band.WriteArray(arr_out)
            no_data_value = -999
            band.SetNoDataValue(no_data_value)
            band.FlushCache()

        del(ordered_ds)

        print( m, "of 12 months done.")

    print("\nReordering of all time series with running mean of",n_months,"done!")

print("\nScript done!")

#### ------------------------------ PACKAGES ----------------------------- ####

import gdal
import numpy as np
import math

#### ------------------------------ FUNCTIONS ----------------------------- ####

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def calculate_SPI(ts):
    from scipy.stats import gamma
    import math
    import numpy as np

    # define no-data value
    no_data_value = -999

    # count occurences of 0 and no_data_value
    unique, counts = np.unique(ts, return_counts=True)
    count_dict = dict(zip(unique, counts))
    m1 = 0
    m2 = 0
    if 0 in ts:
        m1 = count_dict[0]
    if no_data_value in ts:
        m2 = count_dict[no_data_value]

    num_years = ts.shape[0]

    obs_years = num_years - m2

    if obs_years > 30:

        # number of years with 0 or no-data value
        m = m1 + m2

        # 1. Calculate gamma function parameters alpha and beta
        # natural logarithm of time series
        ts_ma = np.ma.masked_where(ts == 0, ts)
        ts_log = np.log(ts_ma)

        # mean of time series
        ts_avg = np.mean(ts)

        # natural log of mean of time series
        ts_avg_log = np.log(ts_avg)

        # sum of natural log
        ts_log_sum = np.sum(ts_log)

        # some other parameter
        A = ts_avg_log - (ts_log_sum / (num_years - m))

        # alpha
        alpha = 1 / (4 * A) * (1 + math.sqrt(1 + (4 * A) / 3))

        # beta
        beta = ts_avg / alpha

        # 2. cummulative distribution function values for the precipitation values
        CDF = m / num_years + (1 - m / num_years) * gamma.cdf(ts, a=alpha, scale=beta)

        # 3. some t parameter for employing the approximate conversion by Abramowitz and Stegun (1965)
        t = np.ma.where(CDF <= .5, np.sqrt(np.log(1 / CDF ** 2)), np.sqrt(np.log(1 / (np.square(1 - CDF)))))

        # some parameters for this conversion
        c0 = 2.515517
        c1 = 0.802853
        c2 = 0.010328
        d1 = 1.432788
        d2 = 0.189269
        d3 = 0.001308

        # 4. the z-scores which are the SPI
        SPI = np.ma.where(CDF <= .5, -(t - ((c0 + c1 * t + c2 * t ** 2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3))),
                          t - ((c0 + c1 * t + c2 * t ** 2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3)))
    else:
        SPI = np.full(shape=(num_years), fill_value=no_data_value, dtype=np.float32)

    return SPI

#### ------------------------------ PROCESSING ----------------------------- ####

#### Calculate SPI

# list of running means
#month_lst = [1,2,3,4,5,6,12,18,24,48]
#month_lst = [6]

for n_months in month_lst:

    # list of months numbers in special order
    month_nums = [6,7,8,5,4,9,10,11,3,2,1,12]
    #month_nums = [6, 7, 8]

    for i in month_nums:

        if i < 10:
            if n_months < 10:
                ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\monthly\RSMS_0' + str(i) + '_0' + str(n_months) + '_3035.tif')
                output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_0' + str(n_months) + r'\\'
                output_file = 'SPI_0' + str(i) + '_0' + str(n_months) + '_3035.tif'
            else:
                ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\monthly\RSMS_0' + str(i) + '_' + str(n_months) + '_3035.tif')
                output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_' + str(n_months) + r'\\'
                output_file = 'SPI_0' + str(i) + '_' + str(n_months) + '_3035.tif'
        else:
            if n_months < 10:
                ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\monthly\RSMS_' + str(i) + '_0' + str(n_months) + '_3035.tif')
                output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_0' + str(n_months) + r'\\'
                output_file = 'SPI_' + str(i) + '_0' + str(n_months) + '_3035.tif'
            else:
                ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\RSMS\RSMS_' + str(i) + '_' + str(n_months) + '_3035.tif')
                output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_' + str(n_months) + r'\\'
                output_file = 'SPI_' + str(i) + '_' + str(n_months) + '_3035.tif'

        print('\nStart calculating SPI for:\n', output_path + output_file)

        arr = ras.ReadAsArray()

        SPI_arr = np.apply_along_axis(arr=arr, axis=0, func1d=calculate_SPI)


        # SPI_arr = SPI_arr * 1000
        SPI_arr = SPI_arr[-5:,:,:]

        print('Writing raster.')
        num_bands = SPI_arr.shape[0]
        input_ras_gt = ras.GetGeoTransform()

        # set output raster definitions
        x_min = input_ras_gt[0]
        y_max = input_ras_gt[3]
        x_max = x_min + input_ras_gt[1] * ras.RasterXSize
        y_min = y_max + input_ras_gt[5] * ras.RasterYSize
        x_res = ras.RasterXSize
        y_res = ras.RasterYSize
        pixel_width_x = input_ras_gt[1]
        pixel_width_y = input_ras_gt[5]

        createFolder(output_path)

        output_path_full = output_path + output_file

        SPI_ds = gdal.GetDriverByName('GTiff').Create(output_path_full, x_res, y_res, num_bands, gdal.GDT_Float32)
        SPI_ds.SetGeoTransform((x_min, pixel_width_x, 0, y_max, 0, pixel_width_y))
        SPI_ds.SetProjection(ras.GetProjection())

        for i in range(0, num_bands):
            band = SPI_ds.GetRasterBand(i + 1)
            annual_SPI_arr = SPI_arr[i,:,:]
            band.WriteArray(annual_SPI_arr)
            no_data_value = -999
            band.SetNoDataValue(no_data_value)
            band.FlushCache()

        del(SPI_ds)

        print('Done:', output_path)

    print("Done!")