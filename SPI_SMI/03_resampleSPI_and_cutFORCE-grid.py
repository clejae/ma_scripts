from osgeo import gdal, gdalconst
import ogr
import joblib
import time

#### ------------------------------ FUNCTIONS ----------------------------- ####

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

#### ------------------------------ RESAMPLING ----------------------------- ####
# # Source
# # for m in range(1,13):
# def workFunc(m):
#
#     print("Start Resampling")
#     src_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\SPI_24\SPI_{0:02d}2018_24_3035.tif'.format(m)
#     src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
#     src_proj = src.GetProjection()
#     src_geotrans = src.GetGeoTransform()
#     src_bands = src.RasterCount
#
#     # We want a section of source that matches this:
#     match_filename = r'Y:\germany-drought\vrt\masks\2015_MASK_FOREST-BROADLEAF_BUFF-01.vrt'
#     match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
#     match_proj = match_ds.GetProjection()
#     match_geotrans = match_ds.GetGeoTransform()
#     wide = match_ds.RasterXSize
#     high = match_ds.RasterYSize
#
#     # Output / destination
#     dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\SPI_24\SPI_{0:02d}2018_24_3035_resampled.tif'.format(m)
#     dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, src_bands, gdalconst.GDT_Float32)
#     dst.SetGeoTransform( match_geotrans )
#     dst.SetProjection( match_proj)
#
#     # Do the work
#     gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)
#
#     del(dst)
#
# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=6)(joblib.delayed(workFunc)(m) for m in range(1,13))

#### ------------------------------ CUT TO FORCE GRID ----------------------------- ####

# stime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
# print("start: " + stime)
# with open(r'Y:\germany-drought\germany.txt') as file:
#     tile_name_lst = file.readlines()
# tile_name_lst = [item.strip() for item in tile_name_lst]
#
# def workFunc(i):
#     print('Tile index',i)
#     for m in range(1,13):
#         ras_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\SPI_24\SPI_{0:02d}2018_24_3035_resampled.tif'.format(m)
#         ras = gdal.Open(ras_pth)
#         # arr = ras.ReadAsArray()
#         shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\miscellaneous\force-tiles_ger_3035.shp')
#         lyr = shp.GetLayer()
#         feat = lyr.GetFeature(i)
#
#         geom = feat.geometry().Clone()
#         name = feat.GetField('Name')
#
#         print('Start: Tile', i, name, '- month', m)
#
#         if int(name[3:5]) > 57:
#             #print(i, name)
#             extent = geom.GetEnvelope()
#
#             x_min_ext = extent[0] + 30
#             x_max_ext = extent[1] + 30
#             y_min_ext = extent[2]
#             y_max_ext = extent[3]
#
#             output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\\' + name + r'\\'
#             createFolder(output_path)
#             output_name_full = output_path + 'SPI_{0:02d}2018_24_3035_resampled.tif'.format(m)
#
#             # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]
#
#             ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
#             ras_cut = None
#
#         else:
#             #print(i, name)
#             extent = geom.GetEnvelope()
#
#             x_min_ext = extent[0]
#             x_max_ext = extent[1]
#             y_min_ext = extent[2]
#             y_max_ext = extent[3]
#
#             output_path = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\\' + name + r'\\'
#             createFolder(output_path)
#             output_name_full = output_path + 'SPI_{0:02d}2018_24_3035_resampled.tif'.format(m)
#
#             # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]
#
#             ras_cut = gdal.Translate(output_name_full, ras, projWin=[x_min_ext, y_max_ext, x_max_ext, y_min_ext])
#             ras_cut = None
#         print('DONE: Tile', i, name, '- month', m)
#
# if __name__ == '__main__':
#     joblib.Parallel(n_jobs=10)(joblib.delayed(workFunc)(i) for i in range(0,496))
#
# etime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
# print("start: " + stime)
# print("end: " + etime)

#### ------------------------------ STACK FORCE MONTHLY TILES ----------------------------- ####

with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]
tile = tiles_lst[1]

def workFunc(tile):
# for i, tile in enumerate(tiles_lst):
# for i in range(0, 496):

    print(tile)

    l = [r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\{0}\SPI_{1:02d}2018_24_3035_resampled.tif'.format(tile, m) for m in range(1,13)]
    l = [r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\SPI_{1}\SPI_{0:02d}2018_{1}_3035.tif'.format(m,) for m in range(1,13)]
    # l = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\{0}\SPI_*2018_24_3035_resampled.tif'.format(tile))
    print(len(l))
    # if len(l) > 12:
    #     print(tile)
    #     break
    if os.path.isfile(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\{0}\SPI24_2018.tif'.format(tile)):
        pass
    else:
        out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\{0}\SPI24_2018.tif'.format(tile)
        out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\SPI_01\SPI_2018_01_3035.tif'
        ras_lst = [gdal.Open(item) for item in l]
        arr_lst = [ras.ReadAsArray() for ras in ras_lst]
        arr_lst = [(arr * 1000).astype(int) for arr in arr_lst]
        arr_lst_nd = []
        for arr in arr_lst:
            arr[arr == 0] = -32767
        # arr_lst = [arr[arr == 0] - 32767 for arr in arr_lst]
        arr_out = np.stack(arr_lst,0)
        print(arr_out.shape)
        gt = ras_lst[0].GetGeoTransform()
        pr = ras_lst[0].GetProjection()
        no_data_value = -32767

        writeArrayToRasterInt(arr_out, out_pth, gt, pr, no_data_value)

if __name__ == '__main__':
    joblib.Parallel(n_jobs=20)(joblib.delayed(workFunc)(tile) for tile in tiles_lst)

