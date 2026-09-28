"""Lotto Max 7/50 — élimination des combinaisons dont le « profil » n'est jamais sorti,
avec test honnête : filtres appris sur 2019-2023, vérifiés sur 2024-2026."""
import numpy as np, pandas as pd

N, K, SPLIT, SAMPLE = 50, 7, '2024-01-01', 3_000_000
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')
      & (b['DRAW DATE'] < '2026-04-14')].sort_values('DRAW DATE')   # ère 7/50 seulement
cols = [f'NUMBER DRAWN {i}' for i in range(1, 8)]
D = np.sort(m[cols].values, axis=1); dates = m['DRAW DATE'].values

def features(X):
    """X: (n,7) triées. Retourne dict de caractéristiques."""
    d = np.diff(X, axis=1)
    run = np.ones(len(X), int); cur = np.ones(len(X), int)
    for j in range(6):
        cur = np.where(d[:, j] == 1, cur + 1, 1); run = np.maximum(run, cur)
    dec = (X - 1) // 10
    return {
        'Somme': X.sum(1),
        'Nb impairs': (X % 2).sum(1),
        'Nb bas (1-25)': (X <= 25).sum(1),
        'Plus longue suite consécutive': run,
        'Nb dizaines différentes': np.array([len(set(r)) for r in dec]),
        'Étendue (max-min)': X[:, -1] - X[:, 0],
        'Max même dernier chiffre': np.array([np.bincount(r % 10).max() for r in X]),
        'Plus grand écart entre 2 numéros': d.max(1),
    }

rng = np.random.default_rng(42)
pool = np.sort(np.argsort(rng.random((SAMPLE, N)), axis=1)[:, :K] + 1, axis=1)  # combinaisons au hasard
fp = features(pool); fd = features(D)
train = dates < SPLIT; test = ~train

rows = []; keep_pool = np.ones(SAMPLE, bool); keep_test = np.ones(test.sum(), bool)
for name in fp:
    lo, hi = fd[name][train].min(), fd[name][train].max()
    ok_pool = (fp[name] >= lo) & (fp[name] <= hi)
    ok_test = (fd[name][test] >= lo) & (fd[name][test] <= hi)
    keep_pool &= ok_pool; keep_test &= ok_test
    rows.append([name, lo, hi, 1 - ok_pool.mean(), 1 - ok_test.mean()])

res = pd.DataFrame(rows, columns=['Filtre', 'Min observé', 'Max observé',
                                  '% combinaisons éliminées', '% vrais tirages futurs éliminés'])
total = pd.DataFrame([['TOUS LES FILTRES', '', '', 1 - keep_pool.mean(), 1 - keep_test.mean()]], columns=res.columns)
res = pd.concat([res, total], ignore_index=True)

# Vérificateur : quel filtre une combinaison échoue-t-elle ?
lo_hi = {k: (fd[k].min(), fd[k].max()) for k in fd}
past = {tuple(r) for r in D}
def verifier(combo):
    X = np.array([sorted(combo)]); f = features(X); out = []
    if tuple(X[0]) in past: out.append('déjà sortie')
    out += [k for k in f if not lo_hi[k][0] <= f[k][0] <= lo_hi[k][1]]
    return out or ['passe tous les filtres']

print(res.to_string(index=False, float_format=lambda x: f'{x:.1%}'))
print('entraînement', train.sum(), '| test', test.sum())
for c in [(1,2,3,4,5,6,7), (3,9,17,24,31,38,46)]: print(c, verifier(c))
res.to_csv('filtres_backtest.csv', index=False)
