import pandas as pd
import gdal
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

with open(r'Y:\germany-drought\germany.txt') as file:
    tile_name_lst = file.readlines()
tile_name_lst = [item.strip() for item in tile_name_lst]

year = '2018'
tree = 'BROADLEAF'



abr_lst = ['DSS','DES','DPS','DFI','DLM','DRI'] #
# abr = 'DSS'
for abr in abr_lst :

    # DRI & DSS
    if abr == 'DSS' or abr == 'DRI':
        cut_lst = [-32768, -32767, 0, 25, 50, 75, 100, 125, 150, 365, 10000]
    # DES & DFI
    if abr == 'DES' or abr == 'DFI' or abr == 'DLM':
        cut_lst = [-32768, -32767, 0, 150, 200, 250, 300, 350, 365, 10000]
    if abr == 'DPS':
        cut_lst = [-32768, -32767, 0, 100, 125, 150, 175, 200, 225, 250, 365, 10000]
    if abr == 'LGS':
        cut_lst = [-32768, -32767, 0, 150, 175, 200, 225, 250, 275, 300, 365, 10000]

    hist_lst_brd = []

    print(abr, '\n')

    # tile_name = tile_name_lst[50]
    for tile_name in tile_name_lst:
        print(tile_name)

        year_str = str(int(year)-1) + '-' + str(int(year)+1)
        ras_pth = r'Y:\germany-drought\level4\{0}\{1}_001-365_LEVEL4_TSA_LNDLG_NDV_{2}-LSP.tif'.format(tile_name,year_str, abr)
        brd_msk_pth = r'Y:\germany-drought\masks\{0}\2015_MASK_FOREST-{1}_UNDISTURBED-2013_BUFF-01.tif'.format(tile_name, tree)

        ras = gdal.Open(ras_pth)
        brd_msk_ras = gdal.Open(brd_msk_pth)

        arr = ras.ReadAsArray()
        brd_msk_arr = brd_msk_ras.ReadAsArray() #

        arr[brd_msk_arr == 0] = -32767  # no data value FORCE -32767

        count_lst_brd = []
        for i in range(len(cut_lst) - 1):
            val_brd = ((cut_lst[i] < arr) & (arr <= cut_lst[i + 1])).sum()
            count_lst_brd.append(val_brd)

        hist_lst_brd.append(count_lst_brd)

    col_lst = []
    for i, item in enumerate(cut_lst[:-1]):
        col_lst.append(abr + '_' + str(item+1) + '_to_' + str(cut_lst[i+1]))

    out_df_brd = pd.DataFrame(hist_lst_brd)
    out_df_brd.columns = col_lst
    out_df_brd['Tile'] = tile_name_lst

    out_df_brd.to_csv(r'O:\Student_Data\CJaenicke\00_MA\data\tables\tile_counts_lsp_metrics\tile_counts_lsp_metrics_newLSP_' + year + '_' + abr + '_' + tree + '.csv', index=False)

    hist_counts_brd = []
    for i in range(1,len(cut_lst)-1):
        val_brd = 0
        val_gra = 0
        for item in hist_lst_brd:
            val_brd = val_brd + item[i]
        hist_counts_brd.append(val_brd)

    label_lst = []
    for i, item in enumerate(cut_lst[1:-1]):
        label_lst.append(str(item + 1) + ' to ' + str(cut_lst[i+2]))

    fig, ax = plt.subplots(figsize=(8,7))
    rects = ax.bar(label_lst, hist_counts_brd)
    plt.xticks(rotation=45, ha='right')
    plt.title('Histogramm ' + abr + ' ' + tree + ' ' + year)
    plt.tight_layout()
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(format(int(height), ',')),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    ax.get_yaxis().set_major_formatter(
        tick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.gcf().subplots_adjust(left=0.15)
    #fig.show()
    fig.savefig(r'O:\Student_Data\CJaenicke\00_MA\figures\LSP-metrics\histograms_germany\Histogramm_newLSP_'+year+'_' + abr + '-' + tree + '.png')