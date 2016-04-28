from __future__ import print_function
from collections import Counter
from count_games import gen_games, game_decoder
from lang_analysis import gen_lang
from game_solver import solve

if __name__ == "__main__":
    lang = gen_lang()

    nlarge = 1
    games = Counter()
    for x in gen_games([nlarge]):
        games.update([x])
    games = list(games.items())
    games.sort()
    print('Generated {0} games, starting...'.format(len(games)))

    solved = 0
    unsolved = 0
    with open('stats{0}.txt'.format(nlarge), 'w', buffering=1) as f:
        print(games, file=f)
        for (game, freq) in games:
            g = game_decoder(game)
            for n in g:
                f.write('{0:3} '.format(n))
            sol = solve(g, lang).items()
            sol.sort()
            f.write('# {0} '.format(freq))
            solved += len(sol) * freq
            unsolved += (920 - len(sol)) * freq
            f.write('# {0} # '.format(solved))
            print(sol, file=f)
            print(g, end=' ')
            print(len(sol))
