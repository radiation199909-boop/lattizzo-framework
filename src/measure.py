"""Step 4. Coverage classes (M1), the not-named share (M3), new concepts per clause (H2a) and the rank share of clauses (H3).
Definitions follow the pre-registration (docs/prereg/prereg_frozen_995a0d0.md, sections 3 and 6, with the implementation
details logged in section 11 on 2026-11-03). In short, for a concept in one unit, let L be its first year in a law and
N its first year in any other record, and w the window in years:

    outside-first   N < L, and the unit has a collected law before N.
                    subclass 'lagging' when a collected law falls strictly between N and L
    law-first       L < N, and the unit has at least 3 other records dated in [L - w, L)
    same year       L = N
    not named       the concept is never seen in a law, and the unit has a collected law after N
    law only        only in laws, with at least 3 other records in [L - w, L + w]
    undecided       everything else

H1: in Florence, outside-first > law-first, read in the main window (25) and judged stable when it holds in at least 2 of 3 windows.
M3: not named / (outside-first + same year + law-first + not named), over concepts first seen after the unit's first law.
Only dress concepts in the main categories enter; generic words and terms for men only are left out.
"""
import argparse, collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_records, read_csv, write_csv, year

MAIN_CATS = {'garment', 'headwear_jewelry', 'material_technique'}
WINDOWS = (10, 25, 50)
MAIN_W = 25
H2A_START = {'Florence': 1400, 'Ming-central': 1425}  # prereg section 6
H3_SPLIT = 1500               # Florence: clauses before and from 1500
H3_MING = (1368, 1424)        # Ming central: early clauses
CLASSES = ['outside-first', 'law-first', 'same year', 'not named', 'law only', 'undecided']


def first_years(att, R):
    """(unit -> concept -> first law year) and (unit -> concept -> first other-record year)."""
    L, N = collections.defaultdict(dict), collections.defaultdict(dict)
    for x in att:
        if x['generic'] == '1' or x['wearer'] == 'male' or x['category'] not in MAIN_CATS:
            continue
        r = R[x['record_id']]
        y = year(r)
        if y is None:
            continue
        D = L if r['group'] == 'law' else N
        D[r['unit']][x['concept']] = min(D[r['unit']].get(x['concept'], 9999), y)
    return L, N


def m1(att, R, w):
    law_years, other_years = collections.defaultdict(set), collections.defaultdict(list)
    for r in R.values():
        y = year(r)
        if y is not None:
            (law_years[r['unit']].add(y) if r['group'] == 'law' else other_years[r['unit']].append(y))
    L, N = first_years(att, R)
    res = {}
    for unit in sorted(set(law_years) | set(other_years)):
        ly, oy, out = sorted(law_years[unit]), other_years[unit], {}
        for c in set(L[unit]) | set(N[unit]):
            l, n, sub = L[unit].get(c), N[unit].get(c), ''
            if l is not None and n is not None:
                if n < l:
                    cls = 'outside-first' if any(y < n for y in ly) else 'undecided'
                    if cls == 'outside-first':
                        sub = 'lagging' if any(n < y < l for y in ly) else 'first response'
                elif l < n:
                    cls = 'law-first' if sum(l - w <= y < l for y in oy) >= 3 else 'undecided'
                else:
                    cls = 'same year'
            elif n is not None:
                cls = 'not named' if any(y > n for y in ly) else 'undecided'
            else:
                cls = 'law only' if sum(l - w <= y <= l + w for y in oy) >= 3 else 'undecided'
            out[c] = dict(cls=cls, sub=sub, L=l, N=n)
        first_law = ly[0] if ly else None
        den = [c for c, v in out.items() if v['N'] is not None and first_law is not None and v['N'] > first_law
               and v['cls'] in ('outside-first', 'same year', 'law-first', 'not named')]
        res[unit] = dict(concepts=out, counts=collections.Counter(v['cls'] for v in out.values()),
                         m3=(sum(out[c]['cls'] == 'not named' for c in den), len(den)))
    return res


def clause_ok(c):
    return c['non_dress'] == '0' and c['title_or_preface'] == '0'


def h2a(att, R, CC):
    """New concepts per law clause: concepts in a clause that no earlier law of the same unit had named."""
    by_rec = collections.defaultdict(set)
    for x in att:
        if x['generic'] == '0' and x['wearer'] != 'male' and x['category'] in MAIN_CATS and R[x['record_id']]['group'] == 'law':
            by_rec[x['record_id']].add(x['concept'])
    out = {}
    for unit, start in H2A_START.items():
        laws = sorted((k for k, r in R.items() if r['unit'] == unit and r['group'] == 'law'), key=lambda k: (year(R[k]), k))
        before = lambda y: set().union(*[by_rec[k] for k in laws if year(R[k]) < y])
        clauses = [k for k in laws if year(R[k]) >= start and k in CC and clause_ok(CC[k])]
        new = [len(by_rec[k] - before(year(R[k]))) for k in clauses]
        out[unit] = (sum(new), len(clauses))
    return out


def h3(CC, field):
    share = lambda ks: (sum(CC[k][field] == 'rank' for k in ks), len(ks))
    ok = [k for k in CC if clause_ok(CC[k])]
    fl = [k for k in ok if CC[k]['unit'] == 'Florence']
    return dict(fl_before=share([k for k in fl if int(CC[k]['year']) < H3_SPLIT]),
                fl_after=share([k for k in fl if int(CC[k]['year']) >= H3_SPLIT]),
                ming_early=share([k for k in ok if CC[k]['unit'] == 'Ming-central' and H3_MING[0] <= int(CC[k]['year']) <= H3_MING[1]]))


def ratio(x):
    return f'{x[0]}/{x[1]}' + (f' = {x[0] / x[1]:.2f}' if x[1] else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', required=True)
    ap.add_argument('--attestations', required=True)
    ap.add_argument('--clauses', help='clause coding table with columns record_id, unit, year, non_dress, title_or_preface and a code column')
    ap.add_argument('--code-field', default='code_human')
    ap.add_argument('--out', required=True, help='output folder')
    a = ap.parse_args()
    R, att = load_records(a.records), read_csv(a.attestations)
    lines, rows = [], []
    for w in WINDOWS:
        res = m1(att, R, w)
        lines.append(f'window w={w}')
        for unit, v in res.items():
            lines.append(f'  {unit:13s} ' + '  '.join(f'{k} {v["counts"][k]}' for k in CLASSES) + f'   M3 {ratio(v["m3"])}')
            if w == MAIN_W:
                rows += [dict(unit=unit, concept=c, cls=d['cls'], subclass=d['sub'], first_law=d['L'] or '', first_other=d['N'] or '')
                         for c, d in sorted(v['concepts'].items())]
        f = res.get('Florence', {}).get('counts', collections.Counter())
        lines.append(f'  H1 in this window: outside-first {f["outside-first"]} vs law-first {f["law-first"]} -> '
                     + ('holds' if f['outside-first'] > f['law-first'] else 'does not hold'))
    if a.clauses:
        CC = {c['record_id']: c for c in read_csv(a.clauses) if c['record_id'] in R}
        for unit, (n, k) in h2a(att, R, CC).items():
            lines.append(f'H2a {unit}: {n} new concepts in {k} clauses' + (f' = {n / k:.2f} per clause' if k else ''))
        h = h3(CC, a.code_field)
        lines.append(f'H3 Florence rank share before {H3_SPLIT}: {ratio(h["fl_before"])}; from {H3_SPLIT}: {ratio(h["fl_after"])}')
        lines.append(f'H3 Ming central rank share {H3_MING[0]}-{H3_MING[1]}: {ratio(h["ming_early"])}')
    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, 'measures.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    write_csv(os.path.join(a.out, 'm1_concepts_w25.csv'), rows, ['unit', 'concept', 'cls', 'subclass', 'first_law', 'first_other'])
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
