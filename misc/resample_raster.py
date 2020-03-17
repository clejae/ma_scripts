from osgeo import gdal, gdalconst

print("Load file to resample.")
# Source
src_filename  = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_06\SPI_06_06_3035.tif'
src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
src_proj = src.GetProjection()
src_geotrans = src.GetGeoTransform()

print("Load file with resampling grid.")
# We want a section of source that matches this:
match_filename =  r'O:\Student_Data\CJaenicke\00_MA\data\raster\LandCover\europe_landcover_2015_RSE-GER_resampled.tif'
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
match_proj = match_ds.GetProjection()
match_geotrans = match_ds.GetGeoTransform()
wide = match_ds.RasterXSize
high = match_ds.RasterYSize

print("Resample and Output.")
# Output / destination
dst_filename = r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\SPI_06\SPI_06_06_3035_resampled3.tif'
dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
dst.SetGeoTransform( match_geotrans )
dst.SetProjection( match_proj)

# Do the work
gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

del dst # Flush