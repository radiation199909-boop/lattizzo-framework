"""Shared helpers: file paths, record loading, robust JSON parsing of model output."""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from opencc import OpenCC
    to_simplified = OpenCC('t2s').convert
except ImportError:  # the demo still runs without OpenCC; Chinese labels are then not normalized
    to_simplified = lambda s: s


def side_of(record):
    """Each corpus side has its own vocabulary: 'it' for Italian records, 'zh' for Chinese records."""
    return 'zh' if record['language'] == 'zh' else 'it'


def read_csv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fields = fields or (list(rows[0]) if rows else [])
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def load_records(path):
    return {r['record_id']: r for r in read_csv(path)}


def year(record):
    y = str(record.get('year', '')).strip()
    return int(y) if y.isdigit() else None


def parse_model_json(raw):
    """Parse the JSON object in a model reply. The raw reply is never changed.
    One repair only: remove trailing commas before } or ], which JSON does not allow."""
    m = re.search(r'\{.*\}', raw or '', re.S)
    if not m:
        return None, False
    try:
        return json.loads(m.group(0)), False
    except json.JSONDecodeError:
        try:
            return json.loads(re.sub(r',\s*([}\]])', r'\1', m.group(0))), True
        except json.JSONDecodeError:
            return None, False


def load_model_output(path):
    """Read a JSONL file written by extract.py. Lines whose 'parsed' field is empty are parsed again from 'raw'."""
    out = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            d['repaired'] = False
            if not d.get('parsed'):
                d['parsed'], d['repaired'] = parse_model_json(d.get('raw', ''))
            out.append(d)
    return out
