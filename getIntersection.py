import os
import numpy as np

dataset_path = '/data/raw_data_prepared/'
gtdata_path = '/data/gt_data_prepared/'
path = [dataset_path, gtdata_path]

data_set = set()
gt_set = set()
sets = [data_set, gt_set]


for i in range(2):
    subfolders = os.listdir(path[i])
    for s in subfolders:
        files = list(filter(lambda f: f.endswith(".jpg"), os.listdir(path[i] + s)))
        files.sort()
        files = files[1:-1]
        for fi in files:
            sets[i].add(s + " " + fi[:-4])

intersect = sets[0].intersection(sets[1])

with open(path[0]+ 'train.txt', 'w') as tf:
    with open(path[0] + 'val.txt', 'w') as vf:
        for item in list(intersect):
            if np.random.random() < 0.1:
                vf.write(item+'\n')
            else:
                tf.write(item+'\n')




#2011_09_26_drive_0095_sync_02 0000000071
