"""Lotto Max 7/52 — éliminer TOUTE combinaison contenant des numéros consécutifs (suites de 2 à 7)."""
import math, numpy as np, pandas as pd

N, K = 52, 7
TOTAL = math.comb(N, K)
RESTE = math.comb(N - K + 1, K)          # formule exacte : lignes sans aucun numéro consécutif = C(46,7)

def a_des_consecutifs(ligne):
    s = sorted(ligne); return any(b - a == 1 for a, b in zip(s, s[1:]))

def generer(n, seed=None):
    """Tire n lignes au hasard, uniformément, parmi les lignes SANS consécutifs :
    on choisit 7 numéros parmi 1..46, puis on ajoute 0,1,2,…,6 → chaque écart devient ≥ 2."""
    rng = np.random.default_rng(seed)
    return [sorted(int(x) + i for i, x in enumerate(sorted(rng.choice(N - K + 1, K, replace=False) + 1)))
            for _ in range(n)]

b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')]
reels = m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values.tolist()
sans = sum(not a_des_consecutifs(r) for r in reels)

print(f'Total 7/52          : {TOTAL:,}')
print(f'Éliminées           : {TOTAL - RESTE:,} ({(TOTAL - RESTE) / TOTAL:.2%})')
print(f'RESTANTES           : {RESTE:,} ({RESTE / TOTAL:.2%})')
print(f'Vrais tirages sans consécutifs : {sans} sur {len(reels)} ({sans / len(reels):.1%})')
for l in generer(4, seed=1): print('Exemple :', l, '| consécutifs ?', a_des_consecutifs(l))
