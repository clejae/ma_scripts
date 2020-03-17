import gdal
import numpy as np
import joblib
import os

file_name =  'COMP-2014-2017-TO-2018_withSTD_'

with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]

input_lst = [r'Y:\germany-drought\level4\\' + item + r'\2013-2019_001-365_LEVEL4_TSA_LNDLG_NDV_C0_S0_FLSP_TY_C95T_' for item in tiles_lst]
out_name_lst = [r'Y:\germany-drought\level4_analysis\\' + item + r'\\' + file_name for item in tiles_lst]
out_pth_lst = [r'Y:\germany-drought\level4_analysis\\' + item  for item in tiles_lst]

job_lst = [[input_lst[i], out_name_lst[i], out_pth_lst[i]] for i in range (len(input_lst))]

## Optional check job list
# for i, job in enumerate(job_lst):
#    print(i+1)
#    print(job)

def workFunc(job):
    print("Start: " + job[0])

    #### DOY measures
    # abr_lst = ['DEM','DSS','DRI','DPS','DFI','DES','DLM']

    #### non-accumulative measures
    abr_lst = ['LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']
    abr_lst = ['LGS', 'VPS', 'VES', 'VLM', 'VBL', 'VSA', 'IBL', 'IBT', 'IGS']

    for abr in abr_lst:
        input_name = job[0] + abr + '.tif'

        ras = gdal.Open(input_name)
        output_name = job[1] + abr + '.tif'

        gt = ras.GetGeoTransform()
        pr = ras.GetProjection()

        x_res = ras.RasterXSize
        y_res = ras.RasterYSize

        arr = ras.ReadAsArray()

        #### DOY measures
        ## the logic behind the raster values
        ## 2014 = 365    2015 = 365      2016 = 366      2017 = 365          2018 = 365
        ## 0 * 365 + x   1 * 365 + x     2 * 365 + x     3 * 365 + x + 1     4 * 365 + x + 1
        ## DOY = x       x - 365         x - 2*365       x - 3*365 - 1       x - 4 * 365 - 1

        # ref_arr = (np.sum(arr[0:4,:,:], axis=0) - 6 * 365 - 1 ) / 4
        # comp_arr = (arr[4,:,:] - 4 * 365 - 1) - ref_arr


        #### non-accumulative measures
        ref_arr = np.mean(arr[0:4,:,:], axis=0)
        comp_arr = arr[4,:,:] - ref_arr

        std_dev_arr = np.std(arr, axis=0)

        msk_arr = comp_arr[np.abs(comp_arr) > np.abs(std_dev_arr)]

        output_path = job[2]

        try:
            # Create target Directory
            os.mkdir(output_path)
            print("Directory " , output_path ,  " Created ")
        except FileExistsError:
            print("Directory " , output_path ,  " already exists")

        target_ds = gdal.GetDriverByName('GTiff').Create(output_name, x_res, y_res, 3, gdal.GDT_Int16)
        target_ds.SetGeoTransform(gt)
        target_ds.SetProjection(pr)

        band = target_ds.GetRasterBand(1)
        band.WriteArray(comp_arr)
        band.SetNoDataValue(-999)
        band.FlushCache()

        band = target_ds.GetRasterBand(2)
        band.WriteArray(std_dev_arr)
        band.SetNoDataValue(-999)
        band.FlushCache()

        band = target_ds.GetRasterBand(3)
        band.WriteArray(std_dev_arr2)
        band.SetNoDataValue(-999)
        band.FlushCache()

        del(target_ds)

    print("Done: " + job[0])

if __name__ == '__main__':
    joblib.Parallel(n_jobs=4)(joblib.delayed(workFunc)(i) for i in job_lst)