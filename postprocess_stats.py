from __future__ import print_function
import pandas as pd

def load_from_stats_file(fname):
    with open(fname) as f:
        print(fname)
        exec('games=' + f.readline())
        glist, gfreq = zip(*games)
        gdata = []
        for l in f:
            exec('game=' + l.split('#')[3])
            ind = [False] * 920
            for g in game:
                ind[g[0] - 90] = True
            gdata.append(ind)
    # glist: list of games in short form ('0011aa', '0011ab', etc.)
    # gfreq: list of frequencies for each game
    # gdata: list of lists, each element gdata[i][j] is a bool indicating
    #        whether there's a solution for the game i with the value (j + 90)
    cols = ['freq'] + list(range(90, 1010))
    data = [[x[0]] + x[1] for x in zip(gfreq, gdata)]
    return pd.DataFrame(data, index=glist, columns=cols)

if __name__ == "__main__":
    dfs = []
    for nlarge in range(5):
        dfs.append(load_from_stats_file('stats{0}.txt'.format(nlarge)))
    dfs = pd.concat(dfs)
    pd.DataFrame(dfs, dtype='int32').to_csv('stats.txt', index_label='game')
    # load with:
    # df = pd.read_csv('stats.txt', index_col=0, dtype={'game': 'str'})