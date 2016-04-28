from lang_analysis import gen_lang
from itertools import permutations, product, chain
from sys import version_info

def solve(nums, lang):
    assert(len(nums) == 6)
    solutions = {}
    for (lang_i, lang_vec) in enumerate(lang):
        if len(solutions) == 920:
            break
        nnums = lang_i + 2
        nops = lang_i + 1
        for numset in permutations(nums, nnums):
            if len(solutions) == 920:
                break
            for opset in product('+-*/', repeat=nops):
                if len(solutions) == 920:
                    break
                for word in lang_vec:
                    if len(solutions) == 920:
                        break
                    displayres = []
                    stack = []
                    iopset = chain(opset)
                    inumset = chain(numset)
                    for c in word:
                        if c == 'N':
                            x = (next(inumset) if version_info[0] == 3
                                 else inumset.next())
                            stack.append(x)
                        elif c == 'O':
                            x = (next(iopset) if version_info[0] == 3
                                 else iopset.next())
                            v1 = stack.pop()
                            v2 = stack.pop()
                            if x == '+':
                                stack.append(v1 + v2)
                            elif x == '-':
                                stack.append(v1 - v2)
                            # Ones are no good for * or /
                            elif v1 == 1 or v2 == 1:
                                break
                            elif x == '*':
                                stack.append(v1 * v2)
                            elif x == '/':
                                if v1 % v2 != 0:
                                    break
                                stack.append(v1 // v2)
                            else:
                                raise ValueError('invalid operator')
                        else:
                            raise ValueError('invalid character')
                        # Zero values are never interesting, because if there is
                        # a solution which involves a zero, there's a simpler
                        # one without it. Same for negative values.
                        if stack[-1] <= 0:
                            break
                        displayres.append(x)
                    else:
                        # only check the result if we did not break out of the
                        # for loop
                        res = stack.pop()
                        if 90 <= res <= 1009 and res not in solutions:
                            solutions[res] = displayres
    return solutions

if __name__ == "__main__":
    lang = gen_lang()
    sol = solve([25, 50, 75, 100, 3, 6], lang)
    print(sol)
    print(len(sol))
