import glob
import os

l = glob.glob(r'Y:\germany-drought\level4\**\*DES*')

for i in l:
    os.rename(i, i[:-4] + '_040.' + i[-3:])