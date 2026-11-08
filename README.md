# lattizzo-framework

Code, protocols and a small demo for the paper *An Animal Called Lattizzo. Naming New Dress in the Sumptuary Laws of Renaissance Italy and Ming China* (DH2027).

The paper asks whether a dress name appears first in a sumptuary law or first in other records, and how often laws never name it at all. We extract names with a large language model, check every extracted term by hand, merge spellings into dated concepts, and compare first years inside and outside the law. This repository holds the full method and runs end to end on 19 real records.

[中文说明](README_zh.md)

## What is in this repository

| Folder | Content |
|---|---|
| `src/` | The pipeline. Extraction, review sheet, concepts, merge audit, measures, agreement, SKOS export |
| `prompts/` | The two prompts used in the paper, byte for byte. SHA-256 values are listed below |
| `demo/` | 19 real records from published editions, cached model replies, a reviewed merge table for the sample concepts, clause codes, and the expected output |
| `docs/` | Method, merge rules, data schema, clause codebook, annotation guidelines, and the frozen pre-registration with an English summary |
| `sample/` | 14 concepts discussed in the paper, as CSV and SKOS |
| `results/` | The summary counts reported in the paper's tables and appendix |

The full corpus, the gold standard, the concept table and the complete model output belong to an ongoing doctoral project. They are not released at this stage. Everything needed to see how each number is produced is here, and the demo shows each step on real text.

## Quick start

```
pip install -r requirements.txt
bash run_demo.sh
```

No API key is needed. The demo reads cached replies of the main model from `demo/model_output.jsonl`. Output goes to `out/` and can be compared with `demo/expected/`. To call a model yourself, put your key in a local `.env` file and see `src/extract.py`.

## Pipeline

| Step | Script | Human work |
|---|---|---|
| 1. Extract names, category and wearer from each record | `src/extract.py` | Gold standard annotated before any model run |
| 2. Check every extracted term against the source | `src/review_sheet.py` | Keep, drop, or mark as generic |
| 3. Merge spellings into concepts | `src/build_concepts.py`, `src/merge_audit.py` | Each merge decided in context, rules in `docs/merge_rules.md` |
| 4. Coverage classes, not-named share, new concepts per clause, rank share | `src/measure.py` | Clause coding by codebook, second coder on a sample |
| 5. Dated vocabulary in SKOS | `src/build_vocab.py` | AAT matches confirmed one by one |
| Agreement | `src/agreement.py` | |

`docs/method.md` explains each step and the coverage rule in full.

## What the demo shows

The demo runs step 3 twice, once without and once with the reviewed merge table. On the same 19 records the two runs give different classes for the same words.

| Concept | Without merging | With merging |
|---|---|---|
| lattizzo | *lattizzi* (Sacchetti, 1395) not named; *lattitij* (law of 1472) law only | outside-first, lagging. Named in a story in 1395, in a law in 1472 |
| ghirlanda | *grillanda* outside-first; *ghirlande* not named | undecided. The word is already in the law of 1356 |
| gamurra | *gamurra* not named; *ghamurre* law only | law-first |

This is the main methodological point of the paper. Spelling decisions move words between classes, so merging has to be done by a person, with rules fixed in advance. `src/merge_audit.py` lists candidate pairs. In the demo it finds *lattitij*/*lattizzi* and *gamurra*/*ghamurre*, and also false pairs such as *cappello*/*coppelle*, which a reader must reject.

The demo numbers are not the paper's results. Nineteen records are too few for the measures to mean anything. The paper's counts are in `results/`.

## Models and prompts

| Task | Prompt | SHA-256 | Models | Call dates |
|---|---|---|---|---|
| Term extraction | `prompts/extraction_prompt_v3.txt` | `4de5ce25b0daade28289fe86efadc68fe4d856b5f08e3ac0861d9748f99841ea` | gpt-6-sol (main), claude-sonnet-5-5, deepseek-v4-pro | 2026-10-28 and 29 |
| Clause coding | `prompts/clause_prompt_m2_v1.txt` | `e3afab1b85f0ee0575bc1c72b52ca7bb671a94c8620ddcc9c7cdceb4cca05022` | the same three, two runs each | 2026-10-30 |

Temperature 0, no reasoning mode, one call per record. claude-sonnet-5-5 does not accept a temperature setting and ran with the default. Model output is used only after human review. Clause codes in the paper are the author's; model codes serve as a check.

## Pre-registration

The study design, hypotheses and decision rules were written before any extraction or measurement and committed on 2026-10-20 at 16:41:22 +02:00.

```
sha256sum docs/prereg/prereg_frozen_995a0d0.md
cf31ce0d81655b2e4f87c5cfaff23dcff4e0410f003890826d533eedd8a20b6d
```

Sections 1 to 10 were frozen at that commit. Every later change was appended to section 11 with date, content and reason. `docs/prereg/summary_en.md` summarizes the registered text in English, together with the changes logged in section 11. The pre-registration was kept in the project repository and was not filed with an external registry.

## Licence

Code under the MIT licence. Documentation, prompts, sample and results under CC BY 4.0. The demo texts come from published editions and public-domain sources listed in `demo/records.csv`.

## Citation

See `CITATION.cff`.
