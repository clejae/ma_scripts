## Clemens Jänicke, Humboldt-Universität zu Berlin

## ---------------------------------------------------- PACKAGES ---------------------------------------------------- ##
import time
import os
import glob
from osgeo import gdal
from joblib import Parallel, delayed

## ---------------------------------------------------- FUNCTIONS ---------------------------------------------------- ##
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

## ---------------------------------------------------- PROCESSING ---------------------------------------------------- ##
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print(starttime)

os.chdir("Y:/berlin-phenology/LND_Composite_2017/")
tileList = glob.glob("*[!.prj]")

tileFolderList = []
for i in range(0,len(tileList)):
    tileFolderList.append("Z:/edc/level2/" + tileList[i]+ "/")

rasterList = []
for folder in tileFolderList:
    #print(folder)
    os.chdir(folder)
    fileList = glob.glob("[2016][2017][2018]*SEN2*BOA.tif")
    rasterList.append(fileList)
    #print(len(rasterList))

jobList = []
for i in range(0,len(tileList)):
    subList = [tileFolderList[i], tileList[i], rasterList[i]]
    jobList.append(subList)

print("Preparation done!")
#for i in jobList:
#    print(i)


#for tile in tileList:
#    createFolder(wf_SEN+tile)

wf_SEN = "Y:/berlin-phenology/SEN2_repr/"
def workFunc(job):
    wf = job[0]
    tile = job[1]
    for raster in job[2]:
        inputRaster = gdal.Open(wf+raster)
        gdal.Warp(wf_SEN + tile + "/EPSG4326_" + raster, inputRaster, dstSRS='EPSG:4326')


starttime_parallel = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("start parallel-processing: " + starttime_parallel)

if __name__ == '__main__':
    Parallel(n_jobs=20)(delayed(workFunc)(i) for i in jobList)

endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("end: " + endtime)
