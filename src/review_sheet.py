"""Step 2. Write a review sheet for the human check of model output.

One row per extracted term, with the model's category, wearer and context. The reviewer fills the last three columns:
    decision            keep | drop | generic      (drop: not a dress term, or not in the source text)
    corrected_surface   the spelling as it stands in the source, when the model changed it
    note                free text
In the paper every extracted term was checked against the source text in this way before merging.
The demo skips this step and uses the model output as it is, so the effect of review can be seen by comparison.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_model_output, load_records, write_csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', required=True)
    ap.add_argument('--model-output', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    R = load_records(a.records)
    rows = []
    for d in load_model_output(a.model_output):
        if d['record_id'] not in R:
            continue
        for i, t in enumerate((d['parsed'] or {}).get('terms', []), 1):
            rows.append(dict(term_id=f"{d['record_id']}#{i}", record_id=d['record_id'], year=R[d['record_id']]['year'],
                             surface=t.get('surface', ''), category=t.get('category', ''), wearer=t.get('wearer', ''),
                             context=t.get('context', ''), decision='', corrected_surface='', note=''))
    write_csv(a.out, rows)
    print('review rows', len(rows), '->', a.out)


if __name__ == '__main__':
    main()
