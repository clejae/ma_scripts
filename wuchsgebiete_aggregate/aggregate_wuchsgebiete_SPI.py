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

#l = [[2017,'VCI'],[2019,'VCI'],[2017,'VPI'],[2018,'VPI'],[2019,'VPI'],[2018,'SPI06'],[2018,'SPI12']]

l = [[2018,'SPI03'],[2018,'SPI06'],[2018,'SPI12'],[2018,'SPI24']]
for xyz in l:

    year = xyz[0]
    abr = xyz[1]

    wuchs_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\stratification_germany\wuchsgebiete\wuchsgebiete_germany_3035.shp'
    tiles_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp'

    if abr[0:3] == 'SPI':
        no_data_val = -999
    if abr[0:3] == 'VCI' or abr[0:3] == 'VPI':
        no_data_val = -32767

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

    out_df = pd.DataFrame(index=id_lst, columns=range(1, 13))

    for feat in wuchs_lyr:
        wuchs_name = feat.GetField('Name')
        wuchs_id = feat.GetField('ID')
        print(abr, year, wuchs_id, wuchs_name)

        tiles_lyr.SetSpatialFilter(None)
        geom = feat.GetGeometryRef()
        geom_wkt = geom.ExportToWkt()
        tiles_lyr.SetSpatialFilter(geom)

        tiles_lst = []
        for tile in tiles_lyr:
            tile_name = tile.GetField('Name')
            tiles_lst.append(tile_name)
            #print(tile_name)

        tiles_lyr.ResetReading()
        print(tiles_lst)

        msk_lst = [r'Y:\germany-drought\masks\{0}\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'.format(i) for i in tiles_lst]
        vrt_msk_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_MASK_FOREST-BROADLEAF.vrt'.format(wuchs_name, wuchs_id)
        vrt_msk = gdal.BuildVRT(vrt_msk_pth, msk_lst)
        #print('Load Mask Arrays')
        arr_msk = vrt_msk.ReadAsArray()

        #print('Rasterize current feat')
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

        print('Load geom array and calculate statistics')
        arr_geom = target_ds.ReadAsArray()
        arr_msk_geom = arr_msk * arr_geom

        if abr[:3] == 'SPI':
            file_lst = [r'Y:\germany-drought\SPI\{0}\{1}_{2}.tif'.format(i, abr, year) for i in tiles_lst]
            vrt_ind_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_{2}_{3}.vrt'.format(wuchs_name,wuchs_id,abr,year)
        elif abr[:3] == 'VPI' or  abr[:3] == 'VCI':
            file_lst = [r'Y:\germany-drought\VCI_VPI\{0}\{2}_BL-2013-2019_{1}.tif'.format(i, abr, year) for i in tiles_lst]
            vrt_ind_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_{2}_{3}.vrt'.format(wuchs_name,wuchs_id,abr, year)

        vrt_ind = gdal.BuildVRT(vrt_ind_pth, file_lst)
        arr_ind = vrt_ind.ReadAsArray()
        n_months = arr_ind.shape[0]

        for month in range(n_months):
            arr_sub = arr_ind[month,:,:]

            arr_sub[arr_msk_geom == 0] = no_data_val  # no data value FORCE -32767
            arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
            arr_sub[arr_sub == no_data_val] = np.nan

            if abr[:3] == 'VCI':
                arr_sub[arr_sub < -15.0] = -15.0
                arr_sub[arr_sub > 100.0] = 100.0

            mean_st = np.nanmean(arr_sub)

            out_df.at[wuchs_id,month+1] = mean_st

        print('--------------------------------------------\n')
        del (vrt_ind)
        del (vrt_msk)
    wuchs_lyr.ResetReading()

    col_name_lst = ['ID', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
    out_df.index.name = 'ID'
    out_df.reset_index(inplace=True)
    out_df.columns = col_name_lst

    out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\{0}_{1}_wuchsgebiete.csv'.format(abr,year)
    out_df.to_csv(out_name, index=False, decimal=".", sep=",")

print('Done')

# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")