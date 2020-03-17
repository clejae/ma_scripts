import os
import glob

#folder_lst = glob.glob(r'Y:\germany-drought\level4_sensitivity\metrics\*')
folder_lst = ['LIN-ITPL_02-SEG_16-INT','LIN-ITPL_03-SEG_16-INT','RBF-ITPL_02-SEG_32-INT_SIG8','RBF-ITPL_03-SEG_32-INT_SIG8']

folder_lst.sort()

#folder_lst = folder_lst[20:]
for item in folder_lst:
    folder = r'Y:\germany-drought\level4_sensitivity\metrics\\' + item
    tail_folder = os.path.split(folder)[1]
    print(tail_folder)

    file_lst = glob.glob(folder + r'\\**\*')
    for file in file_lst:
        tail_file = os.path.split(file)[1]
        head_file = os.path.split(file)[0]
        new_name = os.path.join(head_file, tail_folder + tail_file[-8:])
        os.rename(file, new_name)