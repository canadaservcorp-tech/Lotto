"""Exporte les 199 596 lignes (CSV) + les 9 et 5 lignes du conseil n°2."""
exec(open('lottomax_conseil2.py').read().split('options = [')[0])
import numpy as np, pandas as pd
cols = [f'N{i}' for i in range(1, 8)]
pd.DataFrame(L, columns=cols).to_csv('lignes_199596.csv', index=False)
L9 = L[(bons[:, -3:] >= 3).all(1)]; L5 = L[k >= 6]
np.save('L9.npy', L9); np.save('L5.npy', L5)
print(len(L), L9.tolist(), L5.tolist())
