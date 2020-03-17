import ogr
import gdal
import numpy as np
import time
import joblib

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)

wuchs_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\stratification_germany\wuchsgebiete\wuchsgebiete_germany_3035.shp'
tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\VPI_2018_wuchsgebiete_BL_2013-2018.csv'

wuchs_shp_outer = ogr.Open(wuchs_pth)
wuchs_lyr_outer = wuchs_shp_outer.GetLayer()

no_data_val = -32767

id_lst = []
for feat in wuchs_lyr_outer:
    wuchs_name = feat.GetField('Name')
    wuchs_id = feat.GetField('ID')
    id_lst.append(wuchs_id)
wuchs_lyr_outer.ResetReading()

arr_lst = []

file = open(out_pth, 'w+')
col_name_lst = ['ID', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
for i in range(len(col_name_lst)):
    if i < len(col_name_lst) - 1:
        file.write(str(col_name_lst[i]) + ",")
    elif i == len(col_name_lst) - 1:
        file.write(str(col_name_lst[i]) + "\n")
file.close()

feat_count = wuchs_lyr_outer.GetFeatureCount()

# def workFunc(i):
for i in range(feat_count):
    wuchs_shp = ogr.Open(wuchs_pth)
    tiles_shp = ogr.Open(tiles_pth)

    wuchs_lyr = wuchs_shp.GetLayer()
    tiles_lyr = tiles_shp.GetLayer()

    sr = wuchs_lyr.GetSpatialRef()

    feat = wuchs_lyr.GetFeature(i)

    wuchs_name = feat.GetField('Name')
    wuchs_name = wuchs_name.replace("/", "-")
    wuchs_id = feat.GetField('ID')
    print(wuchs_id, wuchs_name)

    tiles_lyr.SetSpatialFilter(None)
    geom = feat.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()
    tiles_lyr.SetSpatialFilter(geom)

    tiles_lst = []
    for tile in tiles_lyr:
        tile_name = tile.GetField('Name')
        tiles_lst.append(tile_name)
    print(tiles_lst)

    tiles_lyr.ResetReading()

    vrt_msk_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{1}_{0}_MASK_FOREST-BROADLEAF.vrt'.format(wuchs_name,
                                                                                                  wuchs_id)
    vrt_msk = gdal.Open(vrt_msk_pth)
    arr_msk = vrt_msk.ReadAsArray()

    # create memory layer for rasterization
    driver_mem = ogr.GetDriverByName('Memory')
    ogr_ds = driver_mem.CreateDataSource('wrk')
    ogr_lyr = ogr_ds.CreateLayer('poly', srs=sr)

    feat_mem = ogr.Feature(ogr_lyr.GetLayerDefn())
    feat_mem.SetGeometryDirectly(ogr.Geometry(wkt=geom_wkt))

    ogr_lyr.CreateFeature(feat_mem)

    # rasterize geom
    col = vrt_msk.RasterXSize
    row = vrt_msk.RasterYSize

    gt = vrt_msk.GetGeoTransform()

    target_ds = gdal.GetDriverByName('MEM').Create('', col, row, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(gt)

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(-9999)

    gdal.RasterizeLayer(target_ds, [1], ogr_lyr, burn_values=[1])

    arr_geom = target_ds.ReadAsArray()
    arr_msk_geom = arr_msk * arr_geom

    file_lst = [
        r'Y:\germany-drought\VCI_VPI\{0}\2018_BL-2013-2018_VPI.tif'.format(t)
        for t in tiles_lst]
    vrt_ind_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vrt\wuchsgebiete\VPI\{1}_{0}_VPI_2018_BL-2013-2018.vrt'.format(
        wuchs_name,wuchs_id)

    vrt_ind = gdal.BuildVRT(vrt_ind_pth, file_lst)
    arr_ind = vrt_ind.ReadAsArray()

    n_months = arr_ind.shape[0]

    f = open(out_pth, "a+")

    out_lst = []
    out_lst.append(wuchs_id)
    for month in range(n_months):
        arr_sub = arr_ind[month, :, :]

        arr_sub[arr_msk_geom == 0] = -32767  # no data value FORCE -32767
        arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_sub[arr_sub == -32767] = np.nan

        mean_st = np.nanmean(arr_sub)
        out_lst.append(mean_st)

    for i in range(len(out_lst)):
        if i < len(out_lst) - 1:
            f.write(str(out_lst[i]) + ",")
        elif i == len(out_lst) - 1:
            f.write(str(out_lst[i]) + "\n")
    f.close()

    del (vrt_ind)
    del (vrt_msk)

    print(wuchs_id, wuchs_name, 'done.')

# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in range(feat_count))

print('Done')

# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")