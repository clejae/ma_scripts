import gdal
import osr
import glob
import numpy as np


##### --------------------------- extract array, give projection and save to geotiff ---------------------------
folder_lst = glob.glob(r'Y:\germany-drought\VCI_Copernicus\*')

folder = folder_lst[0]

for folder in folder_lst:

    print(folder)

    file_lst = glob.glob(folder + '\*.h5')

    in_pth = file_lst[0]
    for in_pth in file_lst:

        print(in_pth)

        hdf = gdal.Open(in_pth)
        info = gdal.Info(hdf)

        # get latitude value for building gt
        try:
            start = info.index("LAT=") + len("LAT=") # index of last character if this string
            end = info.index("\n", start) # index of first appearance of given character after start index
            lat = float(info[start:end]) # string between these two indices
        except ValueError:
            print("Error")

        # get longitude value for building gt
        try:
            start = info.index("LONG=") + len("LONG=") # index of last character if this string
            end = info.index("\n", start) # index of first appearance of given character after start index
            lon = float(info[start:end]) # string between these two indices
        except ValueError:
            print("Error")

        # # get scaling factor to calculate physical values
        # try:
        #     start = info.index("VCI_SCALING_FACTOR=") + len("VCI_SCALING_FACTOR=")  # index of last character if this string
        #     end = info.index("\n", start)  # index of first appearance of given character after start index
        #     sf = float(info[start:end])  # string between these two indices
        # except ValueError:
        #     print("Error")
        sf = 0.005

        # # get offset to calculate physical values
        # try:
        #     start = info.index("VPI_OFFSET=") + len(
        #         "VPI_OFFSET=")  # index of last character if this string
        #     end = info.index("\n", start)  # index of first appearance of given character after start index
        #     offset = float(info[start:end])  # string between these two indices
        # except ValueError:
        #     print("Error")
        offset = -0.125

        # get projection by EPSG code
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        # create new gt
        gt_new = (lon, 1/112, 0.0, lat, 0.0, -1/112)

        # read array from hdf file
        arr = hdf.ReadAsArray()
        arr = arr.astype(np.int16)

        # set clouds, snow, background etc. to no data value
        arr[arr == 251] = -999
        arr[arr == 252] = -999
        arr[arr == 253] = -999
        arr[arr == 254] = -999
        arr[arr == 255] = -999

        # calculate physical values and set no data value (again)
        arr_bool = np.where(arr == -999 ,0, 1)
        arr_pv = arr * sf + offset
        arr_pv[arr_bool == 0] = -999

        # write array to geotiff
        out_pth = in_pth[:-2] + "tif"

        x_res = arr_pv.shape[1]
        y_res = arr_pv.shape[0]

        tiff = gdal.GetDriverByName("GTiff").Create(out_pth, x_res, y_res, 1, gdal.GDT_Float32)
        tiff.SetProjection(srs.ExportToWkt())
        tiff.SetGeoTransform(gt_new)

        band = tiff.GetRasterBand(1)
        band.WriteArray(arr_pv)
        band.SetNoDataValue(-999)
        band.FlushCache()

        del(tiff)
        del(hdf)
        #del(tiff_rep)

##### --------------------------- reproject to 3035 and clip to extent of Germany ---------------------------
import gdal
import ogr
import glob
import numpy as np



folder_lst = glob.glob(r'Y:\germany-drought\VCI_Copernicus\*')

shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035_extent.shp')
lyr = shp.GetLayer()

feat = lyr.GetNextFeature()
geom = feat.geometry()

ext = geom.GetEnvelope()

folder = folder_lst[0]



for folder in folder_lst:

    print(folder)

    file_lst = glob.glob(folder + '\g2_BIOPAR_VCI_2*0.tif')

    file = file_lst[0]
    for file in file_lst:
        print(file)

        ds = gdal.Warp(file[:-4] + '_3035.tif', file, dstSRS='EPSG:3035')
        del(ds)

        ras = gdal.Open(file[:-4] + '_3035.tif')
        arr = ras.ReadAsArray()

        gt = ras.GetGeoTransform()

        x_min_ext, x_max_ext, y_min_ext, y_max_ext = ext[0], ext[1], ext[2], ext[3]

        # slice input raster array to common dimensions
        px_min = int((x_min_ext - gt[0]) / gt[1])
        px_max = int((x_max_ext - gt[0]) / gt[1])

        py_max = int((y_min_ext - gt[3]) / gt[5])  # raster coordinates count from S to N, but array count from T to B, thus pymax = ymin
        py_min = int((y_max_ext - gt[3]) / gt[5])

        geom_arr = arr[py_min: py_max, px_min: px_max]

        output_name = file[:-21] + '_clip.tif'

        # write arr img to disc
        output_ds = gdal.GetDriverByName('ENVI').Create(output_name, geom_arr.shape[1], geom_arr.shape[0], 1,gdal.GDT_Float32)

        output_ds.SetGeoTransform((x_min_ext, gt[1], 0, y_max_ext, 0, gt[5]))
        output_ds.SetProjection(ras.GetProjection())

        band = output_ds.GetRasterBand(1)
        band.WriteArray(geom_arr)
        band.SetNoDataValue(-999)
        band.FlushCache()
        del (output_ds)


print("\nDone!")

##### --------------------------- move file and delete rest of folder ---------------------------

import gdal
import os
import glob
import numpy as np

folder_lst = glob.glob(r'Y:\germany-drought\VCI_Copernicus\*')

#folder = folder_lst[0]

for folder in folder_lst:

    print(folder)

    file_lst = glob.glob(folder + '\*clip.tif')
    hdr_lst = glob.glob(folder + '\*clip.hdr')
    #file= file_lst[0]

    for file in file_lst:
        print(file)
        os.rename(file, r'Y:\germany-drought\VCI_Copernicus\\' + file[-35:])

    for file in hdr_lst:
        print(file)
        os.rename(file, r'Y:\germany-drought\VCI_Copernicus\\' + file[-35:])

#### --------------------------- calculate monthly mean and clip to extent of germany ---------------------------

import gdal
import numpy as np
import glob
import ogr

#year_int = 2017
for year_int in range(2017,2019):

    year_str = str(year_int)

    month_str_lst = ['01','02','03','04','05','06','07','08','09','10','11','12']

    month_str = '01'
    for month_str in month_str_lst:

        print(year_str, month_str)

        ras_pth_lst = glob.glob(r'Y:\germany-drought\VCI_Copernicus\g2_BIOPAR_VCI_' + year_str + month_str +'*.tif')

        ras_lst = []
        arr_lst = []
        no_data_value = -999

        #ras_pth = ras_pth_lst[0]
        for ras_pth in ras_pth_lst:

            ras = gdal.Open(ras_pth)
            ras_lst.append(ras)

            arr = ras.ReadAsArray()

            gt = ras.GetGeoTransform()

            arr[arr == no_data_value] = np.nan
            arr_lst.append(arr)

        num_arr = len(arr_lst)

        mean_arr = np.nanmean(arr_lst, axis = 0)


        pr = ras_lst[0].GetProjection()

        output_name = r'Y:\germany-drought\VCI_Copernicus\g2_BIOPAR_VCI_' + year_str + month_str +'.tif'

        x_res = mean_arr.shape[1]
        y_res = mean_arr.shape[0]

        target_ds = gdal.GetDriverByName('GTiff').Create(output_name, x_res, y_res, 1, gdal.GDT_Float32)
        target_ds.SetGeoTransform(gt)
        target_ds.SetProjection(pr)

        band = target_ds.GetRasterBand(1)
        band.WriteArray(mean_arr)
        band.SetNoDataValue(-999)
        band.FlushCache()

        del target_ds
