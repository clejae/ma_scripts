import ogr
import gdal
import numpy as np
import time
# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)

bund_pth = r"O:\Student_Data\CJaenicke\00_MA\data\vector\stratification_germany\DE_Bundeslaender_3035.shp"
tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'

bund_shp = ogr.Open(bund_pth)
bund_lyr = bund_shp.GetLayer()

tiles_shp = ogr.Open(tiles_pth)
tiles_lyr = tiles_shp.GetLayer()

for feat in bund_lyr:

    bund_name = feat.GetField('GEN')

    geom = feat.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()
    tiles_lyr.SetSpatialFilter(geom)

    tiles_lst = []
    for tile in tiles_lyr:
        tile_name = tile.GetField('Name')
        tile_vci = r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\\2018_BL-2000-2018_VCI.tif'
        tiles_lst.append(tile_vci)
    print(tiles_lst)

    tiles_lyr.ResetReading()

    vrt = gdal.BuildVRT(r'O:\Student_Data\CJaenicke\00_MA\data\vrt\bundeslaender\{0}_2018_BL-2000-2018_VCI.vrt'.format(bund_name), tiles_lst)
    del (vrt)