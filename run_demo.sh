#!/usr/bin/env bash
# End-to-end run on the demo records. No API key is needed: the model replies are cached in demo/model_output.jsonl.
# Outputs go to out/. Compare them with demo/expected/.
set -euo pipefail
cd "$(dirname "$0")"
OUT=out
PY=${PYTHON:-python3}
mkdir -p "$OUT"

echo "== 1. extraction (cached replies; to call a model instead see src/extract.py)"
"$PY" src/extract.py --records demo/records.csv --provider openai --model any --out "$OUT/unused.jsonl" --ids FI1472-03 --dry-run | head -5
echo "..."

echo "== 2. review sheet for the human check"
"$PY" src/review_sheet.py --records demo/records.csv --model-output demo/model_output.jsonl --out "$OUT/review_sheet.csv"

echo "== 3a. concepts without the reviewed merge table"
"$PY" src/build_concepts.py --records demo/records.csv --model-output demo/model_output.jsonl --out "$OUT/no_merge"
echo "== 3b. merge candidates for a person to decide"
"$PY" src/merge_audit.py --attestations "$OUT/no_merge/attestations.csv" --out "$OUT/merge_candidates.csv"
echo "== 3c. concepts with the reviewed merge table"
"$PY" src/build_concepts.py --records demo/records.csv --model-output demo/model_output.jsonl --merge-table demo/merge_table.csv --out "$OUT/merged"

echo "== 4a. measures without merging"
"$PY" src/measure.py --records demo/records.csv --attestations "$OUT/no_merge/attestations.csv" --clauses demo/clause_coding.csv --out "$OUT/no_merge"
echo "== 4b. measures with merging"
"$PY" src/measure.py --records demo/records.csv --attestations "$OUT/merged/attestations.csv" --clauses demo/clause_coding.csv --out "$OUT/merged"

echo "== 5. SKOS vocabulary"
"$PY" src/build_vocab.py --concepts "$OUT/merged/concepts.csv" --out "$OUT/merged/vocab.ttl" || echo "(rdflib not installed; skipped)"

echo "== 6. clause coding agreement, author vs model"
"$PY" src/agreement.py demo/clause_coding.csv code_human code_model

echo "== four words from the paper, merged run, window 25"
grep -E "^Florence,(lattizzo|manichini|ghirlanda|coppelle)," "$OUT/merged/m1_concepts_w25.csv" || true

echo "== check against demo/expected"
for f in no_merge/measures.txt merged/measures.txt no_merge/m1_concepts_w25.csv merged/m1_concepts_w25.csv; do
  if cmp -s "$OUT/$f" "demo/expected/$f"; then echo "same as expected: $f"; else echo "DIFFERS from expected: $f"; fi
done
