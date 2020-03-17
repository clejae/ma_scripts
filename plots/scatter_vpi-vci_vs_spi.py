import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

spi_lst = ['01', '03', '06', '18', '12', '24', '48']
year_lst = ['2018','2019']
tree_lst = ['BROADLEAF','CONIFER']

for year in year_lst:
    print(year)
    for spi in spi_lst:
        print(spi)
        for tree in tree_lst:
            print(tree)

            df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\VPI_'+year+'_'+tree+'_BL-13-19.csv')

            df_spi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SPI_2018_'+spi+'.csv')
            df_area = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\VPI_2018_BROADLEAF_BL-13-19_area-norm.csv')
            col_name_lst = ['Name', '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12']

            ser_area = df_area['lc_area']

            fig, axs = plt.subplots(12, 12, sharey=True,sharex=True, figsize=(25, 25))
            fig.suptitle('VPI '+tree+' '+year+' - SPI '+spi, fontsize=16)
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            col_vpi, col_spi = '_02','_02'
            x_ind, y_ind = 0,0
            cmap = plt.cm.rainbow
            for y_ind, col_vpi in enumerate(col_name_lst[1:]):

                ser_vpi = df_vpi[col_vpi]
                for x_ind, col_spi in enumerate(col_name_lst[1:]):
                    ser_spi = df_spi[col_spi]
                    bool_lst = df_spi.index[df_spi[col_spi] == -999].tolist()
                    ser_spi = ser_spi.drop((bool_lst))
                    ser_vpi_temp = ser_vpi.drop((bool_lst))
                    ser_area_temp = ser_area.drop((bool_lst))

                    axs[x_ind, y_ind].scatter(ser_vpi_temp, ser_spi, s=0.4, c=ser_area_temp, cmap=cmap )
                    axs[x_ind, y_ind].title.set_text('VPI' + col_vpi + '-SPI' + col_spi)
                    # axs[x_ind, y_ind].set_xlabel(col_vpi[1:])
                    # axs[x_ind, y_ind].set_ylabel(col_spi[1:])
                    axs[x_ind, y_ind].set_ylim(-5, 2.5)
                    axs[x_ind, y_ind].set_xlim(0, 1)

            for x_ind, col_vpi in enumerate(col_name_lst[1:]):
                for y_ind, col_spi in enumerate(col_name_lst[1:]):
                    axs[y_ind, 0].set_ylabel('SPI-' + col_spi[1:], fontsize=14)
                    axs[11, x_ind].set_xlabel('VPI-' + col_vpi[1:], fontsize=14)

            #fig.show()
            fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\VPI '+tree+' '+year+' - SPI '+spi+'.png')


