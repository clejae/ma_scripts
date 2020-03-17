import pandas as pd
import numpy as np
from functools import reduce

year_lst = ['2018','2019']
lc_lst = ['BROADLEAF','CONIFER','GRASSLAND']

for year in year_lst:
    for lc in lc_lst:
        df_lst = []
        print(year, lc)

        #year = '2018'
        # tree = 'CONIFER'

        #df_smi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SMI_2018_'+lc+'.csv')
        df_smi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\SMI_2018.csv')
        df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\VPI_' + year + '_'+lc+'_BL-13-19.csv')

        col_names_smi = ['Name', 'SMI_01', 'SMI_02', 'SMI_03', 'SMI_04', 'SMI_05', 'SMI_06', 'SMI_07', 'SMI_08', 'SMI_09', 'SMI_10', 'SMI_11', 'SMI_12']
        col_names_vpi = ['Name', 'VPI_01' + year, 'VPI_02' + year, 'VPI_03' + year, 'VPI_04' + year, 'VPI_05' + year, 'VPI_06' + year, 'VPI_07' + year, 'VPI_08' + year, 'VPI_09' + year, 'VPI_10' + year, 'VPI_11' + year, 'VPI_12' + year]

        df_smi.columns = col_names_smi
        df_vpi.columns = col_names_vpi

        merged_df = df_smi.set_index('Name').join(df_vpi.set_index('Name'))
        merged_df = merged_df.replace(-999, np.nan)

        corr_df = merged_df.corr()

        if year == '2019':
            t = corr_df.iloc[12:20, 0:12]
        if year == '2018':
            t = corr_df.iloc[12:, 0:12]

        t.index.name = 'Name'
        t.reset_index(inplace=True)

        t.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\correlations\smi-vpi-correlation_' + year + '_'+lc+'_total-SMI.csv')

print('Done')