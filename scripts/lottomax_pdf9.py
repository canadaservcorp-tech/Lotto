"""Extrait les 9 lignes recommandées (gagnantes ≥ 6 $ aux 3 derniers tirages) et crée le PDF."""
import numpy as np, pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

exec(open('lottomax_conseil2.py').read().split('options = [')[0])   # recrée L (199 596) et bons (10 tirages)
neuf = L[(bons[:, -3:] >= 3).all(1)]; assert len(neuf) == 9
dates = m['DRAW DATE'].tolist()[-3:]

st = getSampleStyleSheet(); doc = SimpleDocTemplate('lotto_max_9_lignes.pdf', pagesize=letter,
                                                    topMargin=50, bottomMargin=50)
data = [['#', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', f'Bons {dates[0]}', f'Bons {dates[1]}', f'Bons {dates[2]}']]
for i, (l, b3) in enumerate(zip(neuf, bons[(bons[:, -3:] >= 3).all(1)][:, -3:]), 1):
    data.append([i] + [int(x) for x in l] + [int(x) for x in b3])
t = Table(data, repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E78')),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('FONTSIZE', (0, 0), (-1, -1), 9), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                       ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EEF3F8')])]))
story = [Paragraph('Lotto Max 7/52 - 9 lignes recommandées par le conseil', st['Title']),
         Paragraph('Critère : lignes de votre pool filtré qui ont gagné au moins 6 $ (3 bons numéros ou plus) '
                   f'à chacun des 3 derniers tirages ({", ".join(dates)}).', st['Normal']), Spacer(1, 14), t,
         Spacer(1, 16),
         Paragraph('<b>Comment jouer :</b> 9 mises de 6 $ = 54 $. Inscrivez une ligne par mise comme « votre » sélection ; '
                   'les 3 autres lignes de chaque mise sont des choix rapides (27 au total).', st['Normal']), Spacer(1, 8),
         Paragraph('<b>Chances :</b> gros lot 9 sur 133 784 560 (environ 1 sur 14,9 millions) pour ces 9 lignes ; '
                   'environ 1 sur 3,7 millions avec les 27 choix rapides. Chaque ligne : 4,28 % de gagner au moins 6 $.',
                   st['Normal']), Spacer(1, 8),
         Paragraph('<b>Attention - chevauchement :</b> ces 9 lignes n\'utilisent que 10 numéros différents '
                   '(8, 41 et 52 sont dans les 9 lignes). Chance d\'au moins un gain de 6 $ ou plus avec ces 9 lignes : '
                   'environ 10 %, contre environ 35 % avec 9 lignes étalées (même gain moyen).', st['Normal']),
         Spacer(1, 8),
         Paragraph('<b>Important :</b> avoir gagné aux tirages précédents ne donne aucun avantage au prochain tirage. '
                   'Ces lignes ont exactement les mêmes chances que toute autre ligne. '
                   'Résultats non officiels - validez vos billets auprès de Loto-Québec.', st['Normal'])]
doc.build(story)
for l in neuf: print(list(map(int, l)))
