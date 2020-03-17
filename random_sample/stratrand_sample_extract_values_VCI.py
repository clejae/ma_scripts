import gdal
import ogr
import joblib
import time

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("Start time " + str(starttime))

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]

# for spei in [3,6,12,24]:
    # out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\tables\random_sample\SPI{0:02d}_2018.csv'.format(spei)
    # dir = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles'
    # file_name = r'SPI{0:02d}_2018.tif'.format(spei)

for file_name in [r'EVAPO_2018_int.tif',r'PRECIP_2018_v3_int.tif',r'TEMP_2018_int.tif']:
    if file_name == r'EVAPO_2018_int.tif':
        out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\tables\random_sample\EVAPO_2018.csv'
        dir = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_evapo_p\tiles'

    if file_name == r'PRECIP_2018_v3_int.tif':
        out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\tables\random_sample\PRECIP_2018.csv'
        dir = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\tiles'

    if file_name == r'TEMP_2018_int.tif':
        out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\tables\random_sample\TEMP_2018.csv'
        dir = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_temperature\tiles'
    # file_name = r'EVAPO_2018_int.tif'

    col_name_lst = ['ID', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']

    # out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\tables\random_sample\RAF_2018.csv'
    # dir = r'Y:\germany-drought\level4'
    # file_name = r'2017-2019_001-365_LEVEL4_TSA_LNDLG_NDV_RAF-LSP.tif'
    # col_name_lst = ['ID', 'RAF2018']

    file = open(out_pth, 'w+')
    for i in range(len(col_name_lst)):
        if i < len(col_name_lst) - 1:
            file.write(str(col_name_lst[i]) + ",")
        elif i == len(col_name_lst) - 1:
            file.write(str(col_name_lst[i])+ "\n")
    file.close()

    # for tile in tiles_lst:
    # def workFunc(tile):
    for tile in tiles_lst:
        ras = gdal.Open(r'{0}\{1}\{2}'.format(dir, tile, file_name))
        shp = ogr.Open(r"O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\stratrand_sample_4km.shp")
        lyr = shp.GetLayer()

        gt = ras.GetGeoTransform()

        x_min = gt[0]
        x_max = gt[0] + gt[1] * ras.RasterXSize
        y_max = gt[3]
        y_min = gt[3] + gt[5] * ras.RasterYSize

        lyr.SetSpatialFilterRect(x_min, y_min, x_max, y_max)

        feat_count = lyr.GetFeatureCount()
        if feat_count > 0:

            arr = ras.ReadAsArray()

            if len(arr.shape) == 3:
                n_months = arr.shape[0]

            for feat in lyr:
                point_id = feat.GetField('ID_point')

                geom = feat.geometry().Clone()
                x_coord, y_coord = geom.GetX(), geom.GetY()
                x_index = int((x_coord - gt[0]) / gt[1])
                y_index = int((y_coord - gt[3]) / gt[5])

                out_lst = []
                out_lst.append(point_id)
                if len(arr.shape) == 3:
                    for month in range(n_months):
                        if x_index > 999 or y_index > 999:
                            val = -32767
                        else:
                            val = arr[month, y_index, x_index]
                        out_lst.append(val)
                elif len(arr.shape) == 2:
                    if x_index > 999 or y_index > 999:
                        val = -32767
                    else:
                        val = arr[y_index, x_index]
                    out_lst.append(val)

                file = open(out_pth, "a+")
                for i in range(len(out_lst)):
                    if i < len(out_lst) - 1:
                        file.write(str(out_lst[i]) + ",")
                    elif i == len(out_lst) - 1:
                        file.write(str(out_lst[i]) + "\n")
                file.close()
            print(tile, "done")

        else:
            print("no points in ", tile,   r'{0}\{1}\{2}'.format(dir, tile, file_name) )

        lyr.SetSpatialFilter(None)

    # if __name__ == '__main__':
    #     joblib.Parallel(n_jobs=40)(joblib.delayed(workFunc)(i) for i in tiles_lst)

endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

print("Start time " + str(starttime))
print("End time " + str(endtime))