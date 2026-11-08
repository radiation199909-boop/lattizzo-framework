"""Step 3b. List concept pairs that may be spellings of one word, for a person to decide.

This script never merges anything. It writes candidate pairs; each decision goes into the merge table by hand.
Italian: same form after spelling normalization, edit distance 1 (or 2 for long words), letter transposition, truncated forms.
Chinese: same string after replacing known variant characters.
The column cross=1 marks pairs where one form is seen in a law and the other only outside laws.
These pairs matter most, because merging them can move a concept from one coverage class to another.
"""
import argparse, collections, itertools, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv

RULES = [('ch', 'c'), ('gh', 'g'), ('h', ''), ('zz', 'z'), ('z', 'c'), ('tij', 'ci'), ('ti', 'ci'), ('j', 'i'), ('y', 'i'),
         ('ll', 'l'), ('tt', 't'), ('cc', 'c'), ('ss', 's'), ('rr', 'r'), ('pp', 'p'), ('nn', 'n'), ('mm', 'm'),
         ('bb', 'b'), ('ff', 'f'), ('dd', 'd'), ('gg', 'g'), ('ar', 'er'), ('u', 'v')]
# a short list of variant characters met in the Ming sources; extend it for other corpora
VARIANTS = {'䌷': '绸', '袴': '裤', '帬': '裙', '鞵': '鞋', '鞾': '靴', '背': '褙', '䯼': '鬏', '綵': '彩', '縧': '绦', '絛': '绦',
            '襴': '襕', '珮': '佩', '釵': '钗', '璫': '珰', '摺': '褶', '帊': '帕', '襖': '袄'}


def norm_it(s):
    s = s.lower().replace(' ', '').replace('-', '')
    for x, y in RULES:
        s = s.replace(x, y)
    return re.sub(r'[aeiou]+$', '', s)


def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[:], i
        for j, y in enumerate(b, 1):
            d[j] = min(p[j] + 1, d[j - 1] + 1, p[j - 1] + (x != y))
    return d[-1]


def reason_it(x, y):
    nx, ny = norm_it(x), norm_it(y)
    if nx == ny:
        return 'same after normalization'
    if min(len(nx), len(ny)) >= 5 and lev(nx, ny) == 1:
        return 'edit distance 1'
    if min(len(nx), len(ny)) >= 7 and lev(nx, ny) == 2:
        return 'edit distance 2'
    if len(nx) == len(ny) >= 5 and sorted(nx) == sorted(ny):
        return 'transposition'
    if (x.endswith('-') and y.startswith(x[:-1])) or (y.endswith('-') and x.startswith(y[:-1])):
        return 'truncated form'
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--attestations', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    info = collections.defaultdict(lambda: collections.defaultdict(set))
    for x in read_csv(a.attestations):
        if x['generic'] == '1':
            continue
        k = (x['side'], x['concept'])
        info[k]['law' if x['group'] == 'law' else 'other'].add(x['year'])
        info[k]['surfaces'].add(x['surface'])
    out = []
    for side in ('it', 'zh'):
        for p, q in itertools.combinations(sorted(k for k in info if k[0] == side), 2):
            x, y = p[1], q[1]
            if side == 'it':
                why = reason_it(x, y)
            else:
                why = 'variant characters' if len(x) >= 2 and len(x) == len(y) and \
                    ''.join(VARIANTS.get(c, c) for c in x) == ''.join(VARIANTS.get(c, c) for c in y) else ''
            if not why:
                continue
            ip, iq = info[p], info[q]
            out.append(dict(side=side, a=x, b=y, reason=why, cross=int(bool((ip['law'] and iq['other']) or (iq['law'] and ip['other']))),
                            a_law_years=';'.join(sorted(ip['law'])), a_other_years=';'.join(sorted(ip['other'])),
                            b_law_years=';'.join(sorted(iq['law'])), b_other_years=';'.join(sorted(iq['other'])),
                            decision='', note=''))
    write_csv(a.out, out, ['side', 'a', 'b', 'reason', 'cross', 'a_law_years', 'a_other_years', 'b_law_years', 'b_other_years', 'decision', 'note'])
    print('candidate pairs', len(out), 'of which cross law/other', sum(o['cross'] for o in out), '->', a.out)


if __name__ == '__main__':
    main()
