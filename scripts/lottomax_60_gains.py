"""Plan 60 $ (10 lignes choisies « étalées » + 30 choix rapides) : gains min / max / distribution.
Valeurs des lots = tirage réel du 25 sept. 2026 (lotterycanada.com). 1 000 000 de tirages simulés."""
import numpy as np
N, D = 52, 1_000_000
rng = np.random.default_rng(60)
LOT = {'7': 65_000_000, '6+': 273_318, '6': 6_189, '5+': 1_215, '5': 125, '4+': 66, '4': 20, '3+': 20, '3': 6}
A = np.array([[5, 12, 14, 25, 33, 38, 52], [2, 8, 13, 32, 43, 49, 51], [1, 3, 21, 24, 28, 36, 46],
              [4, 9, 11, 22, 34, 39, 48], [7, 18, 23, 26, 29, 42, 47], [6, 15, 19, 37, 41, 44, 52],
              [8, 14, 16, 27, 31, 35, 45], [5, 17, 23, 31, 44, 46, 48], [2, 6, 11, 23, 28, 38, 45],
              [1, 6, 22, 25, 27, 42, 49]])

def tirer(n, k): return np.argsort(rng.random((n, N)), axis=1)[:, :k] + 1

gain = np.zeros(D); nb_gagnantes = np.zeros(D, int)
for bloc in range(0, D, 100_000):
    n = min(100_000, D - bloc)
    T8 = tirer(n, 8); T, B = T8[:, :7], T8[:, 7]                 # 7 numéros + complémentaire
    P = np.zeros((n, N + 1), bool); np.put_along_axis(P, T, True, axis=1)
    g = np.zeros(n)
    for l in list(A) + list(tirer(30, 7)):                         # 10 choisies + 30 choix rapides
        k = P[:, l].sum(1); bo = (l[None, :] == B[:, None]).any(1)
        v = np.select([k == 7, (k == 6) & bo, k == 6, (k == 5) & bo, k == 5, (k == 4) & bo, k == 4,
                       (k == 3) & bo, k == 3],
                      [LOT['7'], LOT['6+'], LOT['6'], LOT['5+'], LOT['5'], LOT['4+'], LOT['4'], LOT['3+'], LOT['3']], 0)
        g += v; nb_gagnantes[bloc:bloc + n] += v > 0
    gain[bloc:bloc + n] = g

tranches = [('0 $', gain == 0), ('6 à 19 $', (gain >= 6) & (gain < 20)), ('20 à 59 $', (gain >= 20) & (gain < 60)),
            ('60 à 99 $ (remboursé)', (gain >= 60) & (gain < 100)), ('100 à 999 $', (gain >= 100) & (gain < 1000)),
            ('1 000 $ et plus', gain >= 1000)]
for nom, m in tranches: print(f'{nom:22s} {m.mean():8.3%}')
print(f'Minimum simulé : {gain.min():,.0f} $ | Maximum simulé : {gain.max():,.0f} $ | Moyenne : {gain.mean():.2f} $')
print(f'Au moins 60 $ récupérés : {(gain >= 60).mean():.2%} | au moins 1 gain : {(gain > 0).mean():.1%}')
print(f'MAXPLUS (65 × 100 000 $) : 1 chance sur {133_784_560 / (40 * 65):,.0f} par tirage')
