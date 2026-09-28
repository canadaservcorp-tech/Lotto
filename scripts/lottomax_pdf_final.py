"""PDF imprimable du jeu final : chaque ligne dessinée comme une grille de billet 1-52 (numéros cochés).
Page 1 : optimal-10 (results/optimal_lines.csv). Page 2 : partage-10 (results/sharing_lines.csv), variante.
Usage : python lottomax_pdf_final.py [--res ../results]"""
import argparse
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BLEU, GRIS = colors.HexColor('#1F4E78'), colors.HexColor('#BBBBBB')
W, H = letter


def grille(c, x, y, nums, cell=13):
    """Grille 10 colonnes × 6 rangées (1-52), numéros choisis en plein."""
    for n in range(1, 53):
        cx, cy = x + ((n - 1) % 10) * cell, y - ((n - 1) // 10) * cell
        if n in nums:
            c.setFillColor(BLEU); c.roundRect(cx, cy - cell, cell - 1, cell - 1, 2, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont('Helvetica-Bold', 6.5)
        else:
            c.setStrokeColor(GRIS); c.setFillColor(colors.white); c.rect(cx, cy - cell, cell - 1, cell - 1, stroke=1, fill=0)
            c.setFillColor(colors.HexColor('#777777')); c.setFont('Helvetica', 6)
        c.drawCentredString(cx + (cell - 1) / 2, cy - cell + 3.5, str(n))


def page(c, titre, sous_titre, L, notes):
    c.setFillColor(BLEU); c.setFont('Helvetica-Bold', 18); c.drawString(50, H - 55, titre)
    c.setFillColor(colors.black); c.setFont('Helvetica', 9.5); c.drawString(50, H - 72, sous_titre)
    top = H - 100; col_w = (W - 100) / 2
    for i, l in enumerate(L):
        col, row = i % 2, i // 2
        x, y = 50 + col * col_w, top - row * 118
        c.setFillColor(BLEU); c.setFont('Helvetica-Bold', 12); c.drawString(x, y, f'Ligne {i + 1}')
        c.setFillColor(colors.black); c.setFont('Helvetica-Bold', 13)
        c.drawString(x + 52, y, ' – '.join(f'{v:02d}' for v in l))
        grille(c, x, y - 12, set(l))
        c.setFillColor(colors.HexColor('#555555')); c.setFont('Helvetica', 7.5)
        c.drawString(x + 135, y - 60, f'somme {sum(l)}  ·  {sum(v > 31 for v in l)} numéros > 31')
    c.setFillColor(colors.black); yy = 78
    for n in notes:
        c.setFont('Helvetica', 8.5); c.drawString(50, yy, n); yy -= 12
    c.showPage()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--res', default='../results'); a = ap.parse_args()
    cols = [f'n{i}' for i in range(1, 8)]
    opt = pd.read_csv(f'{a.res}/optimal_lines.csv')[cols].values.tolist()
    par = pd.read_csv(f'{a.res}/sharing_lines.csv')[cols].values.tolist()
    out = f'{a.res}/lotto_max_jeu_final.pdf'; c = canvas.Canvas(out, pagesize=letter)
    c.setTitle('Lotto Max 7/52 — jeu final')
    page(c, 'Lotto Max 7/52 — JEU FINAL (optimal-10)',
         '10 mises × 6 $ = 60 $. Sur chaque mise, inscrivez UNE ligne ci-dessous ; les 3 autres lignes sont des choix rapides.',
         opt, ['Couvre les 52 numéros, max 1 numéro commun entre 2 lignes, exactement 1 paire consécutive par ligne.',
               'Simulation (1 M de tirages) : gagner quelque chose ≈ 85 %, récupérer 60 $ ou plus ≈ 1,9 %, retour moyen ≈ 17 $.',
               'Chaque ligne : 1 chance sur 133 784 560 pour le gros lot, 4,28 % pour un lot de 6 $ ou plus — comme toute autre ligne.',
               'Résultats non officiels — validez vos billets auprès de Loto-Québec.'])
    page(c, 'Variante — partage-10 (moins de co-gagnants)',
         'Mêmes chances de gagner ; numéros moins joués (32–52) pour garder une plus grande part d’un gros lot.',
         par, ['Modèle de popularité = hypothèses (anniversaires 1–31 sur-joués), pas des données Loto-Québec.',
               'Part de gros lot attendue ≈ 86 % contre ≈ 84 % pour optimal-10 (30 M de lignes vendues, 30 % choisies à la main).',
               'Choisissez UN des deux jeux et gardez-le : changer de lignes ne change jamais les chances.'])
    c.save(); print('Écrit :', out)


if __name__ == '__main__':
    main()
