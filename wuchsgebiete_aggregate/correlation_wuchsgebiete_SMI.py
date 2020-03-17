import pandas as pd
import numpy as np
from functools import reduce
import gdal
gdal.Info()
tree_lst = ['BROADLEAF','CONIFER']

print('\n')

for year in range(2018,2020):
    df_lst = []
    print(year)

    df_smi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\SMI_GESAMTBODEN_2018_wuchsgebiete.csv')
    df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\VPI_{0}_wuchsgebiete.csv'.format(year))

    col_names_smi = ['Name']
    for m in range(1,13):
        col_names_smi.append('SMI_{0:02d}'.format(m))

    col_names_vpi = ['Name']
    for m in range(1,13):
        col_names_vpi.append('VPI_{0:02d}_{1}'.format(m, year))

    df_smi.columns = col_names_smi
    df_vpi.columns = col_names_vpi

    merged_df = df_smi.set_index('Name').join(df_vpi.set_index('Name'))
    merged_df = merged_df.replace(-999, np.nan)

    corr_df1 = merged_df.corr()
    corr_df = corr_df1.copy()

    t = corr_df.iloc[12:, 0:12]

    t.index.name = 'Name'
    t.reset_index(inplace=True)

    df_lst.append(t)

    df_final = reduce(lambda x, y: pd.merge(x, y, on = 'Name'), df_lst)
    df_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\correlations_wuchsgebiete\smi-vpi-correlation_{0}_wuchsgebiete_BROADLEAF.csv'.format(year)
    df_final.to_csv(df_pth)

print('Done')