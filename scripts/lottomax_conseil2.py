"""Conseil n°2 — réduire les 199 596 lignes (pool filtré ∩ gagnantes ≥ 6 $ au dernier tirage)."""
import itertools, math
import numpy as np, pandas as pd

N, K = 52, 7
ZERO = np.array([10, 20, 30, 40, 50])
def pool(X):
    d = np.diff(X, axis=1); od = (X % 2).sum(1); lo = (X <= 26).sum(1); s = X.sum(1)
    ok = ((d > 1).all(1) & ~np.isin(X, ZERO).any(1) & np.isin(od, (3, 4)) & np.isin(lo, (3, 4))
          & (s >= 150) & (s <= 220))
    ok &= np.max([(X % 10 == k).sum(1) for k in range(10)], 0) < 3
    ok &= np.max([((X - 1) // 10 == k).sum(1) for k in range(6)], 0) < 4
    ok &= (X[:, -1] - X[:, 0] >= 30) & (X[:, -1] >= 45) & (X[:, 0] <= 8) & ~(X <= 31).all(1)
    return ok

b = pd.read_csv('d/LOTTOMAX.csv')
m = b[b['SEQUENCE NUMBER'] == 0].sort_values('DRAW DATE').tail(10)       # 10 derniers tirages (7/52)
T = m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values; BON = m['BONUS NUMBER'].values

C5 = np.array(sorted(itertools.combinations(range(N), 5), key=lambda c: c[::-1]), np.uint8)
lignes = []                                                             # les 199 596 lignes
for a in range(1, N + 1):
    for z in range(a + 6, N + 1):
        n = math.comb(z - a - 1, 5)
        X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)]).astype(np.int16)
        X = X[pool(X)]
        if len(X): X = X[np.isin(X, T[-1]).sum(1) >= 3]
        if len(X): lignes.append(X)
L = np.vstack(lignes); assert len(L) == 199_596

bons = np.stack([np.isin(L, t).sum(1) for t in T], 1)                   # (lignes, 10 tirages)
bonus_last = (L == BON[-1]).any(1); k = bons[:, -1]
wins10 = (bons >= 3).sum(1)

options = [
    ('Gagnantes 20 $ et plus au dernier tirage (4/7, 3/7+c. et mieux)', ((k >= 4) | ((k == 3) & bonus_last)).sum()),
    ('Gagnantes 5/7 et plus au dernier tirage', (k >= 5).sum()),
    ('Gagnantes 6/7 au dernier tirage', (k >= 6).sum()),
    ('Gagnantes ≥ 6 $ aux 2 derniers tirages', ((bons[:, -1] >= 3) & (bons[:, -2] >= 3)).sum()),
    ('Gagnantes ≥ 6 $ aux 3 derniers tirages', (bons[:, -3:] >= 3).all(1).sum()),
    ('Gagnantes ≥ 6 $ dans 3+ des 10 derniers tirages', (wins10 >= 3).sum()),
    ('Gagnantes ≥ 6 $ dans 4+ des 10 derniers tirages', (wins10 >= 4).sum()),
]
res = pd.DataFrame(options, columns=['Option', 'Lignes restantes'])
res['Coût d\'un tirage (6 $ par ligne choisie)'] = res['Lignes restantes'] * 6
print(res.to_string(index=False, formatters={'Lignes restantes': '{:,}'.format,
      "Coût d'un tirage (6 $ par ligne choisie)": '{:,} $'.format}))
print('\nDistribution des gains sur 10 tirages :', dict(zip(*np.unique(wins10, return_counts=True))))
res.to_csv('conseil2_options.csv', index=False)
