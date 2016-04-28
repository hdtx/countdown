from __future__ import print_function
from collections import Counter
from itertools import permutations

def game_decoder(game):
    """
    Decode a game from a hashable compressed format (string) to a
    list of integers.
    String format:
    - numbers 0-9 represent 1-10
    - letters a, b, c, d represent 25, 50, 75, 100
    """
    res = []
    for c in game:
        if '0' <= c <= '9':
            res.append(ord(c) - ord('0') + 1)
        elif 'a' <= c <= 'd':
            res.append((ord(c) - ord('a') + 1) * 25)
        else:
            raise ValueError('invalid game component')
    return res

def gen_games(nlarge=range(5)):
    """
    Return a generator which yields the games, in sequential order. The format
    of the returned string is explained in the function game_decoder.
    Takes an optional parameter which represents the "large number" count in
    the games to be generated. For example, gen_games([0, 3]) returns all games
    with 0 or 3 large numbers.
    If the optional parameter is not provided, returns all possible games.
    """

    # Form the pool of small number cards
    sm_options = ''
    for i in range(10):
        sm_options += str(i) + str(i)
    # Form the pool of large number cards
    lg_options = 'abcd'

    for num_large in nlarge:
        num_small = 6 - num_large
        for sm_sel in permutations(sm_options, num_small):
            for lg_sel in permutations(lg_options, num_large):
                s = list(sm_sel) + list(lg_sel)
                s.sort()
                yield(''.join(s))

if __name__ == "__main__":
    nums = [None] * 5
    ntotal = 0
    nunique = 0
    for nlarge in range(5):
        nums[nlarge] = []
        for x in gen_games([nlarge]):
            nums[nlarge].append(x)
        print('{0:8} -> '.format(len(nums[nlarge])), end='')
        ntotal += len(nums[nlarge])

        nums[nlarge] = Counter(nums[nlarge])

        print(len(nums[nlarge]))
        nunique += len(nums[nlarge])

    print('Total games:  {0}'.format(ntotal))
    print('Unique games: {0}'.format(nunique))
    print('\nTesting the decoding:')
    g = list(nums[3].keys())
    print(g[0], game_decoder(g[0]))
    print(g[430], game_decoder(g[430]))
