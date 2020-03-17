import gdal
import pandas as pd
import glob

with open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_02.txt') as file:
    sample_lst = file.readlines()


sample_lst = [item.strip() for item in sample_lst]
sample_lst = [item.split(sep=',') for item in sample_lst]
df = pd.DataFrame(sample_lst)

df.columns = df.iloc[0]
df = df.reindex(df.index.drop(0))

spi_folder_lst = glob.glob(r'O:\Student_Data\CJaenicke\00_MA\data\climate\dwd_precipitation\SPI\*')

folder = spi_folder_lst[0]
for folder in spi_folder_lst:

    ras_pth_lst = glob.glob(folder + r'\*.tif')

    ras_pth = ras_pth_lst[0]
    for ras_pth in ras_pth_lst:
        ras = gdal.Open(ras_pth)

        arr = ras.ReadAsArray()
        gt = ras.GetGeoTransform()

        coord_lst = []
        i = 0
        for i in range(1, len(df.shape[0]) + 1):
            y_coord = df.iloc[i][2]