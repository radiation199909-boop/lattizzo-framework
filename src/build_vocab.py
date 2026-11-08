"""Step 5. Write the concepts as a SKOS vocabulary in Turtle.
One ConceptScheme per side. The concept label is skos:prefLabel, the other spellings skos:altLabel.
The first year and first record go into skos:historyNote; category and counts into skos:scopeNote.
The namespace is a placeholder. Needs rdflib (pip install rdflib).
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, to_simplified
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SKOS

NS = Namespace('https://example.org/lattizzo/')
SCHEMES = {'it': ('Women\'s dress names in Italian records', 'it'), 'zh': ('Women\'s dress names in Ming records', 'zh-Hans')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--concepts', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    g = Graph()
    g.bind('skos', SKOS)
    g.bind('lz', NS)
    for side, (title, _) in SCHEMES.items():
        g.add((NS['scheme/' + side], RDF.type, SKOS.ConceptScheme))
        g.add((NS['scheme/' + side], SKOS.prefLabel, Literal(title, lang='en')))
    for i, c in enumerate(read_csv(a.concepts), 1):
        side, lang = c['side'], SCHEMES[c['side']][1]
        u = NS[f'concept/{side}-{i:04d}']
        g.add((u, RDF.type, SKOS.Concept))
        g.add((u, SKOS.inScheme, NS['scheme/' + side]))
        g.add((u, SKOS.prefLabel, Literal(c['concept'], lang=lang)))
        for alt in filter(None, c['alt_labels'].split('|')):
            alt_lang = lang if side == 'it' else ('zh-Hant' if to_simplified(alt) != alt else 'zh')
            g.add((u, SKOS.altLabel, Literal(alt, lang=alt_lang)))
        g.add((u, SKOS.scopeNote, Literal(f"category {c['category']}; {c['n_att']} occurrences in {c['n_records']} records", lang='en')))
        g.add((u, SKOS.historyNote, Literal(f"first seen {c['first_year']} ({c['first_record']}); first in a law {c['first_law_year'] or 'none'}", lang='en')))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    g.serialize(a.out, format='turtle')
    print('triples', len(g), '->', a.out)


if __name__ == '__main__':
    main()
