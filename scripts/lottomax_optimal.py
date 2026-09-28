"""Lotto Max 7/52 — sélection « optimale » de N lignes (défaut 10) par optimisation gloutonne.

1. Charge d/LOTTOMAX.csv et vérifie l'ère de jeu courante (7/52, 6 $ = 4 lignes).
2. Énumère les 133 784 560 combinaisons (même vectorisation que lottomax_conseil.py).
3. Garde les candidates au profil « impopulaire » puis choisit N lignes une à une :
   chevauchement ≤ 1 avec les lignes déjà prises, ≥ 2 numéros > 31, exactement une paire consécutive,
   somme 150-230, ≥ 4 dizaines, pas toutes ≤ 31, pas de série arithmétique.
4. Rapport de couverture + Monte Carlo (approche de lottomax_60_gains.py) : « gagne quelque chose »,
   « remboursé », retour moyen — pour les N lignes + 3N choix rapides (6 $ = 1 ligne choisie + 3 QP).
5. Écrit optimal_lines.csv et optimal_comparison.csv (vs conseil-9 et étalées-10 du handoff).

Usage : python lottomax_optimal.py [--n 10] [--draws 300000] [--seed 2026] [--out .]
"""
import argparse, itertools, math, time
import numpy as np, pandas as pd

N_MAX, K = 52, 7
TOTAL = math.comb(N_MAX, K)                       # 133 784 560
ERA3_START, PLAY_PRICE, LINES_PER_PLAY = '2026-04-14', 6, 4
LOT = {'7': 65_000_000, '6+': 273_318, '6': 6_189, '5+': 1_215, '5': 125, '4+': 66, '4': 20, '3+': 20, '3': 6}

CONSEIL9 = np.array([[1, 6, 8, 12, 37, 41, 52], [1, 8, 12, 14, 37, 41, 52], [1, 6, 8, 17, 37, 41, 52],
                     [1, 8, 14, 17, 37, 41, 52], [1, 8, 12, 17, 39, 41, 52], [1, 8, 12, 37, 39, 41, 52],
                     [6, 8, 12, 17, 37, 41, 52], [8, 12, 14, 17, 37, 41, 52], [8, 12, 17, 37, 39, 41, 52]])
ETALEES10 = np.array([[5, 12, 14, 25, 33, 38, 52], [2, 8, 13, 32, 43, 49, 51], [1, 3, 21, 24, 28, 36, 46],
                      [4, 9, 11, 22, 34, 39, 48], [7, 18, 23, 26, 29, 42, 47], [6, 15, 19, 37, 41, 44, 52],
                      [8, 14, 16, 27, 31, 35, 45], [5, 17, 23, 31, 44, 46, 48], [2, 6, 11, 23, 28, 38, 45],
                      [1, 6, 22, 25, 27, 42, 49]])


# ---------------------------------------------------------------- 1. données + ère
def charger(path='d/LOTTOMAX.csv'):
    b = pd.read_csv(path)
    m = b[b['SEQUENCE NUMBER'] == 0].copy()
    X = np.sort(m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values, axis=1).astype(np.int16)
    return m, X


def verifier_ere(m, X):
    rec = m['DRAW DATE'] >= ERA3_START
    if rec.sum() == 0:
        raise SystemExit(f'Aucun tirage depuis {ERA3_START} : fichier trop ancien ? Rafraîchir d/LOTTOMAX.csv.')
    mx_recent, mx_avant = int(X[rec.values].max()), int(X[~rec.values].max())
    print(f"Tirages : {len(m)} (dernier {m['DRAW DATE'].max()}) | depuis {ERA3_START} : {rec.sum()} tirages, "
          f'max tiré = {mx_recent} | avant : max tiré = {mx_avant}')
    if mx_recent != N_MAX or mx_avant > 50:
        raise SystemExit('Ère de jeu incohérente avec 7/52 — vérifier les données.')
    print(f'Ère courante confirmée : 7/{N_MAX}, {PLAY_PRICE} $ = {LINES_PER_PLAY} lignes, 1 chance sur {TOTAL:,}')
    return X[rec.values]


# ---------------------------------------------------------------- 3. critères de profil
def criteres(X):
    """Retourne un dict de masques booléens (True = la ligne SATISFAIT le critère)."""
    d = np.diff(X, axis=1); s = X.sum(1)
    dec = np.stack([((X - 1) // 10 == k).any(1) for k in range(6)], 1).sum(1)
    return {
        'hauts>31 ≥ 2': (X > 31).sum(1) >= 2,
        'exactement 1 paire consécutive': (d == 1).sum(1) == 1,
        'somme 150-230': (s >= 150) & (s <= 230),
        'dizaines ≥ 4': dec >= 4,
        'pas toutes ≤ 31': ~(X <= 31).all(1),
        'pas de série arithmétique': ~(d == d[:, :1]).all(1),
    }


def profil_ok(X):
    ok = np.ones(len(X), bool)
    for v in criteres(X).values(): ok &= v
    return ok


def masques(X):
    """(n,7) numéros 1-52 -> uint64, bit (n-1) allumé."""
    return np.bitwise_or.reduce(np.left_shift(np.uint64(1), X.astype(np.uint64) - np.uint64(1)), axis=1)


# ---------------------------------------------------------------- 2. énumération complète
def enumerer_candidates():
    C5 = np.array(sorted(itertools.combinations(range(N_MAX), 5), key=lambda c: c[::-1]), np.uint8)
    total = 0; garde = []; t0 = time.time()
    for a in range(1, N_MAX + 1):
        for z in range(a + 6, N_MAX + 1):
            n = math.comb(z - a - 1, 5)
            X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)]).astype(np.int16)
            total += n
            X = X[profil_ok(X)]
            if len(X): garde.append(X.astype(np.int8))
    assert total == TOTAL, total
    cand = np.concatenate(garde)
    print(f'Espace complet : {total:,} combinaisons énumérées en {time.time() - t0:.0f} s | '
          f'candidates au profil impopulaire : {len(cand):,} ({len(cand) / total:.2%})')
    return cand


# ---------------------------------------------------------------- 3. sélection gloutonne
def selection_gloutonne(cand, n_lignes, rng):
    M = masques(cand)
    ordre = rng.permutation(len(cand))                 # départage aléatoire reproductible
    cand, M = cand[ordre], M[ordre]
    choix = [0]; sel_mask = M[0]
    for _ in range(n_lignes - 1):
        pire = np.zeros(len(M), np.uint8)              # pire chevauchement avec une ligne déjà prise
        for i in choix:
            pire = np.maximum(pire, np.bitwise_count(M & M[i]).astype(np.uint8))
        couv = np.bitwise_count(M & sel_mask)          # numéros déjà couverts (moins = mieux)
        score = pire.astype(np.int32) * 100 + couv.astype(np.int32)
        score[choix] = np.iinfo(np.int32).max
        j = int(np.argmin(score)); choix.append(j); sel_mask |= M[j]
    L = cand[choix].astype(int)
    return L[np.lexsort(L.T[::-1])]


# ---------------------------------------------------------------- 4. rapports
def chevauchement_max(L):
    return max((len(set(a) & set(b)) for i, a in enumerate(L) for b in L[i + 1:]), default=0)


def couverture(L, nom):
    X = L.astype(np.int16); c = criteres(X)
    couverts = np.unique(L)
    print(f'\n=== {nom} : {len(L)} lignes ===')
    for l in L: print('  ' + ' – '.join(f'{v:2d}' for v in l) + f'   somme {l.sum()}')
    print(f'Numéros distincts : {len(couverts)}/52 | manquants : {sorted(set(range(1, 53)) - set(couverts.tolist()))}')
    print(f'Chevauchement max entre 2 lignes : {chevauchement_max(L)}')
    print('Critères satisfaits (lignes/total) : ' + ', '.join(f'{k} {v.sum()}/{len(L)}' for k, v in c.items()))
    return {'lignes': len(L), 'numéros distincts': len(couverts), 'chevauchement max': chevauchement_max(L),
            **{k: int(v.sum()) for k, v in c.items()}}


def simuler(L, T8, rng, n_qp):
    """Approche lottomax_60_gains.py : lignes choisies + n_qp choix rapides fixes, valeurs des lots réelles."""
    D = len(T8); T, B = T8[:, :7], T8[:, 7]
    P = np.zeros((D, N_MAX + 1), bool); np.put_along_axis(P, T, True, axis=1)
    QP = np.argsort(rng.random((n_qp, N_MAX)), axis=1)[:, :K] + 1

    def gains(lignes):
        g = np.zeros(D); nb = np.zeros(D, int)
        for l in lignes:
            k = P[:, l].sum(1); bo = (l[None, :] == B[:, None]).any(1)
            v = np.select([k == 7, (k == 6) & bo, k == 6, (k == 5) & bo, k == 5, (k == 4) & bo, k == 4,
                           (k == 3) & bo, k == 3], list(LOT.values()), 0)
            g += v; nb += v > 0
        return g, nb

    g_ch, nb_ch = gains(list(L)); g_qp, _ = gains(list(QP))
    g = g_ch + g_qp; cout = len(L) * PLAY_PRICE
    return {'coût $': cout, 'lignes jouées': len(L) + n_qp,
            'gagne qqch (choisies seules)': (g_ch > 0).mean(), 'gagne qqch (avec QP)': (g > 0).mean(),
            'remboursé (choisies seules)': (g_ch >= cout).mean(), 'remboursé (avec QP)': (g >= cout).mean(),
            'gains moyens/ligne choisie': nb_ch.mean() / len(L), 'retour moyen $ (avec QP)': g.mean(),
            'retour moyen hors gros lot $': np.where(g >= LOT['7'], g - LOT['7'], g).mean()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10); ap.add_argument('--draws', type=int, default=300_000)
    ap.add_argument('--seed', type=int, default=2026); ap.add_argument('--out', default='.')
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)

    m, X = charger(); verifier_ere(m, X)
    cand = enumerer_candidates()
    L = selection_gloutonne(cand, a.n, rng)

    jeux = {f'optimal-{a.n}': L, 'conseil-9': CONSEIL9, 'étalées-10': ETALEES10}
    rap = {nom: couverture(S, nom) for nom, S in jeux.items()}

    print(f'\nMonte Carlo : {a.draws:,} tirages simulés (mêmes tirages pour les 3 jeux), '
          f'chaque ligne choisie accompagnée de {LINES_PER_PLAY - 1} choix rapides')
    T8 = np.argsort(rng.random((a.draws, N_MAX)), axis=1)[:, :8] + 1
    for nom, S in jeux.items():
        rap[nom].update(simuler(S, T8, np.random.default_rng(a.seed + 1), len(S) * (LINES_PER_PLAY - 1)))
    comp = pd.DataFrame(rap)
    fmt = comp.astype(object)
    for idx in fmt.index:
        if 'gagne' in idx or 'remboursé' in idx: fmt.loc[idx] = [f'{v:.2%}' for v in comp.loc[idx]]
        elif '$' in idx or 'moyens' in idx: fmt.loc[idx] = [f'{v:,.2f}' for v in comp.loc[idx]]
    print('\n=== Comparaison ===\n' + fmt.to_string())

    pd.DataFrame(L, columns=[f'n{i}' for i in range(1, 8)]).assign(somme=L.sum(1)) \
        .to_csv(f'{a.out}/optimal_lines.csv', index=False)
    comp.to_csv(f'{a.out}/optimal_comparison.csv')
    print(f'\nÉcrit : {a.out}/optimal_lines.csv, {a.out}/optimal_comparison.csv')


if __name__ == '__main__':
    main()
