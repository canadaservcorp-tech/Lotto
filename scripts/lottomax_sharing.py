"""Lotto Max 7/52 — optimiseur « risque de partage » : la probabilité de gagner est fixe, mais la part de gros
lot dépend du nombre d'autres joueurs ayant la même ligne. On modélise la popularité d'une ligne et on choisit
N lignes (chevauchement ≤ 1, profil de lottomax_optimal.py) qui MINIMISENT le nombre attendu de co-gagnants.

MODÈLE DE POPULARITÉ (hypothèses, pas des données Loto-Québec — ajuster POIDS/PATRONS si vous avez mieux) :
  - poids par numéro : jours 1-12 (jour ET mois d'anniversaire) > 13-31 (jour) > 32-52 ; bonus pour 7 et 3,
    malus pour 13 (tendances documentées dans les loteries UK/US : Simon 1998, Farrell et al. 2000).
  - multiplicateurs de patron : ligne entièrement ≤ 31, tous impairs/pairs, suite arithmétique, 3+ consécutifs,
    numéros d'un tirage récent (copie), somme très ronde. Choix rapides (≈ 70 % des lignes) : uniformes.
Nombre attendu de co-gagnants d'une ligne L si elle sort = ventes × [ (1-q)/C(52,7) + q × p_pop(L) ],
où q = part des lignes choisies à la main et p_pop la probabilité qu'un joueur « manuel » choisisse L.

Usage : python lottomax_sharing.py [--n 10] [--ventes 30000000] [--manuel 0.30] [--seed 2026] [--out .]
"""
import argparse, os
import numpy as np, pandas as pd
from lottomax_optimal import (N_MAX, K, TOTAL, CONSEIL9, ETALEES10, charger, verifier_ere, enumerer_candidates,
                              masques, chevauchement_max)

POIDS = np.ones(N_MAX + 1)
POIDS[1:13] = 1.6; POIDS[13:32] = 1.25; POIDS[32:] = 0.7
POIDS[7] *= 1.3; POIDS[3] *= 1.1; POIDS[11] *= 1.1; POIDS[13] *= 0.8
POIDS[0] = 0
PATRONS = {                              # multiplicateur de popularité si le patron est présent
    'toutes ≤ 31 (anniversaires)': 3.0, 'tous impairs ou tous pairs': 1.5, 'suite arithmétique': 20.0,
    '3+ consécutifs': 1.5, 'copie d’un des 10 derniers tirages': 50.0, 'somme multiple de 10': 1.05,
}


def patrons(X, recents):
    d = np.diff(X, axis=1); od = (X % 2).sum(1)
    R = np.zeros(len(X), bool)
    for r in recents: R |= (X == r[None, :]).all(1)
    return {'toutes ≤ 31 (anniversaires)': (X <= 31).all(1), 'tous impairs ou tous pairs': np.isin(od, (0, 7)),
            'suite arithmétique': (d == d[:, :1]).all(1), '3+ consécutifs': ((d[:, :-1] == 1) & (d[:, 1:] == 1)).any(1),
            'copie d’un des 10 derniers tirages': R, 'somme multiple de 10': X.sum(1) % 10 == 0}


def popularite(X, recents):
    """Poids relatif (non normalisé) : produit des poids des 7 numéros × multiplicateurs de patron."""
    w = np.prod(POIDS[X.astype(np.int64)], axis=1)
    for k, m in patrons(X, recents).items(): w = np.where(m, w * PATRONS[k], w)
    return w


def normalisation(rng, recents, n=4_000_000):
    """Estime la somme des poids sur les 133,8 M combinaisons par échantillonnage uniforme."""
    Xs = np.sort(np.argsort(rng.random((n, N_MAX)), axis=1)[:, :K] + 1, axis=1).astype(np.int16)
    return popularite(Xs, recents).mean() * TOTAL


def selection(cand, pop, n_lignes, rng):
    """Glouton : parmi les candidates au chevauchement ≤ 1 avec les lignes prises, la moins populaire."""
    M = masques(cand); ordre = rng.permutation(len(cand)); cand, pop, M = cand[ordre], pop[ordre], M[ordre]
    choix = [int(np.argmin(pop))]; pire = np.zeros(len(M), np.uint8)
    for _ in range(n_lignes - 1):
        pire = np.maximum(pire, np.bitwise_count(M & M[choix[-1]]).astype(np.uint8))
        score = np.where(pire <= 1, pop, np.inf); score[choix] = np.inf
        choix.append(int(np.argmin(score)))
    L = cand[choix].astype(int)
    return L[np.lexsort(L.T[::-1])]


def rapport(nom, L, recents, Z, ventes, q):
    X = L.astype(np.int16); w = popularite(X, recents) / Z
    co = ventes * ((1 - q) / TOTAL + q * w); unif = ventes / TOTAL
    pat = patrons(X, recents)
    print(f'\n=== {nom} : {len(L)} lignes | chevauchement max {chevauchement_max(L)} ===')
    for l, c in zip(L, co): print('  ' + ' – '.join(f'{v:2d}' for v in l) + f'   co-gagnants attendus {c:.3f}')
    print(f'Co-gagnants attendus si la ligne sort : moyenne {co.mean():.3f} (choix rapide uniforme : {unif:.3f}) '
          f'-> popularité relative {co.mean() / unif:.2f}× | part de gros lot attendue {1 / (1 + co.mean()):.1%}')
    print('Patrons populaires présents : ' + ', '.join(f'{k} {v.sum()}' for k, v in pat.items() if v.sum()) or 'aucun')
    return {'lignes': len(L), 'chevauchement max': chevauchement_max(L), 'co-gagnants attendus (moy.)': co.mean(),
            'popularité relative vs choix rapide': co.mean() / unif, 'part de gros lot attendue': 1 / (1 + co.mean()),
            **{k: int(v.sum()) for k, v in pat.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10); ap.add_argument('--ventes', type=float, default=30e6,
                    help='lignes vendues par tirage (hypothèse)')
    ap.add_argument('--manuel', type=float, default=0.30, help='part des lignes choisies à la main')
    ap.add_argument('--seed', type=int, default=2026); ap.add_argument('--out', default='.')
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)

    m, X = charger(); verifier_ere(m, X); recents = X[-10:]
    Z = normalisation(rng, recents)
    cand = enumerer_candidates()
    pop = popularite(cand.astype(np.int16), recents) / Z
    print(f'Popularité relative des candidates : min {pop.min() * TOTAL:.2f}×, médiane {np.median(pop) * TOTAL:.2f}×, '
          f'max {pop.max() * TOTAL:.2f}× la ligne uniforme')
    L = selection(cand, pop, a.n, rng)

    jeux = {f'partage-{a.n}': L, 'conseil-9': CONSEIL9, 'étalées-10': ETALEES10}
    if os.path.exists(f'{a.out}/optimal_lines.csv'):
        OPT = pd.read_csv(f'{a.out}/optimal_lines.csv')[[f'n{i}' for i in range(1, 8)]].values
        jeux[f'optimal-{len(OPT)}'] = OPT
    rap = {nom: rapport(nom, S, recents, Z, a.ventes, a.manuel) for nom, S in jeux.items()}
    comp = pd.DataFrame(rap)
    print(f'\n=== Comparaison (ventes {a.ventes:,.0f} lignes/tirage, {a.manuel:.0%} choisies à la main) ===')
    print(comp.to_string(float_format=lambda v: f'{v:.3f}'))
    print('\nRappel : la probabilité de gagner est identique pour toutes ces lignes ; seul le partage change.')
    pd.DataFrame(L, columns=[f'n{i}' for i in range(1, 8)]).assign(somme=L.sum(1)) \
        .to_csv(f'{a.out}/sharing_lines.csv', index=False)
    comp.to_csv(f'{a.out}/sharing_comparison.csv')
    print(f'Écrit : {a.out}/sharing_lines.csv, {a.out}/sharing_comparison.csv')


if __name__ == '__main__':
    main()
