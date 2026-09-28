"""Lotto Max 7/52 — combien de combinaisons gagnent au moins 6 $ (3/7 = participation gratuite) ?
1) Formule exacte pour N'IMPORTE QUEL tirage.  2) Votre pool de 4 314 139 lignes face au dernier tirage."""
import itertools, math
import numpy as np, pandas as pd

N, K = 52, 7
C = math.comb
TIERS = [  # (catégorie, bons numéros, bonus ?, lot)
    ('7/7', 7, False, 'Gros lot'), ('6/7 + compl.', 6, True, 'Part du fonds'),
    ('6/7', 6, False, 'Part du fonds'), ('5/7 + compl.', 5, True, 'Part du fonds'),
    ('5/7', 5, False, 'Part du fonds'), ('4/7 + compl.', 4, True, 'Part du fonds'),
    ('4/7', 4, False, '20 $'), ('3/7 + compl.', 3, True, '20 $'), ('3/7', 3, False, 'Participation gratuite (6 $)')]

def nb_lignes(k, bonus):   # 7 gagnants, 1 complémentaire, 44 autres
    return C(7, k) * (C(44, 7 - k - 1) if bonus else C(44, 7 - k))

rows = [[t, lot, nb_lignes(k, bo)] for t, k, bo, lot in TIERS]
formule = pd.DataFrame(rows, columns=['Catégorie', 'Lot', 'Lignes gagnantes (sur 133 784 560)'])

# 2) Votre pool (tous les filtres) face au dernier tirage
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
last = b[b['SEQUENCE NUMBER'] == 0].sort_values('DRAW DATE').iloc[-1]
W = np.array([last[f'NUMBER DRAWN {i}'] for i in range(1, 8)]); BON = last['BONUS NUMBER']

C5 = np.array(sorted(itertools.combinations(range(N), 5), key=lambda c: c[::-1]), np.uint8)
taille = 0; gains = dict.fromkeys([t for t, *_ in TIERS], 0)
for a in range(1, N + 1):
    for z in range(a + 6, N + 1):
        n = C(z - a - 1, 5)
        X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)]).astype(np.int16)
        X = X[pool(X)]
        if not len(X): continue
        taille += len(X); k = np.isin(X, W).sum(1); bo = (X == BON).any(1)
        for t, kk, bb, _ in TIERS:
            gains[t] += ((k == kk) & (bo == bb if kk < 7 else True)).sum()
assert taille == 4_314_139

formule['Votre pool, tirage du ' + last['DRAW DATE']] = [gains[t] for t, *_ in TIERS]
tot_all = formule.iloc[:, 2].sum(); tot_pool = sum(gains.values())
print(f"Dernier tirage {last['DRAW DATE']} : {sorted(W.tolist())} compl. {BON}")
print(formule.to_string(index=False, formatters={formule.columns[2]: '{:,}'.format, formule.columns[3]: '{:,}'.format}))
print(f'\nTOTAL ≥ 6 $ : {tot_all:,} lignes sur 133 784 560 ({tot_all / C(N, K):.2%})')
print(f'Votre pool  : {tot_pool:,} lignes sur {taille:,} ({tot_pool / taille:.2%})')
formule.to_csv('lignes_gagnantes.csv', index=False)
