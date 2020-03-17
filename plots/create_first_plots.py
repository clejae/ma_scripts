import gdal
import numpy as np
import ogr, osr
import pandas as pd
import matplotlib.pyplot as plt

abr_lst_all = ['DEM','DSS','DRI','DPS','DFI','DES','DLM','LTS','LGS','VEM','VSS','VRI','VPS','VFI','VES','VLM','VBL','VSA','IST','IBL','IBT','IGS','RAR','RAF','RMR','RMF']

df = pd.read_csv(r'O:\Student_Data\CJaenicke\00_MA\data\vector\random_sample\random_sample_02_analysis_extract.csv', sep=",")
df_bu = df.copy()

#df.shape

df = df.drop(df.index[[65, 1525, 1929, 2991, 4060, 5087, 6866, 8188, 8542]])
df = df.drop('Unnamed: 0', axis=1)
#df.shape

# for abr in abr_lst_all:
#     print("MIN:", abr, min(df[abr]))
#     print("MAX:", abr, max(df[abr]))

# for col in df.columns:
#     print(col)
#
# df.boxplot()
# plt.show()

fig, axs = plt.subplots(4, 7)

# basic plot
axs[0, 0].boxplot()
axs[0, 0].set_title('basic plot')

for abr in abr_lst_all:
    df.boxplot(column=abr)
    plt.title(abr)

    #plt.savefig(output_path + output_description + class_name + '.png')
    plt.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\drouhgt_germany\boxplot-COMP-2014-2017-TO-2018_' + abr + '.png')
    #plt.show()
    plt.close()



