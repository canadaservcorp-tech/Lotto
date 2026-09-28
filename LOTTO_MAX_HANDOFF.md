# Lotto Max Study — Handoff File
Project: `lotto` · Prepared: 2026-09-27 · Status: analysis complete, code not yet confirmed on GitHub

---

## 1. Goal of the study
Start from the full history of Loto-Québec results, focus on **Lotto Max**, and progressively **eliminate combinations** (series, patterns, "never happened" profiles) to reach a small, playable set of lines, then evaluate costs and real chances.

---

## 2. Data
| Item | Detail |
|---|---|
| Source (official) | BCLC PlayNow downloadable numbers: `https://www.playnow.com/resources/documents/downloadable-numbers/LOTTOMAX.zip` (also `649.zip`) |
| Why valid for Québec | Lotto Max and Lotto 6/49 are national games — same numbers everywhere in Canada |
| Coverage | Lotto 6/49: 2,372 draws (2004-01-03 → 2026-09-23). Lotto Max main: 1,273 draws (2009-09-25 → 2026-09-25). MaxMillions: 7,458 |
| Cross-check | Last 3 draws verified against lotterycanada.com |
| Not included | Québec 49, Québec Max, Grande Vie, Extra, Banco (Québec-only games, not in this source) |

---

## 3. Game rules — IMPORTANT (three eras)
| Era | Dates | Format | Jackpot odds / line |
|---|---|---|---|
| 1 | 2009-09-25 → 2019-05-10 | 7 of 49 | 1 in 85,900,584 |
| 2 | 2019-05-14 → 2026-04-10 | 7 of 50 (722 draws) | 1 in 99,884,400 |
| 3 (current) | since 2026-04-14 | **7 of 52** | **1 in 133,784,560** |

Current game: **$6 per play = 4 lines**. The player chooses **1 line**; the other **3 are Quick Picks** (random, unknown in advance). Prize fund = 48% of sales.

**Prize structure (values from real draw of 2026-09-25):**
| Match | Prize |
|---|---|
| 7/7 | Jackpot (est. $65M next draw) |
| 6/7 + bonus | $273,318 (pool share) |
| 6/7 | $6,189 (pool share) |
| 5/7 + bonus | $1,215 (pool share) |
| 5/7 | $125 (pool share) |
| 4/7 + bonus | $66 (pool share) |
| 4/7 | $20 |
| 3/7 + bonus | $20 |
| 3/7 | Free Play ($6) |

Plus MAXPLUS ($100,000 prizes, 65 expected next draw) and MAXMILLIONS ($1M, 6 expected).

---

## 4. Statistical findings (7/50 era, 722 draws)
- **Frequency:** every number within z = −1.5 to +1.6 of expectation → pure chance. Hot numbers (last 100 draws): 43, 6, 31, 34, 28, 41, 3, 48.
- **Repetition from previous draw:** average 1.01 numbers repeat vs 0.98 predicted by hypergeometric law — perfect match with theory.
- **Full combination ever repeated:** none. Max overlap between two draws: 5 numbers.
- **Last digit (…0 numbers 10/20/30/40/50):** drawn 534 times vs 537.7 expected → NOT "low chance".
- **Consecutive numbers:** 61.6% of real draws contain at least one consecutive pair.
- **Previous-draw winners:** lines that won last draw won next draw 4.59% vs 4.27% for losers — within random noise (simulation shows ±1 point swings).
- **Backtest of "never happened" filters** (learned 2019–2023, tested 2024–2026): removed 0.9% of combinations and 0.4% of real winners → no edge.
- **Handicapping + wheel backtest (200 draws):** hot 4.0%, cold 5.1%, random 4.8%, theory 4.3% → no method beats chance.

---

## 5. Elimination chain (current game 7/52) — exact counts
| Step | Filter | Remaining | % of total |
|---|---|---|---|
| 0 | All combinations | 133,784,560 | 100% |
| 1 | No consecutive numbers (formula C(46,7)) | 53,524,680 | 40.0% |
| 2 | No 10, 20, 30, 40, 50 | 25,470,555 | 19.0% |
| 3 | Balanced: 3–4 odd, 3–4 low (1–26), sum 150–220 | 7,496,713 | 5.6% |
| 4 | Council 1: <3 same last digit, <4 same decade, range ≥30, has ≥45 and ≤8, not all ≤31 | **4,314,139** | 3.2% |
| 5 | Won ≥ $6 on last draw (2026-09-25) | **199,596** | 0.15% |
| 6 | Council 2: won ≥ $6 on each of last 3 draws | **9** | — |

Share of real draws that would have survived: step 1 → 38.4%, step 2 → 16.9%, step 4 → 2.6%. **Each filter removes winners in the same proportion as combinations.**

**Council 2 alternative reductions from 199,596:**
| Option | Lines | $60 packages |
|---|---|---|
| Won $20+ last draw | 33,585 | 3,359 |
| Won $6+ in 3+ of last 10 draws | 22,196 | 2,220 |
| Won $6+ in 4+ of last 10 draws | 2,990 | 299 |
| Won 5/7+ last draw | 637 | 64 |
| Won $6+ on each of last 2 draws | 516 | 52 |
| **Won $6+ on each of last 3 draws** | **9** | **1** |
| Won 6/7 last draw | 5 | 1 |

---

## 6. Final line sets

### A. The council's 9 lines (verified: pass all 10 filters, 3 matches on each of last 3 draws, never drawn before)
1. 1 – 6 – 8 – 12 – 37 – 41 – 52
2. 1 – 8 – 12 – 14 – 37 – 41 – 52
3. 1 – 6 – 8 – 17 – 37 – 41 – 52
4. 1 – 8 – 14 – 17 – 37 – 41 – 52
5. 1 – 8 – 12 – 17 – 39 – 41 – 52
6. 1 – 8 – 12 – 37 – 39 – 41 – 52
7. 6 – 8 – 12 – 17 – 37 – 41 – 52
8. 8 – 12 – 14 – 17 – 37 – 41 – 52
9. 8 – 12 – 17 – 37 – 39 – 41 – 52

Weakness: only 10 distinct numbers (8, 41, 52 in all lines) → lines win or lose together.

### B. The 10 "spread" lines ($60 plan) — from the filtered pool, max 1 shared number between any two lines
1. 5 – 12 – 14 – 25 – 33 – 38 – 52
2. 2 – 8 – 13 – 32 – 43 – 49 – 51
3. 1 – 3 – 21 – 24 – 28 – 36 – 46
4. 4 – 9 – 11 – 22 – 34 – 39 – 48
5. 7 – 18 – 23 – 26 – 29 – 42 – 47
6. 6 – 15 – 19 – 37 – 41 – 44 – 52
7. 8 – 14 – 16 – 27 – 31 – 35 – 45
8. 5 – 17 – 23 – 31 – 44 – 46 – 48
9. 2 – 6 – 11 – 23 – 28 – 38 – 45
10. 1 – 6 – 22 – 25 – 27 – 42 – 49

---

### C. Final set — your 4 lines, enhanced to pass all 10 filters (1 number changed each, max 1 shared number)
1. 2 – 8 – 23 – 29 – 46 – 49 – 51  (was 8-23-29-45-46-49-51: 45 → 2)
2. **5 – 12 – 26 – 33 – 37 – 43 – 52**  (was 5-26-27-33-37-43-52: 27 → 12) ← line to choose if only one
3. 4 – 7 – 25 – 28 – 35 – 39 – 46  (was 7-25-28-35-39-46-47: 47 → 4)
4. 1 – 4 – 24 – 31 – 36 – 45 – 49  (was 1-24-31-35-36-45-49: 35 → 4)

Cost: 4 plays × $6 = $24 (16 lines with 12 Quick Picks).

### D. Proof check — 5 real 2025 results vs your filters
All 5 are official main-draw results, and **all 5 would have been eliminated** by your filters:
| Date | Numbers | Fails |
|---|---|---|
| 2025-09-23 | 8, 9, 23, 30, 38, 40, 43 | consecutive, …0, edges |
| 2025-09-30 | 14, 22, 27, 31, 33, 39, 50 | …0, low/high, edges |
| 2025-10-07 | 5, 6, 16, 26, 29, 37, 44 | consecutive, same last digit, edges |
| 2025-12-23 | 3, 28, 37, 38, 39, 41, 43 | consecutive, odd, low, sum, edges |
| 2025-12-30 | 5, 21, 32, 38, 43, 44, 45 | consecutive, low, sum |

---

### E. "Optimal-10" set (`lottomax_optimal.py`, seed 2026) — covers all 52 numbers, max 1 shared number, each line has exactly one consecutive pair
1. 1 – 5 – 15 – 34 – 38 – 41 – 42
2. 2 – 5 – 20 – 21 – 24 – 32 – 49
3. 2 – 13 – 14 – 27 – 33 – 36 – 46
4. 3 – 18 – 26 – 37 – 39 – 49 – 50
5. 4 – 8 – 13 – 26 – 41 – 43 – 44
6. 4 – 9 – 11 – 21 – 22 – 47 – 52
7. 6 – 7 – 24 – 28 – 31 – 35 – 43
8. 8 – 17 – 23 – 28 – 32 – 50 – 51
9. 10 – 12 – 25 – 30 – 32 – 44 – 45
10. 16 – 19 – 20 – 29 – 40 – 48 – 51

Candidate pool with this profile: 33,306,688 of 133,784,560 (24.9%). Monte Carlo (1M draws, 10 lines + 30 Quick Picks, $60): win something 84.6%, money back 1.9%, avg non-jackpot return $17.02 — statistically identical to spread-10 (84.7% / 1.9% / $17.32); council-9 ($54): 73.6% / 3.5% / $15.59. As expected, the profile changes *which* lines are played, not the odds.

### F. "Sharing-10" set (`lottomax_sharing.py`) — same profile + overlap ≤ 1, but chosen to minimise *expected co-winners* under a popularity model (birthday numbers 1–31 over-played, 32–52 under-played, pattern multipliers). Popularity weights are **assumptions**, not Loto-Québec data — edit `POIDS`/`PATRONS` at the top of the script if better data appears.
1. 1 – 32 – 33 – 35 – 37 – 41 – 51
2. 2 – 6 – 33 – 38 – 48 – 49 – 52
3. 2 – 15 – 34 – 40 – 41 – 47 – 50
4. 4 – 16 – 32 – 42 – 44 – 45 – 47
5. 5 – 12 – 36 – 41 – 43 – 44 – 49
6. 8 – 13 – 37 – 39 – 40 – 44 – 48
7. 13 – 19 – 20 – 35 – 43 – 47 – 52
8. 13 – 23 – 33 – 34 – 36 – 42 – 46
9. 14 – 21 – 35 – 36 – 38 – 40 – 45
10. 17 – 26 – 32 – 34 – 38 – 39 – 43

With 30M lines sold/draw and 30% hand-picked: expected co-winners if a line hits = 0.165 (sharing-10) vs 0.197 (optimal-10), 0.196 (council-9), 0.204 (spread-10), 0.224 (Quick Pick) → expected jackpot share 85.8% vs ≈ 83.5%. **Win probability is identical for all sets**; this only changes how much you keep if you win.

### G. Randomness battery (`lottomax_randomness.py`, 4,000 simulated histories per era) — `results/randomness_tests.csv`
14 tests × 3 eras (number & bonus frequency, pair frequency, sum mean/sd, previous-draw repeats, max skip, lag-1 autocorrelation, consecutive pairs, odd/low counts, range, runs, and a predictive test: does first-half frequency predict second-half frequency?). Result: **1 of 42 tests below p = 0.05 (2.1 expected by chance), min p = 0.024, Bonferroni threshold 0.0012 → no exploitable bias.** Predictive correlation between halves: +0.09 / −0.06 / −0.04 (all noise). This closes the "is there a statistical edge" question.

## 7. Real chances (simulations, 300k–1M draws)
| Plan | Cost | Win something | Money back or more | Avg small-prize return | Jackpot |
|---|---|---|---|---|---|
| 9 council lines + 27 Quick Picks (36 lines) | $54 | 72% | 3.7% | $15.50 | 1 in 3.7 M |
| 10 spread lines + 30 Quick Picks (40 lines) | $60 | 83% | 2.0% | $16.95 | 1 in 3.3 M |
| Your 10 chosen lines only: spread vs council-style | — | 38% vs 10% | — | same | — |

Per line: 4.28% chance of $6+ (5,732,581 winning lines out of 133,784,560 in every draw).

---

## 8. Conclusions
1. Lotto Max draws behave exactly like a fair random process; no filter, frequency, handicapping or wheel improves the odds of a single line.
2. Elimination only chooses **which** lines to play; it never concentrates winners.
3. The only real levers: **spreading lines** (more frequent small wins, same average) and **avoiding popular patterns** (less jackpot sharing).
4. Expected long-run return ≈ 48% of money spent.

---

## 9. Corrections made during the study (for transparency)
- First Lotto Max analysis wrongly mixed 48 draws of the new 7/52 game into the 7/50 era and used old odds → fixed.
- Early note that Québec lets you choose all lines was based on old 3-line rules → unverified for the 4-line game; ask retailer.
- A 927-page PDF + CSV of all 199,596 remaining lines was generated but not delivered at the time; I then wrongly said no PDF existed. Both are included in this package.
- DP merge bug and hot/cold sort-direction bug in the strategies script → fixed before results were reported.

---

## 10. Core filter (Python) — the definition of the 4,314,139-line pool
```python
import numpy as np
ZERO = np.array([10, 20, 30, 40, 50])
def pool(X):  # X: (n,7) sorted int16 array
    d = np.diff(X, axis=1); od = (X % 2).sum(1); lo = (X <= 26).sum(1); s = X.sum(1)
    ok = ((d > 1).all(1) & ~np.isin(X, ZERO).any(1) & np.isin(od, (3, 4)) & np.isin(lo, (3, 4))
          & (s >= 150) & (s <= 220))
    ok &= np.max([(X % 10 == k).sum(1) for k in range(10)], 0) < 3
    ok &= np.max([((X - 1) // 10 == k).sum(1) for k in range(6)], 0) < 4
    ok &= (X[:, -1] - X[:, 0] >= 30) & (X[:, -1] >= 45) & (X[:, 0] <= 8) & ~(X <= 31).all(1)
    return ok
```

---

## 11. Project files (folder `~/projects/lotto/`)
All scripts read `d/LOTTOMAX.csv` (unzipped from the source in section 2).
| File | Purpose |
|---|---|
| build.py | All-results workbook (6/49 from 2004, Lotto Max, MaxMillions) + CSVs |
| loto_quebec_resultats_2004_2026.xlsx + 3 CSVs | Raw results |
| lottomax_analyse.py / lotto_max_analyse.xlsx | Frequency, repetition, pairs, odds |
| lottomax_filtres.py / filtres_backtest.csv | "Never happened" filters + backtest |
| lottomax_compte.py | Exact remaining count (7/50 and 7/52) |
| lottomax_series.py / series_elimination.csv | Consecutive and arithmetic series |
| lottomax_sans_suite.py | No-consecutive pool + generator |
| lottomax_finale_0.py | Last-digit frequency + exclusion of …0 numbers |
| lottomax_strategies.py / lotto_max_strategies.xlsx | Pattern filter, handicapping, wheel, walk-forward test |
| lottomax_conseil.py / conseil_filtres.csv | Council 1 filters → 4,314,139 |
| lottomax_gagnantes.py / lignes_gagnantes.csv | Lines winning ≥ $6 |
| lottomax_repeat_test.py | Previous-draw winners test |
| lottomax_conseil2.py / conseil2_options.csv | Council 2 options from 199,596 |
| lottomax_60.py / lottomax_60_gains.py | $60 plan + winnings distribution |
| lottomax_pdf9.py / lotto_max_9_lignes.pdf / verif9.py | 9-line PDF + verification |
| lottomax_pdf.py / export_lignes.py | 927-page PDF + CSV of all 199,596 remaining lines |
| lotto_max_combinaisons_restantes.pdf / combinaisons_restantes_199596.csv | All 199,596 lines |
| enhance4.py | Adjusts any lines to pass the 10 filters with minimum changes |
| lottomax_optimal.py / optimal_lines.csv / optimal_comparison.csv | Era check (7/52), full 133,784,560 enumeration, greedy selection of N lines (overlap ≤ 1, ≥ 2 numbers > 31, exactly one consecutive pair, sum 150–230, ≥ 4 decades, no all-low / arithmetic series), Monte Carlo vs council-9 and spread-10 |
| lottomax_randomness.py / randomness_tests.csv | Monte-Carlo randomness battery on the real draws, per era, with p-values |
| lottomax_pdf_final.py / lotto_max_jeu_final.pdf | Printable ticket grids of optimal-10 (p.1) and sharing-10 (p.2) |
| lottomax_sharing.py / sharing_lines.csv / sharing_comparison.csv | Popularity model → lines minimising expected jackpot co-winners (imports lottomax_optimal.py) |
| LOTTO_MAX_HANDOFF.md | This file |

---

## 12. Open items
- [x] **Push the whole `lotto` folder to GitHub** — done 2026-09-28 (`canadaservcorp-tech/lotto`).
- [ ] Ask retailer whether all 4 lines of a play can be chosen (would allow 36–40 chosen lines).
- [ ] Refresh `d/LOTTOMAX.csv` after each draw before re-running scripts.
