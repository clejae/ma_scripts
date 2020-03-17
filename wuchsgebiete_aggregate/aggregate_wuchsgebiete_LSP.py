import ogr
import gdal
import pandas as pd
import numpy as np
import time

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

wuchs_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\stratification_germany\wuchsgebiete\wuchsgebiete_germany_3035.shp'
tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'

abr_lst = ['DSS','DES','DPS','DRI','DFI']

for abr in abr_lst:

    wuchs_shp = ogr.Open(wuchs_pth)
    tiles_shp = ogr.Open(tiles_pth)

    wuchs_lyr = wuchs_shp.GetLayer()
    tiles_lyr = tiles_shp.GetLayer()

    sr = wuchs_lyr.GetSpatialRef()

    id_lst = []
    for feat in wuchs_lyr:
        wuchs_name = feat.GetField('Name')
        wuchs_id = feat.GetField('ID')
        id_lst.append(wuchs_id)
    wuchs_lyr.ResetReading()

    out_df = pd.DataFrame(index=id_lst, columns=range(2014,2019))

    for feat in wuchs_lyr:
        wuchs_name = feat.GetField('Name')
        wuchs_name = wuchs_name.replace("/","-")
        wuchs_id = feat.GetField('ID')
        print(abr, wuchs_id, wuchs_name)

        tiles_lyr.SetSpatialFilter(None)
        geom = feat.GetGeometryRef()
        geom_wkt = geom.ExportToWkt()
        tiles_lyr.SetSpatialFilter(geom)

        tiles_lst = []
        for tile in tiles_lyr:
            tile_name = tile.GetField('Name')
            tiles_lst.append(tile_name)
            print(tile_name)

        tiles_lyr.ResetReading()
        print('\n')

        # msk_lst = [r'Y:\germany-drought\masks\{0}\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'.format(i) for i in tiles_lst]
        # vrt_msk_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{1}_{0}_MASK_FOREST-BROADLEAF.vrt'.format(wuchs_name, wuchs_id)
        # vrt_msk = gdal.BuildVRT(vrt_msk_pth, msk_lst)
        # del vrt_msk
        # print('Load Mask Arrays')
        vrt_msk_pth =  r'Y:\germany-drought\vrt\wuchsgebiete\{1}_{0}_MASK_FOREST-BROADLEAF.vrt'.format(wuchs_name, wuchs_id)
        vrt_msk = gdal.Open(vrt_msk_pth)
        arr_msk = vrt_msk.ReadAsArray()

        # print('Rasterize current feat')
        # create memory layer for rasterization
        driver_mem = ogr.GetDriverByName('Memory')
        ogr_ds = driver_mem.CreateDataSource('wrk')
        ogr_lyr = ogr_ds.CreateLayer('poly', srs=sr)

        feat_mem = ogr.Feature(ogr_lyr.GetLayerDefn())
        feat_mem.SetGeometryDirectly(ogr.Geometry(wkt=geom_wkt))

        ogr_lyr.CreateFeature(feat_mem)

        # rasterize geom with oversampling factor 100
        col = vrt_msk.RasterXSize
        row = vrt_msk.RasterYSize

        gt = vrt_msk.GetGeoTransform()

        target_ds = gdal.GetDriverByName('MEM').Create('', col, row, 1, gdal.GDT_Byte)
        target_ds.SetGeoTransform(gt)

        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(-9999)

        gdal.RasterizeLayer(target_ds, [1], ogr_lyr, burn_values=[1])

        # print('Load geom array and calculate statistics')
        arr_geom = target_ds.ReadAsArray()
        arr_msk_geom = arr_msk * arr_geom

        file_lst = [r'Y:\germany-drought\level4\{0}\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_{1}.tif'.format(i,abr) for i in tiles_lst]
        vrt_ind_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{1}_{0}_2013-2019-{2}.vrt'.format(wuchs_name,
                                                                                                     wuchs_id,
                                                                                                    abr)

        vrt_ind = gdal.BuildVRT(vrt_ind_pth, file_lst)

        for year in range(2014,2019):
            print(abr, year)
            b_ind = year - 2013
            # for year in range(5,6):
            ras_sub = vrt_ind.GetRasterBand(b_ind)
            arr_sub = ras_sub.ReadAsArray()
            #n_months = arr_ind.shape[0]

            #  arr_sub = arr_ind[month,:,:]

            arr_sub[arr_msk_geom == 0] = -32767  # no data value FORCE -32767
            arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
            arr_sub[arr_sub == -32767.0] = np.nan

            mean_st = np.nanmean(arr_sub)

            out_df.at[wuchs_id, year] = mean_st

        print('--------------------------------------------\n')
        del (vrt_ind)
        del (vrt_msk)

    wuchs_lyr.ResetReading()


    col_name_lst = ['ID', '_2014','_2015','_2016','_2017','_2018']
    out_df.index.name = 'ID'
    out_df.reset_index(inplace=True)
    out_df.columns = col_name_lst
    out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\{1}_2014-2018_wuchsgebiete.csv'.format(year,abr)
    out_df.to_csv(out_name, index=False, decimal=".", sep=",")

    print(abr, 'done!')

print('Script done')

# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")