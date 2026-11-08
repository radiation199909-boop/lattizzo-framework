"""Agreement between two codings of the same items: raw agreement and Cohen's kappa.
Used in the paper for clause coding (author vs model, author vs second coder) and for the gold-standard re-annotation.
    python src/agreement.py demo/clause_coding.csv code_human code_model
"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    path, f1, f2 = sys.argv[1:4]
    rows = [r for r in read_csv(path) if r[f1] and r[f2]]
    po, k = kappa([r[f1] for r in rows], [r[f2] for r in rows])
    print(f'{f1} vs {f2}: n={len(rows)}  agreement={po:.3f}  kappa={k:.3f}')
    for r in rows:
        if r[f1] != r[f2]:
            print(f'  differs: {r["record_id"]}  {f1}={r[f1]}  {f2}={r[f2]}')


if __name__ == '__main__':
    main()
