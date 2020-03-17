import gdal
import numpy as np
import ogr, osr
import pandas as pd
import matplotlib.pyplot as plt

def equalSampleFromArray(arr, breaks_list, nsamples):
    '''
    This function enables the user to get an equal sized random sample in different strata from a two-dimensional array.
    Required input is an 2d array, a list containing the break values,
    starting with the minimum of the first stratum and ending with the maximum of the last stratum.
    Moreover, the number of desired samples per stratum is also required as input.

    :param arr: Input Array
    :param breaks_list: List indicating breaks e.g. 0,1,2 resulting in two strata (0-1,1-2)
    :param nsamples: Number of Samples
    :return:
    '''

    import numpy as np
    import math
    import random

    nbreaks = len(breaks_list)-1

    # empty list to store values to, which are created in the following loop
    coords_arr_list = []

    for i in range(0, nbreaks):

        # sub arr contains now all index values of position of cells within a certain stratum in the original input
        # array
        sub_arr = np.where((arr > breaks_list[i]) & (arr < breaks_list[i + 1] + 1))

        # in case that there are less cells which meet desired conditions than the number of samples for each stratum,
        # arrays have to be extented so that values can be drawn several times
        if len(sub_arr[0] < nsamples):

            # here, the factor is determined which should be used to extend the array with the pixel index values for
            # each stratum
            factor = math.ceil(nsamples / len(sub_arr[0]))
            y_arr = np.tile(sub_arr[0], factor)

            # the index object is a tuple with y and x index for pixels separated.
            # therefore, arrays need to be extended in each occasion
            x_arr = np.tile(sub_arr[1], factor)

        # if not, there is no need for array extension
        else:
            y_arr = sub_arr[0]
            x_arr = sub_arr[1]

        # here, the random samples are drawn. samples are not directly drawn
        # but only int numbers within the range of the index list. random numbers are written to a list.
        sample_id_list = [random.randint(0, len(y_arr) - 1) for sample_id in range(0, nsamples)]

        for k in range(0, len(sample_id_list)):

            # the randomly drawn index values are now used to extract y and x index values of the cells
            # in the target stratum
            y_val = y_arr[sample_id_list[k]]
            x_val = x_arr[sample_id_list[k]]
            coords_arr = [y_val, x_val]

            # finally, y and x values are merged to a tuple and passed on to a general list,
            # which is the only object returned by this function
            coords_arr_list.append(coords_arr)

    return coords_arr_list

ras = gdal.Open(r'Y:\germany-drought\vrt\masks\2015_MASK_FOREST-BROADLEAF_BUFF-01.vrt')

arr = ras.ReadAsArray()

gt = ras.GetGeoTransform()

coord_ind_lst = equalSampleFromArray(arr,[0.5,1.5],10000)

coord_lst = []
coord_lst_txt = []

for sub_lst in coord_ind_lst:

    y_index = sub_lst[0]
    x_index = sub_lst[1]

    x_coord = x_index * gt[1] + gt[0]
    y_coord = y_index * gt[5] + gt[3]

    coord_lst.append((y_coord, x_coord))
    coord_lst_txt.append((y_index, x_index, y_coord, x_coord))

with open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_02.txt', "w+") as file:
    file.write("y_index, x_index, y_coord, x_coord\n")
    for item in coord_lst_txt:
        for i in range(len(item)):
            if i < len(item)-1:
                file.write(str(item[i])+", ")
            else:
                file.write(str(item[i]))
        file.write("\n")
file.close()

# ##### -------------------- OPTIONAL: write list to shapefile --------------------
# driver = ogr.GetDriverByName("ESRI Shapefile")
# shp_out = driver.CreateDataSource(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_01.shp')
#
# srs = osr.SpatialReference()
# srs.ImportFromEPSG(3035)
#
# lyr = shp_out.CreateLayer('random_sample_01', srs, ogr.wkbPoint)
#
# field_id = ogr.FieldDefn("ID", ogr.OFTInteger)
# field_id.SetWidth(10)
# lyr.CreateField(field_id)
# lyr.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
# lyr.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
#
# i = 1
# for i, coord_tuple in enumerate(coord_lst):
#
#     point = ogr.Geometry(ogr.wkbPoint)
#     point.AddPoint(coord_tuple[1], coord_tuple[0])
#
#     feat = ogr.Feature(lyr.GetLayerDefn())
#     feat.SetField("ID", i)
#     feat.SetField("Latitude", coord_tuple[0])
#     feat.SetField("Longitude", coord_tuple[1])
#
#     feat.SetGeometry(point)
#
#     lyr.CreateFeature(feat)
#     del feat
#
# del shp_out

abr_lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']

output_df = pd.DataFrame()
#output_lst = [['ID','DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']]

abr = abr_lst[0]
for abr in abr_lst:

    print(abr)

    ras = gdal.Open(r'Y:/germany-drought/vrt/analysis/COMP-2014-2017-TO-2018_' + abr + '.vrt')
    arr = ras.ReadAsArray()


    for i, sub_lst in enumerate(coord_ind_lst):

        y_index = sub_lst[0]
        x_index = sub_lst[1]

        val = arr[y_index, x_index]

        output_df.at[i, abr] = val

    output_df.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_02_analysis_extract.csv', sep=",")

abr_lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']

output_df = pd.DataFrame()
#output_lst = [['ID','DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']]

abr = abr_lst[0]
for abr in abr_lst:

    print(abr)

    ras = gdal.Open(r'Y:/germany-drought/vrt/pheno-metrics/2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' + abr + '.vrt')
    arr = ras.ReadAsArray()


    for i, sub_lst in enumerate(coord_ind_lst):

        y_index = sub_lst[0]
        x_index = sub_lst[1]

        val = arr[y_index, x_index]

        output_df.at[i, abr] = val

output_df.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_02_pheno-metrics_extract.csv', sep=",")


