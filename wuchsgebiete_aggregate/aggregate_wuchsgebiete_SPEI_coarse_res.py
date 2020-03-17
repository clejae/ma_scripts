import ogr
import gdal
import pandas as pd
import numpy as np
import joblib
import time

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("Starting process, time: " + starttime)

spei = 6

wuchs_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\stratification_germany\wuchsgebiete\wuchsgebiete_germany_3035.shp'
tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'
out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\SPEI{0:02d}_2018_wuchsgebiete.csv'.format(spei)

wuchs_shp_outer = ogr.Open(wuchs_pth)
wuchs_lyr_outer = wuchs_shp_outer.GetLayer()

id_lst = []
for feat in wuchs_lyr_outer:
    wuchs_name = feat.GetField('Name')
    wuchs_id = feat.GetField('ID')
    id_lst.append(wuchs_id)
wuchs_lyr_outer.ResetReading()

out_df_2018 = pd.DataFrame(index=id_lst, columns=range(1, 13))

arr_lst = []

file = open(out_pth, 'w+')
col_name_lst = ['ID', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
for i in range(len(col_name_lst)):
    if i < len(col_name_lst) - 1:
        file.write(str(col_name_lst[i]) + ",")
    elif i == len(col_name_lst) - 1:
        file.write(str(col_name_lst[i])+ "\n")
file.close()

feat_count = wuchs_lyr_outer.GetFeatureCount()

def workFunc(i):
    wuchs_shp = ogr.Open(wuchs_pth)

    wuchs_lyr = wuchs_shp.GetLayer()

    sr = wuchs_lyr.GetSpatialRef()
    feat = wuchs_lyr.GetFeature(i)
    geom = feat.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()

    wuchs_name = feat.GetField('Name')
    wuchs_name = wuchs_name.replace("/","-")
    wuchs_id = feat.GetField('ID')
    print(wuchs_id, wuchs_name)

    # create memory layer for rasterization
    driver_mem = ogr.GetDriverByName('Memory')
    ogr_ds = driver_mem.CreateDataSource('wrk')
    ogr_lyr = ogr_ds.CreateLayer('poly', srs=sr)

    feat_mem = ogr.Feature(ogr_lyr.GetLayerDefn())
    feat_mem.SetGeometryDirectly(ogr.Geometry(wkt=geom_wkt))

    ogr_lyr.CreateFeature(feat_mem)

    ras_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\SPEI\SPEI{0:02d}-2018.tif".format(spei)
    ras = gdal.Open(ras_pth)

    # rasterize geom
    col = ras.RasterXSize
    row = ras.RasterYSize

    gt = ras.GetGeoTransform()

    target_ds = gdal.GetDriverByName('MEM').Create('', col, row, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(gt)

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(-32767)

    gdal.RasterizeLayer(target_ds, [1], ogr_lyr, burn_values=[1])

    arr_geom = target_ds.ReadAsArray()

    arr_ind = ras.ReadAsArray()

    n_months = arr_ind.shape[0]

    f = open(out_pth, "a+" )

    out_lst = []
    out_lst.append(wuchs_id)
    for month in range(n_months):
        arr_sub = arr_ind[month,:,:]

        arr_sub[arr_geom == 0] = -32767  # no data value FORCE -32767
        arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        arr_sub[arr_sub == -32767] = np.nan

        mean_st = np.nanmean(arr_sub)
        out_lst.append(mean_st)

    for i in range(len(out_lst)):
        if i < len(out_lst) -1 :
            f.write(str(out_lst[i]) + ",")
        elif i == len(out_lst) -1 :
            f.write(str(out_lst[i]) + "\n")
    f.close()

    del(target_ds)

    print(wuchs_id, wuchs_name, 'done.')

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(i) for i in range(feat_count))

print('\nProcessing done!')

# #### END TIME-COUNT AND PRINT TIME STATS #### #

endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

print("start: " + starttime)
print("end: " + endtime)
