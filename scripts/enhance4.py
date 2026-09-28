"""Ajuste 4 lignes pour qu'elles passent les 10 filtres, en gardant le plus de numéros d'origine
et en restant étalées (chevauchement max 1 entre lignes)."""
import itertools
S = [[8,23,29,45,46,49,51],[5,26,27,33,37,43,52],[7,25,28,35,39,46,47],[1,24,31,35,36,45,49]]
def ok(l):
    return (all(b-a > 1 for a, b in zip(l, l[1:])) and not set(l) & {10,20,30,40,50}
            and sum(x%2 for x in l) in (3,4) and sum(x<=26 for x in l) in (3,4) and 150 <= sum(l) <= 220
            and max(sum(x%10==k for x in l) for k in range(10)) < 3
            and max(sum((x-1)//10==k for x in l) for k in range(6)) < 4
            and l[-1]-l[0] >= 30 and l[-1] >= 45 and l[0] <= 8 and not all(x <= 31 for x in l))
choisies = []
for orig in S:
    best = None
    for keep in (6, 5, 4, 3):
        for base in itertools.combinations(orig, keep):
            reste = [n for n in range(1, 53) if n not in base]
            for add in itertools.combinations(reste, 7 - keep):
                l = sorted(base + add)
                if not ok(l): continue
                ov = max((len(set(l) & set(c)) for c in choisies), default=0)
                if ov > 1: continue
                score = (len(set(l) & set(orig)), -ov, -abs(sum(l) - 185))   # garder + étaler + somme centrée
                if best is None or score > best[0]: best = (score, l)
        if best: break
    choisies.append(best[1])
    print(orig, '→', best[1], '| gardés', best[0][0], '| somme', sum(best[1]))
print('Chevauchements :', [len(set(a) & set(b)) for a, b in itertools.combinations(choisies, 2)])
