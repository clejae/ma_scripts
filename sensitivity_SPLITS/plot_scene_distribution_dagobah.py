import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import glob
import os
import pandas as pd
import datetime
import numpy as np

with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

start = datetime.datetime.strptime('20130101', '%Y%m%d')
end = datetime.datetime.strptime('20191231', '%Y%m%d')
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
date_generated = [str(date)[:10] for date in date_generated]
date_generated = [date.replace("-","") for date in date_generated]

df = pd.DataFrame(index = date_generated, columns = tiles_lst)
for col in df.columns:
    df[col].values[:] = 0

month_range = []
year_range = [str(i) for i in range(2013,2020)]
for year in range(2013,2020):
    for month in range(1,13):
        if month <  10:
            month_gen = str(year) +'0' + str(month)
        else:
            month_gen = str(year) + str(month)
        month_range.append(month_gen)

df_mth = pd.DataFrame(index = month_range, columns = tiles_lst)
for col in df_mth.columns:
    df_mth[col].values[:] = 0

df_year = pd.DataFrame(index = year_range, columns = tiles_lst)
for col in df_year.columns:
    df_year[col].values[:] = 0

tile = tiles_lst[0]
y = 1
for tile in tiles_lst:
    scene_lst = [os.path.basename(x) for x in glob.glob(r'Z:\edc\level2\\'  + tile + r'\201[3-9]*BOA.tif')]
    scene_lst_year = [string[:4] for string in scene_lst]
    scene_lst_month = [string[:6] for string in scene_lst]
    scene_lst = [string[:8] for string in scene_lst]

    for scene in scene_lst:
        df.at[scene, tile] = y
    for scene in scene_lst_month:
        df_mth.at[scene, tile] += 1
    for scene in scene_lst_year:
        df_year.at[scene, tile] += 1

    y += 1

df_year['average'] = df_year.mean(axis=1)

# ---------------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(40, 10))
for i, column in enumerate(df):
    ax.plot(df.index.values, df[column], marker='o', label=column, linestyle='None')

legend = ax.legend(shadow=True, title='Input Tiles', fontsize=18)
loc = plticker.MultipleLocator(base=182.5)
ax.xaxis.set_major_locator(loc)
plt.xticks(rotation='vertical')
ax.set_xlabel('DOY', fontsize=20)
ax.set_ylim(0.5, 4.5)

plt.show()
plt.savefig(r'Y:\germany-drought\level4_sensitivity\plots\scene_distribution.png')
plt.close()

# ---------------------------------------------------------------------------------------------------------------------

fig2, ax2 = plt.subplots(figsize=(20, 10))
bar_width = 0.2
x_pos_lst = []
r1 = np.arange(len(df_mth.index))
x_pos_lst.append(r1)

for i in range(len(tiles_lst)-1):
    r = [x + bar_width * (i+1) for x in r1]
    x_pos_lst.append(r)

for i, column in enumerate(df_mth):
    r = x_pos_lst[i]
    ax2.bar(x = r, height = df_mth[column], width = bar_width, label= tiles_lst[i])

x_pos = 0
for i in range(0,8):
    ax2.axvline(x_pos, 0, 1, c='black')
    x_pos += 12

x_pos = 2
for i in range(0,7):
    ax2.annotate('Avg. #scenes: \n' + str(df_year['average'][i]), xy =(x_pos,19))
    x_pos += 12

ax2.set_ylabel('#Scenes', fontsize=20)
ax2.set_ylim(0,20)
legend = ax2.legend( shadow=True, title = 'Input Tiles', fontsize=12, loc='upper right')
plt.xticks([r + bar_width for r in range(len(df_mth.index))],df_mth.index.values, rotation='vertical')
fig2.show()
fig2.savefig(r'Y:\germany-drought\level4_sensitivity\plots\2013-2019_monthly_scene_distribution.png')
plt.close()

# ---------------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots(1,4,sharey=True, figsize=(40, 10))

plt.rcParams.update({'font.size':16})

for j, column in enumerate(df_mth):
    ax = plt.subplot(1,4,j+1)
    ax.bar(df_mth.index.values, df_mth[column])
    ax.set_ylim(0,20)
    x_pos = 0.5
    for i in range(0, 8):
        ax.axvline(x_pos, 0, 1, c='black')
        x_pos += 12

    x_pos = 2
    for i in range(0, 7):
        ax.annotate('Avg. \n' + str(df_year[column][i]), xy=(x_pos, 18), fontsize=16)
        x_pos += 12

    ax.set_title(tiles_lst[j], fontsize=24)
    plt.xticks(rotation='vertical')

    loc = plticker.MultipleLocator(base=12)
    ax.xaxis.set_major_locator(loc)

ax = plt.subplot(1,4,1)
ax.set_ylabel('#Scenes', fontsize=20)
fig.show()

fig.savefig(r'Y:\germany-drought\level4_sensitivity\plots\2013-2019_monthly_scene_distribution2.png')