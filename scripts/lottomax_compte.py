"""Compte EXACT des combinaisons Lotto Max qui restent après les filtres « jamais sorti »."""
import itertools, math, time
import numpy as np, pandas as pd

b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')
      & (b['DRAW DATE'] < '2026-04-14')]
D = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1)

def feats(X):
    X = X.astype(np.int16); d = np.diff(X, axis=1)
    run = np.ones(len(X), np.int8); cur = np.ones(len(X), np.int8)
    for j in range(6):
        cur = np.where(d[:, j] == 1, cur + 1, 1); run = np.maximum(run, cur)
    dec = (X - 1) // 10
    return {'Somme': X.sum(1), 'Nb impairs': (X % 2).sum(1), 'Nb bas (1-25)': (X <= 25).sum(1),
            'Suite consécutive': run,
            'Dizaines': sum((dec == k).any(1) for k in range(6)),
            'Étendue': X[:, -1] - X[:, 0],
            'Même dernier chiffre': np.max([(X % 10 == k).sum(1) for k in range(10)], axis=0),
            'Plus grand écart': d.max(1)}

R = {k: (v.min(), v.max()) for k, v in feats(D).items()}   # plages jamais dépassées (722 tirages)

# combinaisons de 5 parmi 0..49 en ordre « colex » : les C(L,5) premières n'utilisent que 0..L-1
C5 = np.array(sorted(itertools.combinations(range(50), 5), key=lambda c: c[::-1]), np.uint8)

def compter(N):
    total = kept = 0; par_filtre = dict.fromkeys(R, 0)
    for a in range(1, N + 1):
        for z in range(a + 6, N + 1):
            n = math.comb(z - a - 1, 5); total += n
            mid = C5[:n].astype(np.int16) + a + 1
            X = np.column_stack([np.full(n, a), mid, np.full(n, z)])
            f = feats(X); ok = np.ones(n, bool)
            for k, (lo, hi) in R.items():
                o = (f[k] >= lo) & (f[k] <= hi); par_filtre[k] += (~o).sum(); ok &= o
            kept += ok.sum()
    return total, kept, par_filtre

# Jeu 7/52 : les maximums « Dizaines = 5 » et « Étendue = 49 » venaient du fait que 51-52 n'existaient pas.
# On les relâche pour ne pas éliminer des combinaisons à cause d'une règle de l'ancien jeu.
R50 = dict(R); R52 = dict(R, Dizaines=(R['Dizaines'][0], 6), Étendue=(R['Étendue'][0], 51))
n52 = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2026-04-14')]
D52 = np.sort(n52[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1)
for nom, RR in (('strictes 7/50', R50), ('corrigées 7/52', R52)):
    f = feats(D52); ok = np.ones(len(D52), bool)
    for k, (lo, hi) in RR.items(): ok &= (f[k] >= lo) & (f[k] <= hi)
    print(f'Vrais tirages 7/52 éliminés par les plages {nom} : {(~ok).sum()} sur {len(D52)}')

for N, R in ((50, R50), (52, R52)):
    t = time.time(); total, kept, pf = compter(N)
    passe = kept - (len(D) if N == 50 else 0)   # anciennes combinaisons gagnantes (toutes passent les filtres)
    print(f'\n=== 7/{N} : {total:,} combinaisons ({time.time()-t:.0f}s)')
    for k, v in pf.items(): print(f'  {k:22s} élimine {v:>12,}  ({v/total:.3%})')
    print(f'  RESTANT : {passe:,}  ({passe/total:.2%}) | éliminées : {total-passe:,}')
print('Plages:', R)
