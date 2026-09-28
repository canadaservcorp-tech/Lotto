"""PDF des combinaisons restantes (Lotto Max 7/52) après tout le travail de filtrage."""
import itertools, math
import numpy as np, pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

N = 52
ZERO = np.array([10, 20, 30, 40, 50])
def pool(X):
    d = np.diff(X, axis=1); od = (X % 2).sum(1); lo = (X <= 26).sum(1); s = X.sum(1)
    ok = ((d > 1).all(1) & ~np.isin(X, ZERO).any(1) & np.isin(od, (3, 4)) & np.isin(lo, (3, 4))
          & (s >= 150) & (s <= 220))
    ok &= np.max([(X % 10 == k).sum(1) for k in range(10)], 0) < 3
    ok &= np.max([((X - 1) // 10 == k).sum(1) for k in range(6)], 0) < 4
    ok &= (X[:, -1] - X[:, 0] >= 30) & (X[:, -1] >= 45) & (X[:, 0] <= 8) & ~(X <= 31).all(1)
    return ok

b = pd.read_csv('d/LOTTOMAX.csv')
m = b[b['SEQUENCE NUMBER'] == 0].sort_values('DRAW DATE').tail(3)
T = m[[f'NUMBER DRAWN {i}' for i in range(1, 8)]].values; DATE = m['DRAW DATE'].iloc[-1]

C5 = np.array(sorted(itertools.combinations(range(N), 5), key=lambda c: c[::-1]), np.uint8)
parts = []
for a in range(1, N + 1):
    for z in range(a + 6, N + 1):
        n = math.comb(z - a - 1, 5)
        X = np.column_stack([np.full(n, a), C5[:n].astype(np.int16) + a + 1, np.full(n, z)]).astype(np.int16)
        X = X[pool(X)]
        if len(X): X = X[np.isin(X, T[-1]).sum(1) >= 3]
        if len(X): parts.append(X)
L = np.vstack(parts); L = L[np.lexsort(L.T[::-1])]; assert len(L) == 199_596
bons = np.stack([np.isin(L, t).sum(1) for t in T], 1)
L9 = L[(bons >= 3).all(1)]; L5 = L[bons[:, -1] >= 6]
pd.DataFrame(L, columns=[f'N{i}' for i in range(1, 8)]).to_csv('combinaisons_restantes_199596.csv', index=False)

SPREAD = [[5, 12, 14, 25, 33, 38, 52], [2, 8, 13, 32, 43, 49, 51], [1, 3, 21, 24, 28, 36, 46],
          [4, 9, 11, 22, 34, 39, 48], [7, 18, 23, 26, 29, 42, 47], [6, 15, 19, 37, 41, 44, 52],
          [8, 14, 16, 27, 31, 35, 45], [5, 17, 23, 31, 44, 46, 48], [2, 6, 11, 23, 28, 38, 45],
          [1, 6, 22, 25, 27, 42, 49]]

W, H = letter; c = canvas.Canvas('lotto_max_combinaisons_restantes.pdf', pagesize=letter)
c.setTitle('Lotto Max 7/52 - combinaisons restantes'); page = [1]
def pied():
    c.setFont('Helvetica', 7); c.setFillColor(colors.grey)
    c.drawString(40, 25, f'Lotto Max 7/52 - combinaisons restantes - tirage de référence {DATE}')
    c.drawRightString(W - 40, 25, f'Page {page[0]}'); c.setFillColor(colors.black)
def nouvelle():
    pied(); c.showPage(); page[0] += 1
def ligne(nums): return '  '.join(f'{int(x):2d}' for x in nums)

# Page 1 : résumé
y = H - 60; c.setFont('Helvetica-Bold', 18); c.drawString(40, y, 'Lotto Max 7/52 - Combinaisons restantes')
y -= 22; c.setFont('Helvetica', 10); c.drawString(40, y, f'Données officielles BCLC, dernier tirage : {DATE}')
etapes = [('Toutes les combinaisons 7/52', '133 784 560'),
          ('Sans numéros consécutifs', '53 524 680'),
          ('+ sans 10, 20, 30, 40, 50', '25 470 555'),
          ('+ filtre équilibré (3-4 impairs, 3-4 bas, somme 150-220)', '7 496 713'),
          ('+ filtres du conseil (finales, dizaines, étendue, bords, anniversaires)', '4 314 139'),
          (f'+ gagnantes 6 $ et plus au tirage du {DATE}', '199 596'),
          ('+ gagnantes 6 $ et plus aux 3 derniers tirages', f'{len(L9)}'),
          (f'+ gagnantes 6/7 au tirage du {DATE}', f'{len(L5)}')]
y -= 30; c.setFont('Helvetica-Bold', 11); c.drawString(40, y, 'Étapes d\'élimination'); y -= 18
for e, v in etapes:
    c.setFont('Helvetica', 10); c.drawString(50, y, e); c.drawRightString(W - 50, y, v); y -= 16
y -= 10; c.setFont('Helvetica-Oblique', 9)
for t in ['Rappel : chaque ligne a exactement la même chance au prochain tirage :',
          '1 sur 133 784 560 pour le gros lot, environ 4,3 % pour gagner 6 $ ou plus.',
          'Les filtres réduisent la liste; ils n\'augmentent pas les chances d\'une ligne.']:
    c.drawString(50, y, t); y -= 13

def bloc(titre, lignes_):
    global y
    y -= 16; c.setFont('Helvetica-Bold', 11); c.drawString(40, y, titre); y -= 16
    c.setFont('Courier', 10)
    for i, l in enumerate(lignes_, 1):
        c.drawString(50, y, f'{i:2d}.   {ligne(l)}'); y -= 13
bloc(f'Plan 60 $ : 10 lignes étalées (chevauchement max 1 numéro)', SPREAD)
nouvelle(); y = H - 50
bloc(f'{len(L9)} lignes gagnantes aux 3 derniers tirages', L9)
bloc(f'{len(L5)} lignes gagnantes 6/7 au tirage du {DATE}', L5)
nouvelle()

# Liste complète : 199 596 lignes, 3 colonnes x 72 rangées = 216 lignes par page
COLS, ROWS = 3, 72; xs = [40 + i * 180 for i in range(COLS)]; per = COLS * ROWS
for start in range(0, len(L), per):
    c.setFont('Helvetica-Bold', 9)
    c.drawString(40, H - 35, f'Liste complète : 199 596 combinaisons (lignes {start + 1:,} à {min(start + per, len(L)):,})')
    c.setFont('Courier', 7.5)
    chunk = L[start:start + per]
    for j, l in enumerate(chunk):
        col, row = divmod(j, ROWS)
        c.drawString(xs[col], H - 52 - row * 9.6, f'{start + j + 1:>7,} {ligne(l)}')
    nouvelle()
c.save(); print('pages :', page[0] - 1, '| 9 lignes :', len(L9), '| 5 lignes :', len(L5))
