"""Lotto Max 7/52 — filtres supplémentaires proposés par le « conseil », comptés EXACTEMENT
sur le pool actuel (aucun consécutif, aucun …0, 3-4 impairs, 3-4 bas, somme 150-220)."""
import itertools, math
import numpy as np, pandas as pd

N, K = 52, 7
ZERO = np.array([10, 20, 30, 40, 50])
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')]
REEL = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1)

def pool_actuel(X):
    d = np.diff(X, axis=1); od = (X % 2).sum(1); lo = (X <= 26).sum(1); s = X.sum(1)
    return ((d > 1).all(1) & ~np.isin(X, ZERO).any(1) & np.isin(od, (3, 4))
            & np.isin(lo, (3, 4)) & (s >= 150) & (s <= 220))

FILTRES = {   # True = on ÉLIMINE la ligne
    'Anniversaires : les 7 numéros ≤ 31':          lambda X: (X <= 31).all(1),
    '3+ numéros avec la même finale':              lambda X: np.max([(X % 10 == k).sum(1) for k in range(10)], 0) >= 3,
    '4+ numéros dans la même dizaine':             lambda X: np.max([((X - 1) // 10 == k).sum(1) for k in range(6)], 0) >= 4,
    'Étendue < 30 (numéros trop groupés)':         lambda X: X[:, -1] - X[:, 0] < 30,
    'Aucun numéro ≥ 45 ou aucun ≤ 8 (bords vides)': lambda X: (X[:, -1] < 45) | (X[:, 0] > 8),
}

C5 = np.array(sorted(itertools.combinations(range(N), 5), key=lambda c: c[::-1]), np.uint8)
base = 0; seul = dict.fromkeys(FILTRES, 0); tous = 0
for a in range(1, N + 1):
    for z in range(a + 6, N + 1):
        n = math.comb(z - a - 1, 5)
        X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)]).astype(np.int16)
        X = X[pool_actuel(X)]
        if not len(X): continue
        base += len(X); garde = np.ones(len(X), bool)
        for k, f in FILTRES.items():
            e = f(X); seul[k] += e.sum(); garde &= ~e
        tous += garde.sum()
assert base == 7_496_713

rows = []; pool_r = pool_actuel(REEL.astype(np.int16)); garde_r = pool_r.copy(); r0 = pool_r.sum()
for k, f in FILTRES.items():
    e_r = f(REEL.astype(np.int16)) & pool_r      # chaque filtre seul
    rows.append([k, seul[k], seul[k] / base, e_r.sum() / r0])
    garde_r &= ~f(REEL.astype(np.int16))
res = pd.DataFrame(rows, columns=['Filtre', 'Lignes éliminées', '% du pool', '% des vrais tirages du pool éliminés'])
print(res.to_string(index=False, formatters={'Lignes éliminées': '{:,}'.format,
      '% du pool': '{:.1%}'.format, '% des vrais tirages du pool éliminés': '{:.1%}'.format}))
print(f'\nPool de départ : {base:,} | après TOUS les filtres : {tous:,} ({tous/math.comb(N, K):.2%} du total)')
print(f'Vrais tirages : {r0} dans le pool de départ, {garde_r.sum()} après tous les filtres (sur {len(REEL)})')
res.to_csv('conseil_filtres.csv', index=False)
