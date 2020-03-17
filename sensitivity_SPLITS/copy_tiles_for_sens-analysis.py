import glob
import random
import joblib
import shutil

def createFolder(directory):
    import os
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

# read tiles from text file into a list
with open(r'Y:\germany-drought\germany.txt') as file:
    tiles_lst = file.readlines()
tiles_lst = [item.strip() for item in tiles_lst]

# loop over list
def workFunc(tile):
    print(tile)

    file_vci = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\2018_BL-2013-2019_VCI.tif'
    file_vpi = r'Y:\germany-drought\VCI_VPI\\' + tile + r'\2018_BL-2013-2019_VPI.tif'

    shutil.copy2(file_vci, r'O:\Student_Data\CJaenicke\00_MA\data\raster\LSP-metrics\\'  + tile)
    shutil.copy2(file_vpi, r'O:\Student_Data\CJaenicke\00_MA\data\raster\LSP-metrics\\' + tile)
    print("Done", tile)

if __name__ == '__main__':
    joblib.Parallel(n_jobs=15)(joblib.delayed(workFunc)(i) for i in tiles_lst)

    # rnd_sample_lst = [60,40,20]
    #
    # for rnd_sample in rnd_sample_lst:
    #
    #     print(rnd_sample)
    #     half_rnd = int(rnd_sample/2)
    #
    #     # search for all files in folder of tile and draw a random file
    #
    #     #file_lst = glob.glob(r'Z:\edc\level2\\' + tile + r'\\201[7-9]*BOA*')
    #     file_lst_2018 = glob.glob(r'Y:\germany-drought\sensitivity_dc\all\\' + tile + r'\\2018*BOA*.tif')
    #     rnd_lst_2018 = random.sample(file_lst_2018, rnd_sample)
    #
    #     file_lst_2017 = glob.glob(r'Y:\germany-drought\sensitivity_dc\all\\' + tile + r'\\2017*BOA*.tif')
    #     rnd_lst_2017 = random.sample(file_lst_2017, half_rnd)
    #
    #     file_lst_2019 = glob.glob(r'Y:\germany-drought\sensitivity_dc\all\\' + tile + r'\\2019*BOA*.tif')
    #     rnd_lst_2019 = random.sample(file_lst_2019, half_rnd)
    #
    #     # join all three lists into one
    #     file_lst = rnd_lst_2017 + rnd_lst_2018 + rnd_lst_2019
    #     print(len(file_lst))
    #
    #     # loop over joined list
    #     for file in file_lst:
    #
    #         # create folder, if it doesn't exist
    #         # copy file into said folder
    #         createFolder(r'Y:\germany-drought\sensitivity_dc\\' + str(rnd_sample) + r'\\' + tile)
    #         shutil.copy2(file, r'Y:\germany-drought\sensitivity_dc\\' + str(rnd_sample) + r'\\' + tile)
    #         shutil.copy2(file[:-3] + 'hdr', r'Y:\germany-drought\sensitivity_dc\\' + str(rnd_sample) + r'\\' + tile)
    #
    #         # replace substr 'BOA' with 'QAI' to also copy the corresponding QAI files
    #         qai_str = file.replace('BOA','QAI')
    #         shutil.copy2(qai_str, r'Y:\germany-drought\sensitivity_dc\\' + str(rnd_sample) + r'\\' + tile)
    #         shutil.copy2(qai_str[:-3] + 'hdr', r'Y:\germany-drought\sensitivity_dc\\' + str(rnd_sample) + r'\\' + tile)
