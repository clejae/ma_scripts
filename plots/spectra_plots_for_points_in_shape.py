import gdal, ogr
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

shp = ogr.Open(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\broadleaf_tree_sample.shp')

lyr = shp.GetLayer()

for feat in lyr:
    id_feat = feat.GetField('id')
    tile_name = feat.GetField('Tile')

    geom = feat.GetGeometryRef()
    env = geom.GetEnvelope()

    ras_vci = gdal.Open(r'Y:\germany-drought\VCI_VPI\\' + tile_name + r'\2018_BL-2013-2019_VPI.tif')
    arr_vci = ras_vci.ReadAsArray()

    ras_spi1 = gdal.Open(r'Y:\germany-drought\SPI\\' + tile_name + r'\SPI_062018_06.tif')
    arr_spi1 = ras_spi1.ReadAsArray()

    ras_spi2 = gdal.Open(r'Y:\germany-drought\SPI\\' + tile_name + r'\SPI_082018_06.tif')
    arr_spi2 = ras_spi2.ReadAsArray()

    gt = ras_vci.GetGeoTransform()

    x_coord = env[0]
    y_coord = env[2]

    x_ind = math.floor((x_coord - gt[0]) / gt[1])
    y_ind = math.floor((y_coord - gt[3]) // gt[5])


    def plotTimeSeries(x, y, annotation, title):
        slice_vci = arr_vci[:, y, x]
        slice_vci = slice_vci / 10000.0
        slice_vci[slice_vci == -3.2767] = np.nan
        # slice_tsi = arr_tsi[:, y, x]
        # slice_tsi = slice_tsi / 10000.0
        # slice_tsi[slice_tsi == -3.2767] = np.nan

        #color_dict = {'LND08': 'black', 'LND07': 'black', 'SEN2A': 'grey', 'SEN2B': 'grey'}

        plt.rcParams.update({'font.size': 16})
        fig, ax = plt.subplots(figsize=(15, 5))
        legend_elements = [Line2D([0], [0], color='C0', lw=2, label='RBF-Interpolation'),
                           Line2D([0], [0], marker='o', color='black', label='Landsat observation',
                                  markerfacecolor='black', markersize=5, linestyle='None'),
                           Line2D([0], [0], marker='o', color='grey', label='Sentinel observation',
                                  markerfacecolor='grey', markersize=5, linestyle='None')]

        # 0,4153005464480874
        # 0,4945355191256831

        ax.scatter(dates_lst, slice_vci, color=[color_dict[i] for i in sensors_lst])
        ax.plot(dates_lst_tsi, slice_tsi)
        ax.axvspan(2013.415, 2013.495, color='C2', alpha=0.2)
        ax.axvspan(2014.415, 2014.495, color='C2', alpha=0.2)
        ax.axvspan(2015.415, 2015.495, color='C2', alpha=0.2)
        ax.axvspan(2016.415, 2016.495, color='C2', alpha=0.2)
        ax.axvspan(2017.415, 2017.495, color='C2', alpha=0.2)
        ax.axvspan(2018.415, 2018.495, color='C1', alpha=0.2)
        ax.axvspan(2019.415, 2019.495, color='C2', alpha=0.2)
        ax.legend(handles=legend_elements, loc=3)
        ax.annotate(annotation, xy=(2013, .95), fontsize=16)
        ax.set_ylabel('NDVI')
        ax.set_ylim(0, 1)
        ax.set_xlim(2013, 2020)
        ax.title.set_text(title)
        fig.show()
        return fig