import pandas as pd
import numpy as np
from functools import reduce

spi_lst = ['01', '03', '06', '18', '12', '24', '48']
year_lst = ['2018','2019']
tree_lst = ['BROADLEAF','CONIFER']

for year in year_lst:
    for tree in tree_lst:
        df_lst = []
        print('\n')

        year = '2018'
        # tree = 'CONIFER'

        for spi in spi_lst:
            #print(year, tree, spi)
            print(year, spi)
            df_spi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SPI_2018_'+spi+'.csv')
            df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\VPI_2018_grass_BL-13-19.csv')
            #df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\VPI_' + year + '_'+tree+'_BL-13-19.csv')

            col_names_spi = ['Name', 'SPI_' + spi + '_01', 'SPI_' + spi + '_02', 'SPI_' + spi + '_03', 'SPI_' + spi + '_04', 'SPI_' + spi + '_05', 'SPI_' + spi + '_06', 'SPI_' + spi + '_07', 'SPI_' + spi + '_08', 'SPI_' + spi + '_09', 'SPI_' + spi + '_10', 'SPI_' + spi + '_11', 'SPI_' + spi + '_12']
            col_names_vpi = ['Name', 'VPI_01' + year, 'VPI_02' + year, 'VPI_03' + year, 'VPI_04' + year, 'VPI_05' + year, 'VPI_06' + year, 'VPI_07' + year, 'VPI_08' + year, 'VPI_09' + year, 'VPI_10' + year, 'VPI_11' + year, 'VPI_12' + year]

            df_spi.columns = col_names_spi
            df_vpi.columns = col_names_vpi

            merged_df = df_spi.set_index('Name').join(df_vpi.set_index('Name'))
            merged_df = merged_df.replace(-999, np.nan)

            corr_df1 = merged_df.corr()
            corr_df = corr_df1.copy()

            if year == '2019':
                t = corr_df.iloc[12:20, 0:12]
            if year == '2018':
                t = corr_df.iloc[12:, 0:12]

            t.index.name = 'Name'
            t.reset_index(inplace=True)

            df_lst.append(t)

        df_final = reduce(lambda x, y: pd.merge(x, y, on = 'Name'), df_lst)
        #df_final.to_csv(r'O:\Student_Data\CJaenicke\00_MA\figures\index_comparison\BL_2013-2019\spi-vpi-correlation_'+year+'_'+tree+'.csv')
        df_final.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\spi-vpi-correlation_' + year + '_grass.csv')
print('Done')