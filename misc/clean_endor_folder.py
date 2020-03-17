### Delete files


import os
import glob

lst = ['DEM','LTS','VEM','VLM','VBL','IST','IBL','IBT','RAR','RAF','RMR','RMF','STA']
lst = ['SPI']
abr = 'SPI'
for abr in lst:
    print(abr)
    file_lst = glob.glob(r'Y:\germany-drought\VCI_VPI\**\*_BL-2013-2017_TEST_VPI.tif')
    #file_lst = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\**\*resampled.tif')
    print(len(file_lst))
    for i, file in enumerate(file_lst):
        print(i+1, len(file_lst), '\n', file)
        os.remove(file)

### Delete folders

import glob
import shutil


with open(r'Y:\germany-drought\germany_subset_del.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

file_lst = glob.glob(r'Y:\germany-drought\VPI_Copernicus\**\*.vrt')
for file in tile_name_lst:
    shutil.rmtree('Y:/germany-drought/level4_sensitivity/metrics/ALL_OBS-08_LSP_SEG/' + file)
print("Done!")

lst = glob.glob(r"Y:\california\level2_ba\**\E_L2A_suBA_mosaic_crco_long*")
len(lst)

for file in lst:
    os.remove(file)