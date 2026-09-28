"""Lotto Max 7/52 — élimination des « séries » : suites consécutives et progressions arithmétiques.
Compte exact (suites) + estimation par échantillon (progressions) + fréquence dans les vrais tirages."""
import itertools, math
import numpy as np, pandas as pd

N, K = 52, 7
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')]      # 7/50 + 7/52 : 770 tirages
D = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1)

def plus_longue_suite(X):
    d = np.diff(X, axis=1); run = np.ones(len(X), np.int8); cur = run.copy()
    for j in range(6):
        cur = np.where(d[:, j] == 1, cur + 1, 1); run = np.maximum(run, cur)
    return run

def plus_longue_progression(X, maxL=7):
    """Plus longue progression arithmétique (même écart, pas consécutif exigé) dans chaque ligne."""
    P = np.zeros((len(X), N + 1), bool); np.put_along_axis(P, X, True, axis=1)
    best = np.full(len(X), 2, np.int8)
    for L in range(3, maxL + 1):
        found = np.zeros(len(X), bool)
        for d in range(1, (N - 1) // (L - 1) + 1):
            span = (L - 1) * d; acc = P[:, 1:N + 1 - span].copy()
            for t in range(1, L): acc &= P[:, 1 + t * d:N + 1 - span + t * d]
            found |= acc.any(1)
        best[found] = L
    return best

# 1) Compte EXACT des plus longues suites consécutives sur les 133 784 560 combinaisons
C5 = np.array(sorted(itertools.combinations(range(N), 5), key=lambda c: c[::-1]), np.uint8)
exact = np.zeros(8, np.int64)
for a in range(1, N + 1):
    for z in range(a + 6, N + 1):
        n = math.comb(z - a - 1, 5)
        X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)])
        exact += np.bincount(plus_longue_suite(X), minlength=8)
TOT = math.comb(N, K); assert exact.sum() == TOT

# 2) Progressions arithmétiques : échantillon de 2 000 000 combinaisons (estimation)
rng = np.random.default_rng(7); S = 2_000_000
pool = np.sort(np.argsort(rng.random((S, N)), axis=1)[:, :K] + 1, axis=1)
ap_pool = np.bincount(plus_longue_progression(pool), minlength=8) / S
ap_real = np.bincount(plus_longue_progression(D), minlength=8) / len(D)
run_real = np.bincount(plus_longue_suite(D), minlength=8) / len(D)

rows = []
for L in range(2, 8):
    elim = exact[L:].sum()
    rows.append([f'Suite consécutive de {L}+ (ex. {", ".join(map(str, range(10, 10 + L)))})',
                 elim, elim / TOT, run_real[L:].sum()])
AP7 = sum(N - 6 * d for d in range(1, 9))          # exact : 7 numéros en progression parfaite
for L in range(3, 8):
    est = AP7 if L == 7 else round(ap_pool[L:].sum() * TOT)    # 3 à 6 termes : estimation (échantillon)
    rows.append([f'Progression de {L}+ termes (ex. {", ".join(str(5 + 4 * i) for i in range(L))})',
                 est, est / TOT, ap_real[L:].sum()])
res = pd.DataFrame(rows, columns=['Série éliminée', 'Combinaisons éliminées (7/52)',
                                  '% des combinaisons', '% des vrais tirages qui avaient ce motif'])
print(res.to_string(index=False, formatters={'Combinaisons éliminées (7/52)': '{:,}'.format,
      '% des combinaisons': '{:.3%}'.format, '% des vrais tirages qui avaient ce motif': '{:.1%}'.format}))
res.to_csv('series_elimination.csv', index=False)
