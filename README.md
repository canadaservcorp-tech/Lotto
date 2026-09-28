# lotto — Lotto Max study
Start with `LOTTO_MAX_HANDOFF.md` (full summary, results, final lines).

- `scripts/` — all Python scripts. Scripts read `d/LOTTOMAX.csv`, so first run:
  `cd scripts && ln -s ../data d`
- `data/` — official BCLC raw files (LOTTOMAX.csv, 649.csv), downloaded 2026-09-26.
  Refresh: https://www.playnow.com/resources/documents/downloadable-numbers/LOTTOMAX.zip
- `results/` — workbooks, CSVs and PDFs produced by the scripts.

Requirements: Python 3, pandas, numpy, openpyxl, reportlab.

Optimal line selector: `cd scripts && python3 lottomax_optimal.py --n 10 --draws 1000000 --out ../results`
(~1 min; writes `results/optimal_lines.csv` and `results/optimal_comparison.csv`).
Randomness battery: `python3 lottomax_randomness.py --sims 4000 --out ../results` (seconds).
Sharing-risk optimizer: `python3 lottomax_sharing.py --out ../results` (~1 min; run after lottomax_optimal.py).
