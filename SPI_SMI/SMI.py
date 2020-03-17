import numpy as np
import gdal
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from scipy.interpolate import griddata

def writeRasterFloat(in_array, out_path, gt, pr, no_data_value):

    if len(in_array.shape) == 3:
        nbands_out = in_array.shape[0]
        x_res = in_array.shape[2]
        y_res = in_array.shape[1]

        out_ras = gdal.GetDriverByName('GTiff').Create(out_path, x_res, y_res, nbands_out, gdal.GDT_Float32)
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

def GetExtent(gt, cols, rows):
    # Get extent from gt und cols,rows.
    # found at http://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
    # Format is: [[UpperLeft],[LowerLeft],[LowerRight],[UpperRight]]
    ext = []
    xarr = [0, cols]
    yarr = [0, rows]
    for px in xarr:
        for py in yarr:
            x = gt[0] + (px * gt[1]) + (py * gt[2])
            y = gt[3] + (px * gt[4]) + (py * gt[5])
            ext.append([x, y])
        yarr.reverse()
    return ext


ref_pth = r'Y:\germany-drought\vrt\masks\2015_MASK_FOREST-BROADLEAF_BUFF-01.vrt'
#ref_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_12\SPI_012018_12_3035.tif'
netcdf_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\SMI_Lall_Gesamtboden_monatlich_1951_2018_inv.nc"
#netcdf_pth = r"O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\SMI_L02_Oberboden_monatlich_1951_2018_inv.nc"
out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\SMI_2018_Gesamtboden.tif'

print('opening input')
## open a reference raster
ref_ras = gdal.Open(ref_pth)
gt = ref_ras.GetGeoTransform()
pr = ref_ras.GetProjection()
ref_arr = ref_ras.ReadAsArray()

## get Info about netcdf File
print(gdal.Info(netcdf_pth))

## open netcdf file, load subds and read them as arrays
ds = gdal.Open(netcdf_pth)
subds_lst = ds.GetSubDatasets()
## SMI
ds_smi = gdal.Open(ds.GetSubDatasets()[0][0])
smi_arr = ds_smi.ReadAsArray()
## kerndel width
ds_kw = gdal.Open(ds.GetSubDatasets()[1][0])
kw_arr = ds_kw.ReadAsArray()
## latitude
ds_lat = gdal.Open(ds.GetSubDatasets()[2][0])
lat_arr = ds_lat.ReadAsArray()
## longtitude
ds_lon = gdal.Open(ds.GetSubDatasets()[3][0])
lon_arr = ds_lon.ReadAsArray()

## optional: check difference between neighbouring lat/lon values
# t1 = lat_arr[0,:] - lat_arr[1,:]
# t2 = lat_arr[:,0] - lat_arr[:,1]
#
# t3 = lon_arr[0,:] - lon_arr[1,:]
# t4 = lon_arr[:,0] - lon_arr[:,1]

## get projection of netcdf file, in this case its empty
# pr_netcdf = ds.GetProjection()

## get lat, lon and smi-values
# for y in range(lat_arr.shape[0]):
#     for x in range(lat_arr.shape[1]):
#         y_coord = lat_arr[y,x]
#         x_coord = lon_arr[y,x]
#         value = smi_arr[0,y,x]
#
#         coord_lst.append([y_coord, x_coord, value])

## export lat, lon and smi-values to csv for use in GIS
# with open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\coordinates_with-values.txt', 'w+') as file:
#     file.write("y_index, x_index\n")
#     for item in coord_lst:
#         for i in range(len(item)):
#             if i < len(item) - 1:
#                 file.write(str(item[i]) + ", ")
#             else:
#                 file.write(str(item[i]))
#         file.write("\n")
# file.close()

## lat, lon values are in EPSG 4326, this transfroms them into EPSG 3035

proj = '3035'
in_proj = Proj(init='epsg:4326')
out_proj = Proj(init='epsg:'+proj)
x_arr, y_arr = transform(in_proj, out_proj, lon_arr, lat_arr)

## get extent of reference raster
## Format is: [[UpperLeft],[LowerLeft],[LowerRight],[UpperRight]]
extent = GetExtent(gt, ref_ras.RasterXSize, ref_ras.RasterYSize)
min_x = min([i[0] for i in extent])
max_x = max([i[0] for i in extent])
min_y = min([i[1] for i in extent])
max_y = max([i[1] for i in extent])


## optional: create gt for output, but is should be the same as the reference gt
pixel_x_size = (max_x - min_x)/ref_ras.RasterXSize
pixel_y_size = (max_y - min_y)/ref_ras.RasterYSize
gt_out = (min_x, pixel_x_size, 0, max_y, 0, -pixel_y_size)

## create two grids of lat/lon values representing the reference raster
## the interpolation-function does not take a pre-created tuple of both grid as input
## the tuple needs to be created on the function (see below for clarification)
xi = np.linspace(min_x, max_x, ref_ras.RasterXSize)
yi = np.linspace(min_y, max_y, ref_ras.RasterYSize)
grid = np.meshgrid(xi, yi)
grid_x = grid[0]
grid_y = grid[1]

## optional: get sub_arr of smi_arr
## for example the last 12 bands, i.e. jan-dec 2018
arr_sub = smi_arr[-12:,:,:]

## optional: flip array upside-down, because values are stored upside-down
## but not necessary since lat/lon values are stored up-down as well
# arr_sub = np.flip(arr_sub, axis=1)

## create list to store all interpolated bands in:
#out_lst = []

for i in range(12):
    print(i)
    ## Get input for interpolation from netcdf arrays
    ## Theses are the SMI values with corresponding lat/lon values
    arr = arr_sub[i,:,:]
    values = arr.flatten(order='F')
    x_arr_f = x_arr.flatten(order='F')
    y_arr_f = y_arr.flatten(order='F')

    ## Drop no-data values. In this case -9999
    values[values == -9999] = np.nan
    x_arr_f[np.isnan(values)] = np.nan
    y_arr_f[np.isnan(values)] = np.nan
    values = values[np.logical_not(np.isnan(values))]
    x_arr_f = x_arr_f[np.logical_not(np.isnan(x_arr_f))]
    y_arr_f = y_arr_f[np.logical_not(np.isnan(y_arr_f))]
    points = np.array([x_arr_f, y_arr_f])
    points = points.T

    ## Interpolate
    grid_int = griddata(points, values, (grid_x, grid_y), method='linear')

    ## ! Do this only, if the netcdf arrays wasnt flipped before !
    ## Optional: flip the interpolated grid
    int_arr = np.flip(grid_int, axis=0)

    ## Set the extrapolated areas to nodata value
    int_arr[ref_arr == -999] = -999

    ## Optional: plot the array
    # cmap = plt.cm.RdYlGn
    # cmap.set_bad('white')
    # fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.imshow(out_arr)
    # fig.show()

    out_pth = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\SMI_2018_Gesamtboden_' + str(i) + '.tif'
    ## Write raster to disc
    writeRasterFloat(int_arr, out_pth, gt_out, pr, -999)

    #out_lst.append(int_arr)

#out_arr = np.array(out_lst)





## Additional and not used: create and set projection of raster manually
## ! Some lines are missing !
# t1 = y_arr[0,:] - y_arr[1,:]
# np.mean(t1)
# t2 = x_arr[:,0] - x_arr[:,1]
# np.mean(t2)
# # x_min = np.min(x_arr)
# # y_max = np.max(y_arr)
# x_arr = np.flip(x_arr, axis=0)
# y_arr = np.flip(y_arr, axis=0)
# x_min = x_arr[0,0]
# y_max = y_arr[0,0]
# a1 = y_arr[0,174] - y_arr[0,0]
# b1 = x_arr[0,174] - x_arr[0,0]
# c1 = math.sqrt(a1** 2 + b1**2)
# sin_alpha1 = a1/c1
# alpha1 = math.degrees(sin_alpha1)
# b2 = y_arr[0,0] - y_arr[224,0]
# a2 = x_arr[224,0] - x_arr[0,0]
# c2 = math.sqrt(a2** 2 + b2**2)
# sin_alpha2 = a2/c2
# alpha2 = math.degrees(sin_alpha2)
# proj = '3035'
# # x_tf, y_tf = transform(in_proj, out_proj, x_min, y_max)
# # y_tf = y_tf - 12000
# gt_new = (x_tf, 4000, 0, y_tf, 0, -4000)
# sr = osr.SpatialReference()
# sr.ImportFromEPSG(int(proj))
# pr = sr.ExportToWkt()
# writeRasterFloat(arr_out, r'O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\test_' + proj + '.bsq', gt_new, pr, -999)

## cut raster to FORCE grid
import gdal
import joblib

print('cut raster to FORCE grid\n')

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def getCorners(path):
    ds = gdal.Open(path)
    gt = ds.GetGeoTransform()
    width = ds.RasterXSize
    height = ds.RasterYSize
    minx = gt[0]
    miny = gt[3] + width * gt[4] + height * gt[5]
    maxx = gt[0] + width * gt[1] + height * gt[2]
    maxy = gt[3]
    return [minx, miny, maxx, maxy]

month_lst = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# for month in month_lst:
def workFunc(month):
    print("Start", month)
    ras = gdal.Open(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SMI\SMI_'+month+'2018_Gesamtboden.tif')
    arr = ras.ReadAsArray()

    with open(r'Y:\germany-drought\germany.txt') as file:
        tiles_lst = file.readlines()

    tiles_lst = [item.strip() for item in tiles_lst]

    i = 0

    gt = ras.GetGeoTransform()
    pr = ras.GetProjection()

    for tile in tiles_lst:

        print(tile)

        tile_pth = 'Y:/germany-drought/level4/' + tile + '/2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_DLM.tif'
        print(tile_pth)
        i += 1

        extent = getCorners(tile_pth)

        x_min_ext = extent[0]
        x_max_ext = extent[2]
        y_min_ext = extent[1]
        y_max_ext = extent[3]

        # slice input raster array to common dimensions
        px_min = int((x_min_ext - gt[0]) / gt[1])
        px_max = int((x_max_ext - gt[0]) / gt[1])

        py_max = int((y_min_ext - gt[3]) / gt[5])  # raster coordinates count from S to N, but array count from T to B, thus pymax = ymin
        py_min = int((y_max_ext - gt[3]) / gt[5])

        geom_arr = arr[py_min: py_max, px_min: px_max]
        #geom_arr = np.round(geom_arr, 3)

        createFolder(r'Y:\germany-drought\SMI\\' + tile)

        output_name = r'Y:\germany-drought\SMI\\' + tile + r'\SMI_'+month+'2018_Gesamtboden.tif'

        # write arr img to disc
        output_ds = gdal.GetDriverByName('ENVI').Create(output_name, geom_arr.shape[1], geom_arr.shape[0], 1,
                                                        gdal.GDT_Float32)

        output_ds.SetGeoTransform((x_min_ext, gt[1], 0, y_max_ext, 0, gt[5]))
        output_ds.SetProjection(ras.GetProjection())

        band = output_ds.GetRasterBand(1)
        band.WriteArray(geom_arr)
        band.SetNoDataValue(-999)
        band.FlushCache()
        del(output_ds)

    print("Done", month)

if __name__ == '__main__':
    joblib.Parallel(n_jobs=5)(joblib.delayed(workFunc)(i) for i in month_lst)