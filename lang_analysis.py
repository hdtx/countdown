from math import factorial as fac

def lang_k_rec(available_o, available_n, k, x, possible):
    if available_n > 0:
        lang_k_rec(available_o, available_n - 1, k + 'N', x + 1, possible)
    if available_o > 0 and x > 1:
        lang_k_rec(available_o - 1, available_n, k + 'O', x - 1, possible)
    if available_o == 0 and available_n == 0:
        possible.append('NN' + k + 'O')

def gen_lang():
    possible_k = [[], [], [], [], []]
    for av in range(5):
        lang_k_rec(av, av, '', 2, possible_k[av])
        possible_k[av].sort()
    return possible_k

if __name__ == "__main__":
    ntotal = 0
    possible_k = gen_lang()
    for av in range(5):
        print(possible_k[av])
        l = len(possible_k[av])
        print(l, 'words')
        n = 4**(1 + av) * (fac(6) // fac(4 - av)) * l
        ntotal += n
        print(n, 'possibilities\n')
    print(ntotal, 'total possibilities')
