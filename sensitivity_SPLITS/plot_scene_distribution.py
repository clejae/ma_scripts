import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import glob
import os
import pandas as pd
import datetime

with open(r'Y:\germany-drought\germany_subset2.txt') as file:
    tiles_lst = file.readlines()

tiles_lst = [item.strip() for item in tiles_lst]

start = datetime.datetime.strptime('20170101', '%Y%m%d')
end = datetime.datetime.strptime('20191231', '%Y%m%d')
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
date_generated = [str(date)[:10] for date in date_generated]
date_generated = [date.replace("-","") for date in date_generated]

fig, axs = plt.subplots(1, len(tiles_lst), sharey=True, sharex=True, figsize=(40, 10))

folder_lst = ['20','40','60','all']
for j, folder in enumerate(folder_lst):
    df = pd.DataFrame(index = date_generated, columns = tiles_lst)
    for col in df.columns:
        df[col].values[:] = 0

    tile = tiles_lst[0]
    y = 1
    for tile in tiles_lst:
        scene_lst = [os.path.basename(x) for x in glob.glob(r'Y:\germany-drought\sensitivity_dc\\' + folder + r'\\' + tile + r'\*BOA.tif')]
        scene_lst = [string[:8] for string in scene_lst]

        for scene in scene_lst:
            df.at[scene, tile] = y

        y += 1


    # fig, ax = plt.subplots(figsize=(10, 10))

    ax = plt.subplot(1,4,j+1)
    for i, column in enumerate(df):
        # plot current column against row names
        ax.plot(df.index.values, df[column], 'o', label=column)


    # change tick frequency on x-axis
    loc = plticker.MultipleLocator(base=182.5) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    # set vertical lines on x-axis
    ax.axvline(397, 0, 1)
    ax.axvline(425, 0, 1)
    ax.axvline(456, 0, 1)
    ax.axvline(486, 0, 1)
    ax.axvline(517, 0, 1)
    ax.axvline(547, 0, 1)
    ax.axvline(578, 0, 1)
    ax.axvline(609, 0, 1)
    ax.axvline(639, 0, 1)
    ax.axvline(670, 0, 1)
    ax.axvline(700, 0, 1)
    # highlight specific area on x-axis
    ax.axvspan(366, 731, color='green', alpha=0.2)
    # rotate x-axis-ticks labels
    plt.xticks(rotation='vertical')
    # set x-axis label
    ax.set_xlabel('DOY', fontsize=20)
    ax.set_xlim(181, 910)
    ax.set_ylim(0.5, y)
    ax.title.set_text(folder)

    if j +1 == 1:
        # change labels at y-axis
        ax.set_yticks([1, 2, 3, 4])
        ax.set_yticklabels(tiles_lst, fontsize=24)
    else:
        ax.set_yticklabels([])

# restraine y-axis limits


#plt.show()

plt.savefig(r'Y:\germany-drought\level4_sensitivity\plots\scene_distribution.png')
plt.close()





