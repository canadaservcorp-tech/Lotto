import numpy as np, pandas as pd, math
L = [[1,6,8,12,37,41,52],[1,8,12,14,37,41,52],[1,6,8,17,37,41,52],[1,8,14,17,37,41,52],[1,8,12,17,39,41,52],
     [1,8,12,37,39,41,52],[6,8,12,17,37,41,52],[8,12,14,17,37,41,52],[8,12,17,37,39,41,52]]
b = pd.read_csv('d/LOTTOMAX.csv'); m = b[b['SEQUENCE NUMBER'] == 0].sort_values('DRAW DATE')
last3 = m.tail(3); past = {tuple(sorted(r)) for r in m[[f'NUMBER DRAWN {i}' for i in range(1,8)]].values.tolist()}
for _, r in last3.iterrows(): print(r['DRAW DATE'], sorted(r[[f'NUMBER DRAWN {i}' for i in range(1,8)]].tolist()), 'compl.', r['BONUS NUMBER'])
fails = 0
for i, l in enumerate(L, 1):
    chk = {'sans consécutif': all(b2-a > 1 for a, b2 in zip(l, l[1:])), 'sans ...0': not set(l) & {10,20,30,40,50},
           'impairs 3-4': sum(x%2 for x in l) in (3,4), 'bas 3-4': sum(x<=26 for x in l) in (3,4),
           'somme 150-220': 150 <= sum(l) <= 220, 'finale <3': max(sum(x%10==k for x in l) for k in range(10)) < 3,
           'dizaine <4': max(sum((x-1)//10==k for x in l) for k in range(6)) < 4, 'étendue ≥30': l[-1]-l[0] >= 30,
           'bords': l[-1] >= 45 and l[0] <= 8, 'pas tous ≤31': not all(x <= 31 for x in l)}
    bons = [len(set(l) & set(r[[f'NUMBER DRAWN {j}' for j in range(1,8)]])) for _, r in last3.iterrows()]
    bon_c = [int(r['BONUS NUMBER'] in l) for _, r in last3.iterrows()]
    ko = [k for k, v in chk.items() if not v] + (['<3 bons'] if min(bons) < 3 else [])
    fails += len(ko)
    print(i, l, 'somme', sum(l), '| bons', bons, 'compl.', bon_c, '| déjà sortie' if tuple(l) in past else '', '| OK' if not ko else ko)
print('Lignes distinctes :', len({tuple(l) for l in L}), '| erreurs :', fails)
print('Numéros utilisés :', sorted(set(sum(L, []))))
print('Gros lot 9 lignes : 1 sur', f'{math.comb(52,7)/9:,.0f}', '| avec 27 choix rapides : 1 sur', f'{math.comb(52,7)/36:,.0f}')
