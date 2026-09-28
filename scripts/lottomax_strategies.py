"""Lotto Max 7/52 — handicapping, filtrage de motifs, analyse de fréquence et roue (wheeling)
appliqués au pool restant : aucun consécutif + aucun 10/20/30/40/50.  Avec test honnête (walk-forward)."""
import itertools, math
from collections import Counter
import numpy as np, pandas as pd

N, K, ZERO = 52, 7, {10, 20, 30, 40, 50}
ALLOWED = [n for n in range(1, N + 1) if n not in ZERO]
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')].sort_values('DRAW DATE')
X = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1).tolist()
dates = m['DRAW DATE'].tolist()

def valide(l): return all(b - a > 1 for a, b in zip(l, l[1:])) and not set(l) & ZERO

# ---------- 1. Filtrage de motifs : distribution EXACTE dans le pool restant vs vrais tirages ----------
def distrib_pool():
    """DP exacte sur le pool : clé (nb impairs, nb bas 1-26, somme) → nombre de lignes."""
    f = {(0, False, 0, 0, 0): 1}
    for n in range(1, N + 1):
        g = Counter()
        for (k, prev, od, lo, s), v in f.items():
            g[(k, False, od, lo, s)] += v
            if n not in ZERO and not prev and k < K:
                g[(k + 1, True, od + n % 2, lo + (n <= 26), s + n)] += v
        f = g
    out = Counter()
    for (k, _, od, lo, s), v in f.items():
        if k == K: out[(od, lo, s)] += v
    return out

pool = distrib_pool(); TOTAL = sum(pool.values()); assert TOTAL == 25_470_555
def bande(s): return 'somme < 150' if s < 150 else ('somme 150-220' if s <= 220 else 'somme > 220')
motifs = []
for nom, cle in [('Impairs', lambda od, lo, s: od), ('Bas (1-26)', lambda od, lo, s: lo),
                 ('Somme', lambda od, lo, s: bande(s))]:
    cp = Counter(); cr = Counter()
    for (od, lo, s), v in pool.items(): cp[cle(od, lo, s)] += v
    XV = [r for r in X if valide(r)]                # vrais tirages qui auraient été dans le pool
    for r in XV: cr[cle(sum(x % 2 for x in r), sum(x <= 26 for x in r), sum(r))] += 1
    for val in sorted(cp, key=str):
        motifs.append([nom, val, cp[val], cp[val] / TOTAL, cr[val] / len(XV)])
motifs = pd.DataFrame(motifs, columns=['Motif', 'Valeur', 'Lignes du pool', '% du pool', '% vrais tirages (du pool)'])

# Filtre de motifs « équilibré » : 3-4 impairs, 3-4 bas, somme 150-220
eq = sum(v for (od, lo, s), v in pool.items() if od in (3, 4) and lo in (3, 4) and 150 <= s <= 220)
eq_reel = sum(1 for r in X if valide(r) and sum(x % 2 for x in r) in (3, 4)
              and sum(x <= 26 for x in r) in (3, 4) and 150 <= sum(r) <= 220)

# ---------- 2. Handicapping / fréquence : score de chaque numéro autorisé ----------
def scores(hist, fen=100):
    rec = hist[-fen:]; c = Counter(x for r in rec for x in r)
    last = {n: next((i for i, r in enumerate(reversed(hist)) if n in r), len(hist)) for n in ALLOWED}
    return pd.DataFrame([[n, c[n], c[n] / len(rec), last[n]] for n in ALLOWED],
                        columns=['Numéro', f'Sorties ({fen} dern.)', 'Taux', 'Retard (tirages)'])

# ---------- 3. Roue abrégée : garantie « 3 si 3 » sur v numéros, lignes valides seulement ----------
def roue(nums, t=3):
    nums = sorted(nums)
    cand = [c for c in itertools.combinations(nums, K) if valide(c)]
    a_couvrir = set(itertools.combinations(nums, t)); lignes = []
    while a_couvrir:
        best = max(cand, key=lambda c: len(a_couvrir & set(itertools.combinations(c, t))))
        gain = a_couvrir & set(itertools.combinations(best, t))
        if not gain: break                       # triplets impossibles à couvrir (ex. 2 consécutifs)
        lignes.append(best); a_couvrir -= gain
    return lignes, len(a_couvrir)

def choisir(hist, v, methode, rng):
    ordre = [n for n in scores(hist).sort_values(['Taux', 'Numéro'], ascending=[methode != 'chauds', True])['Numéro']]
    if methode == 'hasard': ordre = list(rng.permutation(ALLOWED))
    choix = []
    for n in ordre:                               # pas de consécutifs dans la sélection
        if all(abs(n - c) > 1 for c in choix): choix.append(int(n))
        if len(choix) == v: break
    return choix

# ---------- 4. Test walk-forward : 200 derniers tirages, 12 numéros, même roue ----------
V, TEST = 12, 200
rng = np.random.default_rng(3); res = {k: Counter() for k in ('chauds', 'froids', 'hasard')}
cache = {}
for i in range(len(X) - TEST, len(X)):
    hist, tirage = X[:i], set(X[i])
    for meth in res:
        nums = choisir(hist, V, meth, rng); key = tuple(nums)
        if key not in cache: cache[key] = roue(nums)[0]
        for l in cache[key]:
            res[meth][len(tirage & set(l))] += 1
        res[meth]['lignes'] += len(cache[key])
bt = pd.DataFrame([[meth, c['lignes'], sum(c[k] for k in range(3, 8)), sum(c[k] for k in range(4, 8)),
                    sum(c[k] for k in range(3, 8)) / c['lignes']] for meth, c in res.items()],
                  columns=['Méthode', 'Lignes jouées', 'Lignes 3+ bons', 'Lignes 4+ bons', 'Taux 3+ par ligne'])
p3 = sum(math.comb(7, k) * math.comb(45, 7 - k) for k in range(3, 8)) / math.comb(52, 7)

# ---------- 5. Proposition pour le prochain tirage ----------
sc = scores(X); prochains = choisir(X, V, 'chauds', rng); lignes, trou = roue(prochains)

with pd.ExcelWriter('lotto_max_strategies.xlsx') as w:
    motifs.to_excel(w, sheet_name='Motifs', index=False)
    sc.sort_values('Taux', ascending=False).to_excel(w, sheet_name='Handicap', index=False)
    pd.DataFrame(lignes, columns=[f'N{i}' for i in range(1, 8)]).to_excel(w, sheet_name='Roue', index=False)
    bt.to_excel(w, sheet_name='Backtest', index=False)

print(f'Pool restant : {TOTAL:,}')
print(f'Filtre équilibré (3-4 impairs, 3-4 bas, somme 150-220) : {eq:,} lignes ({eq/TOTAL:.1%} du pool) '
      f'| vrais tirages qui passent tout : {eq_reel/len(X):.1%}')
print(motifs.to_string(index=False, formatters={'% du pool': '{:.1%}'.format, '% vrais tirages (du pool)': '{:.1%}'.format}))
print(sc.sort_values('Taux', ascending=False).head(8).to_string(index=False))
print('\nBacktest', TEST, 'tirages :'); print(bt.to_string(index=False)); print(f'Théorie 3+ par ligne : {p3:.4f}')
print(f'\nRoue sur {prochains} : {len(lignes)} lignes, triplets non couverts : {trou}')
for l in lignes: print(l)
