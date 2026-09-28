"""Lotto Max — batterie de tests d'aléa sur les VRAIS tirages (d/LOTTOMAX.csv), par ère (7/49, 7/50, 7/52).

Chaque statistique est calculée sur les tirages réels puis sur S historiques simulés de même taille
(tirage uniforme sans remise) : la p-valeur est la fraction des simulations au moins aussi extrêmes
(bilatérale). Aucune hypothèse de loi asymptotique -> valable même pour la petite ère 7/52.

Tests : fréquence des numéros, fréquence du complémentaire, fréquence des paires, somme (moyenne et
écart-type), répétitions du tirage précédent, écart max sans sortie (« retard »), autocorrélation lag 1 des
sommes, nb de paires consécutives, nb d'impairs, nb de bas, étendue, série de sommes au-dessus de la médiane
(runs), et test prédictif : la fréquence de la 1re moitié prédit-elle la 2e moitié (corrélation) ?

Usage : python lottomax_randomness.py [--sims 4000] [--seed 7] [--out .]
"""
import argparse
import numpy as np, pandas as pd

ERAS = [('7/49', '2009-09-25', '2019-05-14', 49), ('7/50', '2019-05-14', '2026-04-14', 50),
        ('7/52', '2026-04-14', '2100-01-01', 52)]
K = 7


def charger(path='d/LOTTOMAX.csv'):
    b = pd.read_csv(path)
    m = b[b['SEQUENCE NUMBER'] == 0].sort_values('DRAW DATE')
    X = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1).astype(np.int16)
    return m, X, m['BONUS NUMBER'].values.astype(np.int16)


def simuler(rng, S, D, N):
    """S historiques de D tirages : 7 numéros triés + complémentaire."""
    T8 = np.argsort(rng.random((S, D, N)), axis=2)[:, :, :8] + 1
    return np.sort(T8[:, :, :7], axis=2).astype(np.int16), T8[:, :, 7].astype(np.int16)


def occ(X, N):
    """(S,D,7) -> (S,N) comptes par numéro."""
    P = np.zeros(X.shape[:-1] + (N + 1,), np.int32)
    np.put_along_axis(P, X.astype(np.int64), 1, axis=-1)
    return P[..., 1:].sum(1)


def pair_chi2(X, N):
    S, D, _ = X.shape
    i, j = np.triu_indices(K, 1)
    a, b = X[..., i], X[..., j]                                   # (S,D,21)
    idx = (a - 1) * N + (b - 1)
    C = np.zeros((S, N * N), np.int32)
    for s in range(S): C[s] = np.bincount(idx[s].ravel(), minlength=N * N)
    ii, jj = np.triu_indices(N, 1); C = C[:, ii * N + jj]
    e = D * 21 / (N * (N - 1) / 2)
    return ((C - e) ** 2 / e).sum(1)


def runs(sig):
    """nb de séquences dans une suite booléenne (S,D)."""
    return 1 + (sig[:, 1:] != sig[:, :-1]).sum(1)


def stats(X, B, N):
    """X:(S,D,7) B:(S,D). Retourne dict nom -> (S,) statistiques."""
    S, D, _ = X.shape
    O = occ(X, N); eN = D * K / N
    s = X.sum(2).astype(float)
    rep = (X[:, 1:, :, None] == X[:, :-1, None, :]).any(3).sum(2)          # répétitions vs tirage précédent
    # retard max : plus grand écart entre deux sorties d'un même numéro (toutes les positions)
    pres = np.zeros((S, D, N + 1), bool); np.put_along_axis(pres, X.astype(np.int64), True, axis=2)
    retard = np.zeros(S)
    for k in range(S):
        r = 0
        for n in range(1, N + 1):
            t = np.flatnonzero(pres[k, :, n])
            if len(t) > 1: r = max(r, int(np.diff(t).max()))
        retard[k] = r
    med = np.median(s, axis=1, keepdims=True)
    h1, h2 = occ(X[:, :D // 2], N), occ(X[:, D // 2:], N)
    corr_pred = np.array([np.corrcoef(h1[k], h2[k])[0, 1] for k in range(S)])
    ac = np.array([np.corrcoef(s[k, :-1], s[k, 1:])[0, 1] for k in range(S)])
    return {
        'chi² fréquence des 7 numéros': ((O - eN) ** 2 / eN).sum(1),
        'chi² fréquence du complémentaire': ((occ(B[..., None], N) - D / N) ** 2 / (D / N)).sum(1),
        'chi² fréquence des paires': pair_chi2(X, N),
        'somme : moyenne': s.mean(1), 'somme : écart-type': s.std(1),
        'répétitions du tirage précédent (moy.)': rep.mean(1),
        'retard max d’un numéro (tirages)': retard,
        'autocorrélation lag 1 des sommes': ac,
        'nb paires consécutives (moy.)': (np.diff(X, axis=2) == 1).sum(2).mean(1),
        'nb impairs (moy.)': (X % 2).sum(2).mean(1),
        'nb bas ≤ N/2 (moy.)': (X <= N // 2).sum(2).mean(1),
        'étendue max-min (moy.)': (X[:, :, -1] - X[:, :, 0]).mean(1),
        'runs des sommes > médiane': runs(s > med).astype(float),
        'prédictif : corr(fréq. 1re moitié, 2e moitié)': corr_pred,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sims', type=int, default=4000); ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--out', default='.')
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)
    m, X, B = charger(); rows = []
    for nom, d0, d1, N in ERAS:
        sel = ((m['DRAW DATE'] >= d0) & (m['DRAW DATE'] < d1)).values
        Xr, Br = X[sel][None], B[sel][None]; D = sel.sum()
        assert Xr.max() <= N
        print(f'\n=== Ère {nom} : {D} tirages ({m["DRAW DATE"][sel].min()} → {m["DRAW DATE"][sel].max()}) ===')
        real = stats(Xr, Br, N)
        sim = {k: [] for k in real}
        for b0 in range(0, a.sims, 200):                           # par blocs pour la mémoire
            Xs, Bs = simuler(rng, min(200, a.sims - b0), D, N)
            for k, v in stats(Xs, Bs, N).items(): sim[k].append(v)
        for k in real:
            v = np.concatenate(sim[k]); r = float(real[k][0])
            p = 2 * min((v >= r).mean(), (v <= r).mean()); p = min(1.0, p + 1 / len(v))
            rows.append([nom, k, r, v.mean(), v.std(), p])
            flag = ' <-- p < 0.05' if p < 0.05 else ''
            print(f'{k:48s} réel {r:10.3f} | simulé {v.mean():10.3f} ± {v.std():8.3f} | p = {p:.3f}{flag}')
    res = pd.DataFrame(rows, columns=['ère', 'test', 'réel', 'simulé moyenne', 'simulé écart-type', 'p-valeur'])
    n, n05 = len(res), (res['p-valeur'] < 0.05).sum()
    print(f'\n{n} tests, {n05} avec p < 0.05 (attendu sous pur hasard : ≈ {0.05 * n:.1f}). '
          f'p minimale = {res["p-valeur"].min():.4f} ; seuil de Bonferroni = {0.05 / n:.4f}')
    verdict = 'AUCUN biais exploitable détecté' if res['p-valeur'].min() > 0.05 / n else 'ANOMALIE à examiner'
    print(f'Verdict : {verdict}.')
    res.to_csv(f'{a.out}/randomness_tests.csv', index=False)
    print(f'Écrit : {a.out}/randomness_tests.csv')


if __name__ == '__main__':
    main()
