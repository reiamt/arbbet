import pandas as pd

from bwin_funcs import Bwin
from bah_funcs import BAH

bwin = Bwin()
bwin_games = bwin.get_football_games()

bah = BAH()
bah_games = bah.get_football_bets()

result_merge = pd.merge(bwin_games, bah_games, on=['Team1','Team2'])

cols = ['1_bwin', 'X_bwin', '2_bwin', '1_bah', 'X_bah', '2_bah']
possibilities = [[True, True, True, False, False, False],
                 [False, False, False, True, True, True],
                 [True, True, False, False, False, True],
                 [True, False, False, False, True, True],
                 [False, True, True, True, False, False],
                 [False, False, True, True, True, False],
                 [True, False, True, False, True, False]]
def f(x):
    a, b, c = x
    return 1/a+1/b+1/c

for i, possibility in enumerate(possibilities):
    tmp = [c for p, c in zip(possibility, cols) if p]
    result_merge['ip_'+str(i)] = result_merge[tmp].apply(f, axis=1, result_type='expand')

print(result_merge[cols].min())
print(result_merge[cols].idxmin())


print(result_merge)
#print(result)