from osgeo import gdal
import glob
import os

file_list = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\**\SPI06_2018.tif')
vrt = gdal.BuildVRT(r'O:\Student_Data\CJaenicke\00_MA\data\vrt\indices\SPI06_2018.vrt', file_list)
del(vrt)


file_list = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\X00*_Y0048\SPI_012018_24_3035_resampled.tif')
vrt = gdal.BuildVRT(r'O:\Student_Data\CJaenicke\00_MA\data\vrt\X00xx_Y0048.vrt', file_list)
del(vrt)



file_list = glob.glob(r'Y:\california\level2_ba\**\E_L2A_suBA_mosaic_crco_long.tif')
vrt = gdal.BuildVRT(r'Y:\california\E_L2A_suBA_mosaic_crco_long.vrt', file_list)
del(vrt)

for m in range(1,13):
    l = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\**\SPI24_{0}.tif'.format(m))
    for i in l:
        os.remove(i)

#wd = 'Y:/germany-drought/'
wd = r'O:\Student_Data\CJaenicke\00_MA\data\climate\SPI\tiles\\'

lst = ['VPI','VCI']
#lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']
#lst = ['CONIFEROUS','BROADLEAF','MIXED','CONIFEROUS_BUFF-01','BROADLEAF_BUFF-01','MIXED_BUFF-01']
#lst = ['DEM']
# lst = ['GRASSLAND_BUFF-01']
# abr = 'GRASSLAND_BUFF-01'
for abr in lst:
    print(abr)

    #file_list = glob.glob(wd + 'masks/**/*'+abr+ '.tif')
    file_list = glob.glob(wd + 'LSP-metrics/**/2018_BL-2013-2019_' + abr + '.tif')
    #file_list = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\raster\masks/**/2015_MASK_FOREST-BROADLEAF_UNDISTURBED-2013_BUFF-01.tif')
    print("Length", len(file_list))

    #vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=True)
    #print(wd + 'masks/2015_MASK_'+ abr + '.vrt')
    vrt = gdal.BuildVRT(wd + 'vrt/2018_BL-2013-2019_' + abr + '.vrt', file_list)

    #ds = gdal.Translate('Y:/berlin-phenology/SEN2_coreg/20160827_mosaic.tif', vrt)
    #del(ds)

    del(vrt)

print("\nDone!")