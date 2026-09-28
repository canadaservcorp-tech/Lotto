"""Les lignes qui ont gagné ≥ 6 $ au tirage précédent gagnent-elles plus souvent au tirage suivant ?
Test sur les 48 paires de tirages consécutifs du jeu 7/52, avec 2 000 000 de lignes au hasard."""
import numpy as np, pandas as pd
N, K, S = 52, 7, 2_000_000
b = pd.read_csv('d/LOTTOMAX.csv')
m = b[(b['SEQUENCE NUMBER'] == 0) & (b['DRAW DATE'] >= '2026-04-14')].sort_values('DRAW DATE')
T = m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values
rng = np.random.default_rng(11)
L = np.argsort(rng.random((S, N)), axis=1)[:, :K] + 1
P = np.zeros((S, N + 1), bool); np.put_along_axis(P, L, True, axis=1)
gagne = np.stack([P[:, t].sum(1) >= 3 for t in T])        # (tirages, lignes) : ≥ 3 bons
avant, apres = gagne[:-1], gagne[1:]
taux_si_gagne = (avant & apres).sum() / avant.sum()
taux_si_perdu = (~avant & apres).sum() / (~avant).sum()
print(f'Paires de tirages : {len(avant)}')
print(f'Lignes gagnantes au tirage précédent → gagnent au suivant : {taux_si_gagne:.2%}')
print(f'Lignes perdantes au tirage précédent → gagnent au suivant : {taux_si_perdu:.2%}')
