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

for feat in wuchs_lyr:
    wuchs_name = feat.GetField('Name')
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
        print(tile_name)

    tiles_lyr.ResetReading()
    print('\n')

    msk_lst = [r'Y:\germany-drought\masks\{0}\2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif'.format(i) for i in tiles_lst]
    vrt_msk_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_MASK_FOREST-BROADLEAF.vrt'.format(wuchs_name, wuchs_id)
    vrt_msk = gdal.BuildVRT(vrt_msk_pth, msk_lst)
    print('Load Mask Arrays')
    arr_msk = vrt_msk.ReadAsArray()

    print('Rasterize current feat')
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

    #for year in range(2017,2020):
    for spi in ['03','06','12']:
        year = 2018
        print(year)

        # file_lst = [r'Y:\germany-drought\VCI_VPI\{0}\{1}_BL-2013-2019_VCI.tif'.format(i,year) for i in tiles_lst]
        # vrt_ind_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_{2}_BL-2013-2019_VCI.vrt'.format(wuchs_name,
        #                                                                                              wuchs_id,
        #                                                                                             year)

        file_lst = [r'Y:\germany-drought\SPI\{0}\SPI_01{1}_{2}.tif'.format(i, year, spi) for i in tiles_lst]
        vrt_ind_pth = r'Y:\germany-drought\vrt\wuchsgebiete\{0}{1}_{2}_SPI_{3}.vrt'.format(wuchs_name,wuchs_id,year,spi)

        vrt_ind = gdal.BuildVRT(vrt_ind_pth, file_lst)
        arr_ind = vrt_ind.ReadAsArray()
        n_months = arr_ind.shape[0]

        out_df = pd.DataFrame(index=id_lst, columns=range(1, n_months+1))

        # for month in range(n_months):
        #     arr_sub = arr_ind[month,:,:]
        #
        #     arr_sub[arr_msk_geom == 0] = -32767  # no data value FORCE -32767
        #     arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
        #     arr_sub[arr_sub == -32767.0] = np.nan
        #
        #     arr_sub[arr_sub < -15.0] = -15.0
        #     arr_sub[arr_sub > 100.0] = 100.0
        #
        #     mean_st = np.nanmean(arr_sub)
        #
        #     out_df.at[wuchs_id,month+1] = mean_st

        for month in range(n_months):
            arr_sub = arr_ind[month,:,:]

            arr_sub[arr_msk_geom == 0] = -32767  # no data value FORCE -32767
            arr_sub = arr_sub + 0.0  # small trick to convert data type of array to float, normal way didn't work somehow
            arr_sub[arr_sub == -32767.0] = np.nan

            arr_sub[arr_sub < -15.0] = -15.0
            arr_sub[arr_sub > 100.0] = 100.0

            mean_st = np.nanmean(arr_sub)

            out_df.at[wuchs_id,month+1] = mean_st

    col_name_lst = ['ID', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']
    out_df.index.name = 'ID'
    out_df.reset_index(inplace=True)
    out_df.columns = col_name_lst

    #out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\{0}_BL-2013-2019_VCI_wuchsgebiete.csv'.format(year)
    out_name = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\{0}_SPI_{1}_wuchsgebiete.csv'.format(year,spi)
    out_df.to_csv(out_name, index=False, decimal=".", sep=",")

    print('--------------------------------------------\n')
    del (vrt_ind)
    del (vrt_msk)
wuchs_lyr.ResetReading()

print('Done')


# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")