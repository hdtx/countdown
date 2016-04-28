from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors

df = pd.read_csv('stats.txt', index_col=0, dtype={'game': 'str'})
# start and end points for each set (0 large numbers, 1, 2, 3, 4)
limits = [[0, 2850],
          [2850, 8658],
          [8658, 12348],
          [12348, 13188],
          [13188, 13243]]

### Generate images for the data
## First raw B-W images, black for no solution, white for at least one solution

# dpi=1 is needed or a column may vanish (http://stackoverflow.com/q/36863768/)
plt.imsave('res/bw_data_all.png',
           df.iloc[:,11:911].values, cmap=cm.binary_r, dpi=1)
for (li, l) in enumerate(limits):
    plt.imsave('res/bw_data_{0}.png'.format(li),
               df.iloc[l[0]:l[1],11:911].values, cmap=cm.binary_r, dpi=1)

## Color-coded images according to how many points it's possible to get
dpts = pd.DataFrame(df.iloc[:,1:] * 3, dtype='int8')

def calc_p(row, reverse=False):
    dist = 11
    it = range(len(row))
    if reverse:
        it.reverse()
    for j in it:
        dist += 1
        if row[j] != 0:
            dist = 0
        elif dist <= 5:
            row[j] = 2
        elif dist <= 10:
            row[j] = 1
    return row

def calc_points(row):
    row = calc_p(row)
    row = calc_p(row, reverse=True)
    return row

dpts = dpts.apply(calc_points, raw=True, axis=1).iloc[:,10:910]

# make a color map of fixed colors (http://stackoverflow.com/q/9707676)
cmap = colors.ListedColormap(['black', 'red', 'green', 'white'])
bounds=[0,1,2,3]

plt.imsave('res/data_all.png', dpts.values, cmap=cmap, dpi=1)
for (li, l) in enumerate(limits):
    plt.imsave(
        'res/data_{0}.png'.format(li), dpts.iloc[l[0]:l[1],:], cmap=cmap, dpi=1)

### Generate statistics of the solvability for each game/value

(dpts.apply(pd.value_counts, normalize=True, axis=1).fillna(0) * 100).to_json(
    'res/perc_game_all.json', double_precision=2, orient='index')
(dpts.apply(pd.value_counts, normalize=True, axis=0).fillna(0) * 100).to_json(
    'res/perc_val_all.json', double_precision=2)
for (li, l) in enumerate(limits):
    (dpts.iloc[l[0]:l[1],:].apply(
        pd.value_counts, normalize=True, axis=1).fillna(0) * 100).to_json(
        'res/perc_game_{0}.json'.format(li), double_precision=2, orient='index')
    (dpts.iloc[l[0]:l[1],:].apply(
        pd.value_counts, normalize=True, axis=0).fillna(0) * 100).to_json(
        'res/perc_val_{0}.json'.format(li), double_precision=2)
