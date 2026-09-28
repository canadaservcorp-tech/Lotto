"""Lotto Max 7/52 — les numéros finissant par 0 (10, 20, 30, 40, 50) sortent-ils moins ?
Puis compte exact des lignes SANS consécutifs ET SANS ces numéros."""
import math, numpy as np, pandas as pd

N, K = 52, 7
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2019-05-14')]
X = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1)
dates = m['DRAW DATE'].values
n50 = (dates < '2026-04-14').sum(); n52 = len(dates) - n50

# 1) Fréquence par numéro, avec le bon nombre de tirages selon le jeu (1-50 puis 1-52)
def attendu(n):  # chances : 7/50 pendant l'ère 7/50 (si n<=50), 7/52 pendant l'ère 7/52
    return (n50 * 7 / 50 if n <= 50 else 0) + n52 * 7 / 52

rows = []
for d in range(10):
    nums = [n for n in range(1, N + 1) if n % 10 == d]
    obs = sum((X == n).sum() for n in nums); att = sum(attendu(n) for n in nums)
    rows.append([f'…{d}', ', '.join(map(str, nums)), obs, round(att, 1), obs / att])
freq = pd.DataFrame(rows, columns=['Finale', 'Numéros', 'Sorties', 'Attendu', 'Ratio'])

# 2) Compte exact (programmation dynamique) : 7 numéros, aucun consécutif, numéros interdits exclus
def compter(interdits):
    # f[k][ok] = nb de façons ; on parcourt 1..52, ok = dernier numéro choisi est le précédent
    f = {(0, False): 1}
    for n in range(1, N + 1):
        g = {}
        for (k, prev), v in f.items():
            g[(k, False)] = g.get((k, False), 0) + v                    # on ne prend pas n
            if n not in interdits and not prev and k < K:
                g[(k + 1, True)] = g.get((k + 1, True), 0) + v          # on prend n
        f = g
    return sum(v for (k, _), v in f.items() if k == K)

ZERO = {10, 20, 30, 40, 50}
total, sans_suite, sans_suite_ni_0 = math.comb(N, K), compter(set()), compter(ZERO)

def ok(r, interdits):
    return all(b - a > 1 for a, b in zip(r, r[1:])) and not set(r) & interdits
reel_a = sum(ok(r, set()) for r in X); reel_b = sum(ok(r, ZERO) for r in X)

print(freq.to_string(index=False, formatters={'Ratio': '{:.2f}'.format}))
print(f'\nTotal                              : {total:,}')
print(f'Sans consécutifs                   : {sans_suite:,} ({sans_suite/total:.2%}) | vrais tirages : {reel_a/len(X):.1%}')
print(f'Sans consécutifs ET sans 10-20-30-40-50 : {sans_suite_ni_0:,} ({sans_suite_ni_0/total:.2%}) | vrais tirages : {reel_b/len(X):.1%}')
