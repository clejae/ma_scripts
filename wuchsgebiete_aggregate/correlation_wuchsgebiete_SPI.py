import pandas as pd
import numpy as np
from functools import reduce

spi_lst = ['03', '06', '12', '24']
tree_lst = ['BROADLEAF','CONIFER']


for year in range(2018,2019):
    df_lst = []
    #print(year, tree, spi)
    for spi in spi_lst:
        print(year, spi)
        df_spi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\SPI{0}_2018_wuchsgebiete.csv'.format(spi))
        df_vpi = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\wuchsgebiete\VCI_{0}_wuchsgebiete.csv'.format(year))

        col_names_spi = ['Name']
        for m in range(1,13):
            col_names_spi.append('SPI_{0}_{1:02d}'.format(spi, m))

        col_names_vpi = ['Name']
        for m in range(1,13):
            col_names_vpi.append('VCI_{0:02d}_{1}'.format(m, year))

        df_spi.columns = col_names_spi
        df_vpi.columns = col_names_vpi

        merged_df = df_spi.set_index('Name').join(df_vpi.set_index('Name'))
        merged_df = merged_df.replace(-999, np.nan)

        corr_df1 = merged_df.corr()
        corr_df = corr_df1.copy()

        t = corr_df.iloc[12:, 0:12]

        t.index.name = 'Name'
        t.reset_index(inplace=True)

        df_lst.append(t)

    df_final = reduce(lambda x, y: pd.merge(x, y, on = 'Name'), df_lst)
    df_pth = r'O:\Student_Data\CJaenicke\00_MA\data\vector\lsp_metrics\correlations_wuchsgebiete\spi-vci-correlation_{0}_wuchsgebiete_BROADLEAF_new.csv'.format(year)
    df_final.to_csv(df_pth)

print('Done')