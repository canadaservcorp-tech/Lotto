"""Meilleure utilisation de 60 $ au Lotto Max 7/52 : 10 mises = 10 lignes choisies (+30 choix rapides).
Compare 3 façons de choisir les 10 lignes par simulation de 300 000 tirages."""
import numpy as np
N, K, D = 52, 7, 300_000
rng = np.random.default_rng(2026)
ZERO = np.array([10, 20, 30, 40, 50])

def pool(X):
    d = np.diff(X, axis=1); od = (X % 2).sum(1); lo = (X <= 26).sum(1); s = X.sum(1)
    ok = ((d > 1).all(1) & ~np.isin(X, ZERO).any(1) & np.isin(od, (3, 4)) & np.isin(lo, (3, 4))
          & (s >= 150) & (s <= 220))
    ok &= np.max([(X % 10 == k).sum(1) for k in range(10)], 0) < 3
    ok &= np.max([((X - 1) // 10 == k).sum(1) for k in range(6)], 0) < 4
    ok &= (X[:, -1] - X[:, 0] >= 30) & (X[:, -1] >= 45) & (X[:, 0] <= 8) & ~(X <= 31).all(1)
    return ok

def hasard(n): return np.sort(np.argsort(rng.random((n, N)), axis=1)[:, :K] + 1, axis=1)

# A) 10 lignes de votre pool, choisies pour se chevaucher le MOINS possible
cand = hasard(2_000_000); cand = cand[pool(cand)]
choix = [cand[0]]
for _ in range(9):
    ov = np.max([np.isin(cand, c).sum(1) for c in choix], axis=0)          # pire chevauchement
    cov = np.isin(cand, np.concatenate(choix)).sum(1)                      # numéros déjà couverts
    choix.append(cand[np.lexsort((cov, ov))[0]])
A = np.array(choix)
# B) roue « 3 si 3 » sur 12 numéros (10 lignes très chevauchantes)
B = np.array([[3, 6, 12, 18, 28, 31, 34], [3, 6, 38, 41, 43, 45, 48], [12, 18, 28, 31, 38, 41, 43],
              [12, 18, 28, 34, 38, 45, 48], [3, 12, 31, 34, 41, 43, 45], [6, 18, 28, 31, 41, 45, 48],
              [6, 12, 31, 34, 38, 43, 48], [3, 18, 28, 34, 41, 43, 48], [3, 6, 18, 28, 38, 43, 45],
              [3, 6, 12, 34, 38, 41, 45]])
# C) 10 lignes au hasard (choix rapides)
C = hasard(10)

T = hasard(D)                                                                # tirages simulés
def evaluer(L):
    P = np.zeros((D, N + 1), bool); np.put_along_axis(P, T, True, axis=1)
    bons = np.stack([P[:, l].sum(1) for l in L], 1)                         # (tirages, 10 lignes)
    g = bons >= 3
    return g.any(1).mean(), g.sum(1).mean(), (bons >= 4).any(1).mean()

print('Numéros couverts / chevauchement max entre 2 lignes :')
for nom, L in [('A pool étalé', A), ('B roue 12 numéros', B), ('C hasard', C)]:
    ovm = max(len(set(a) & set(b)) for i, a in enumerate(L) for b in L[i + 1:])
    p1, moy, p4 = evaluer(L)
    print(f'{nom:18s} couverts {len(set(L.ravel())):2d}/52, chevauchement max {ovm} | '
          f'≥1 gain 6 $+ : {p1:.1%} | gains moyens/tirage : {moy:.3f} | ≥1 ligne 4+ bons : {p4:.2%}')
print('\nVos 10 lignes (option A) :'); [print(' ', list(map(int, l))) for l in A]
