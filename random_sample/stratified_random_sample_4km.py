import gdal
import ogr
import math
import numpy as np
import joblib

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

shp_grd = ogr.Open(r"O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\4km_grid.shp")
lyr_grd = shp_grd.GetLayer()

ras = gdal.Open(r'Y:\germany-drought\vrt\masks\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.vrt')
gt = ras.GetGeoTransform()
pr = ras.GetProjection()
x_ref = gt[0]
y_ref = gt[3]

# feat = lyr_grd.GetFeature(22274)
feat_count = lyr_grd.GetFeatureCount()
arr = ras.ReadAsArray()

coord_lst = []
coord_lst_txt = []

for feat in lyr_grd:
# def workFunc(i):
    #print(i)


    # feat = lyr_grd.GetFeature(i)
    geom = feat.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()

    extent = geom.GetEnvelope()

    x_min_ext = extent[0]
    x_max_ext = extent[1]
    y_min_ext = extent[2]
    y_max_ext = extent[3]

    dist_x = x_ref - x_min_ext
    steps_x = -(math.floor(dist_x / 30))
    x_min_ali = x_ref + steps_x * 30  # - 30

    dist_x = x_ref - x_max_ext
    steps_x = -(math.floor(dist_x / 30))
    x_max_ali = x_ref + steps_x * 30  # + 30

    dist_y = y_ref - y_min_ext
    steps_y = -(math.floor(dist_y / 30))
    y_min_ali = y_ref + steps_y * 30  # - 30

    dist_y = y_ref - y_max_ext
    steps_y = -(math.floor(dist_y / 30))
    y_max_ali = y_ref + steps_y * 30  # + 30

    # slice input raster array to common dimensions
    px_min = int((x_min_ali - gt[0]) / gt[1])
    px_max = int((x_max_ali - gt[0]) / gt[1])

    py_max = int((y_min_ali - gt[3]) / gt[
        5])  # raster coordinates count from S to N, but array count from Top to Bottum, thus pymax = ymin
    py_min = int((y_max_ali - gt[3]) / gt[5])

    geom_arr = arr[py_min: py_max, px_min: px_max]

    if np.sum(geom_arr) >= 1:

        coord_ind_lst = equalSampleFromArray(geom_arr, [0.5, 1.5], 1)

        for sub_lst in coord_ind_lst:
            y_index = sub_lst[0]
            x_index = sub_lst[1]

            x_coord = x_index * gt[1] + x_min_ali
            y_coord = y_index * gt[5] + y_max_ali

            coord_lst.append((y_coord, x_coord))
            coord_lst_txt.append((y_index, x_index, y_coord, x_coord))
    else:
        pass
    print(i, r'/', feat_count, 'done')

lyr_grd.ResetReading()
with open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_stratified_4km.txt', "w+") as file:
    file.write("y_index, x_index, y_coord, x_coord\n")
    for item in coord_lst_txt:
        for i in range(len(item)):
            if i < len(item)-1:
                file.write(str(item[i])+", ")
            else:
                file.write(str(item[i]))
        file.write("\n")
file.close()


#
# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in range(feat_count))