from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
from collections import defaultdict

df = pd.read_csv('stats.txt', index_col=0, dtype={'game': 'str'})

# start and end points for each set (0 large numbers, 1, 2, 3, 4)
limits = [[0, 2850],
          [2850, 8658],
          [8658, 12348],
          [12348, 13188],
          [13188, 13243]]

### Generate images for the data

# raw B-W images, black for no solution, white for at least one solution
# dpi=1 is needed or a column may vanish (http://stackoverflow.com/q/36863768/)
plt.imsave('res/bw_data_all.png',
           df.iloc[:,11:911].values, cmap=cm.binary_r, dpi=1)
for (li, l) in enumerate(limits):
    plt.imsave('res/bw_data_{0}.png'.format(li),
               df.iloc[l[0]:l[1],11:911].values, cmap=cm.binary_r, dpi=1)

# Color-coded images according to how many points it's possible to get
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

freq = df['freq']
points = [0, 5, 7, 10]

# accumulated counts according to game frequency
overall_f = dpts.apply(pd.value_counts, axis=1).fillna(0).mul(freq, axis=0)

# points according to each case (n large, 6 - n small)
ovfs = {}
ovfs['overall'] = 100 * overall_f.sum() / overall_f.sum().sum()
for (li, l) in enumerate(limits):
    ovf = overall_f.iloc[l[0]:l[1],:]
    ovfs['{}:{}'.format(li, 6 - li)] = 100 * ovf.sum() / ovf.sum().sum()
ovf = pd.DataFrame(ovfs).T.reset_index()
ovf.columns = ['case'] + [str(x) + ' points' for x in points]
#exp_val = ovf.mul(ovf.index.values, axis=0).sum() / 100
#exp_val.name = 'expected'
#ovf = pd.concat([ovf, pd.DataFrame(exp_val).T])
ovf.to_json('res/perc_overall.json', orient='split', double_precision=2)

# points for each game and for each target value, overall and separated by
# large number count
def weighted_value_counts(s, freq):
    s = s.values
    vals = defaultdict(lambda: 0)
    for (k, v) in enumerate(s):
        vals[v] += freq[k]
    res = pd.Series(vals.values(), index=vals.keys())
    return res / sum(vals.values())

(dpts.apply(pd.value_counts, normalize=True, axis=1).fillna(0) * 100).to_json(
    'res/perc_game.json', double_precision=2, orient='index')
(dpts.apply(weighted_value_counts, freq=freq, axis=0).fillna(0) * 100).to_json(
    'res/perc_val.json', double_precision=2)
for (li, l) in enumerate(limits):
    (dpts.iloc[l[0]:l[1],:].apply(
        pd.value_counts, normalize=True, axis=1).fillna(0) * 100).to_json(
        'res/perc_game_{0}.json'.format(li), double_precision=2, orient='index')
    (dpts.iloc[l[0]:l[1],:].apply(
        weighted_value_counts, freq=freq, axis=0).fillna(0) * 100).to_json(
        'res/perc_val_{0}.json'.format(li), double_precision=2)

# points according to presence of a given number in the inputs
elements = {str(x): x + 1 for x in range(10)}
elements['a'] = 25
elements['b'] = 50
elements['c'] = 75
elements['d'] = 100
nfs = {}
for c in '0123456789abcd':
    t = overall_f[list(c in x for x in overall_f.index)].sum()
    nfs[elements[c]] = 100 * t / t.sum()
nf = pd.DataFrame(nfs).T.reset_index()
nf.columns = ['numbers'] + [str(x) + ' points' for x in points]
nf.to_json('res/perc_by_number.json', orient='split', double_precision=2)

# Chance of getting the game 112233 given you chose 0 large
print(freq.iloc[limits[0][0]:limits[0][1]].sum() / float(freq['001122']))
# Perfectly solvable games (possible to get 10 points no matter the target)
perfect = [x for x in overall_f.itertuples() if sum(x[1:4]) < 1]
print(overall_f.sum().sum() / sum(x[4] for x in perfect))
# Perfect games with no large numbers
perf_small = [x for x in perfect if set(x[0]).isdisjoint({'a','b','c','d'})]
print(overall_f.sum().sum() / sum(x[4] for x in perf_small))
