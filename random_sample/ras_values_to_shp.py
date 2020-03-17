import ogr, osr
import gdal
import numpy
import time
import pandas as pd

start = time.time()

with open('Y:/germany-drought/germany.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_01.shp')
lyr = shp.GetLayer()

output_df = pd.DataFrame()
out_lst = [["ID","DEM"]]

# tile = tiles_lst[100]
for tile in tiles_lst:

    print(tile)

    ras = gdal.Open(r'Y:\germany-drought\level4_analysis\\' + tile + r'\COMP-2014-2017-TO-2018_DEM.tif')

    arr = ras.ReadAsArray()

    gt = ras.GetGeoTransform()

    x_min = gt[0]
    x_max = gt[0] + gt[1] * ras.RasterXSize
    y_max = gt[3]
    y_min = gt[3] + gt[5] * ras.RasterYSize

    lyr.SetSpatialFilterRect(x_min, y_min, x_max, y_max)

    print("Num points in tile:", lyr.GetFeatureCount())

    for feat in lyr:

        point_id = feat.GetField("ID")
        geom = feat.geometry().Clone()
        x_coord, y_coord = geom.GetX(), geom.GetY()
        x_index = int((x_coord - gt[0]) / gt[1])
        y_index = int((y_coord - gt[3]) / gt[5])

        dem = arr[y_index, x_index]
        sub_lst = [point_id, dem]

        output_df['ID'] = point_id
        output_df['DEM'] = dem

        out_lst.append(sub_lst)

    lyr.SetSpatialFilter(None)

end = time.time()