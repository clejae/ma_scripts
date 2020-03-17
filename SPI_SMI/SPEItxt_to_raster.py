import gdal
import numpy as np

def convertStrToList(strng, delimiter):
    lst = list(strng.split(delimiter))
    return lst

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

spei = 24

ref_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\monthly_aggr\DIFF_ts_05_03_3035.tif"
ref_ras = gdal.Open(ref_pth)

gt = ref_ras.GetGeoTransform()
pr = ref_ras.GetProjection()

arr_lst = []
for r in range(666):
    in_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\diff_p-pet\spei_as_txt\{0:02d}\SPEI{0:02d}-2018_row{1:03d}.txt".format(spei,r)

    file = open(in_pth, 'r')

    line_lst = [line.rstrip('\n') for line in open(in_pth)]
    line_lst = [i.replace(" ",",") for i in line_lst]
    line_lst = [i.replace("NA", "-3.2767") for i in line_lst]
    line_lst = [convertStrToList(i,",") for i in line_lst]

    arr = np.array(line_lst)
    arr = arr.astype(float)
    arr = arr * 10000

    arr_lst.append(arr)

fin_arr = np.array(arr_lst)
fin_arr_sw = fin_arr.swapaxes(0,2)
fin_arr_sw = fin_arr_sw.astype(int)

out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\SPEI{0:02d}-2018.tif'.format(spei)
writeArrayToRaster(fin_arr_sw, out_pth, gt, pr, -32767)