"""Step 3. Turn extracted terms into attestations and concepts.

A concept is one dress name on one side ('it' or 'zh'). Spellings are joined into one concept only through the merge table,
which a person fills by reading each spelling in context (rules in docs/merge_rules.md). A spelling missing from the table
falls back to an automatic form (lower case for Italian, simplified characters for Chinese) and is marked reviewed=0.

Terms are kept when the category is a dress category. Terms for men only (wearer=male) and generic words
(category=generic, or generic=1 in the merge table) stay in the attestation file and are left out of the measures later.

Outputs
    attestations.csv   one row per term occurrence
    concepts.csv       one row per concept, with first year in a law and first year in any other record
"""
import argparse, collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_model_output, load_records, read_csv, side_of, to_simplified, write_csv, year

DRESS = {'garment', 'headwear_jewelry', 'material_technique', 'color', 'pattern', 'generic'}


def auto_label(side, surface):
    return to_simplified(surface) if side == 'zh' else surface.lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', required=True)
    ap.add_argument('--model-output', required=True)
    ap.add_argument('--merge-table', help='reviewed spelling-to-concept table; leave out to see the result without merging')
    ap.add_argument('--out', required=True, help='output folder')
    a = ap.parse_args()

    R = load_records(a.records)
    M = {}
    if a.merge_table:
        for m in read_csv(a.merge_table):
            M[(m['side'], m['surface'])] = m

    att = []
    for d in load_model_output(a.model_output):
        r = R.get(d['record_id'])
        if r is None or not d['parsed']:
            continue
        side = side_of(r)
        for t in d['parsed'].get('terms', []):
            s = str(t.get('surface', '')).strip()
            cat = t.get('category', '')
            if not s or cat not in DRESS:
                continue
            m = M.get((side, s)) or M.get((side, to_simplified(s)))
            if m and m.get('delete') == '1':
                continue
            att.append(dict(record_id=r['record_id'], side=side, unit=r['unit'], year=r['year'], group=r['group'], genre=r['genre'],
                            surface=s, concept=m['concept'] if m else auto_label(side, s),
                            category=(m['category'] if m and m.get('category') else cat),
                            generic=int(m['generic'] == '1') if m else int(cat == 'generic'),
                            wearer=t.get('wearer', 'unclear'), reviewed=int(bool(m)), context=t.get('context', '')))

    by = collections.defaultdict(list)
    for x in att:
        by[(x['side'], x['concept'])].append(x)
    concepts = []
    for (side, label), xs in sorted(by.items()):
        ys = lambda grp: [int(x['year']) for x in xs if x['group'] == grp and str(x['year']).isdigit()]
        first = min(xs, key=lambda x: (int(x['year']) if str(x['year']).isdigit() else 9999, x['record_id']))
        concepts.append(dict(side=side, concept=label, alt_labels='|'.join(sorted({x['surface'] for x in xs} - {label})),
                             category=collections.Counter(x['category'] for x in xs).most_common(1)[0][0],
                             generic=int(any(x['generic'] for x in xs)), male_only=int({x['wearer'] for x in xs} == {'male'}),
                             reviewed=int(all(x['reviewed'] for x in xs)), n_att=len(xs), n_records=len({x['record_id'] for x in xs}),
                             first_year=first['year'], first_record=first['record_id'],
                             first_law_year=min(ys('law'), default=''), first_other_year=min(ys('other'), default='')))
    write_csv(os.path.join(a.out, 'attestations.csv'), att)
    write_csv(os.path.join(a.out, 'concepts.csv'), concepts)
    print(f'attestations {len(att)}  concepts {len(concepts)}  reviewed concepts {sum(c["reviewed"] for c in concepts)}  -> {a.out}')


if __name__ == '__main__':
    main()
