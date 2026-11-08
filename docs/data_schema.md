# Data schema

All tables are UTF-8 CSV with a header row. The demo files follow these layouts.

## records.csv

| Column | Meaning |
|---|---|
| record_id | identifier, such as FI1472-03 or MING-C-15 |
| unit | legislative unit, Florence or Ming-central |
| year | year with a 1 January start |
| group | law or other |
| genre | law, literature, letter, account book, chronicle, miscellany (biji), local gazetteer, commentary |
| language | it or zh |
| text | the passage as given in the edition |
| source | edition and page |
| section_heading | Ming central laws only, the heading under which the clause stands. It often names the rank |

## model_output.jsonl

One JSON object per model call.

| Field | Meaning |
|---|---|
| record_id, run | record and run label (gold, gold2, all) |
| provider, model_requested, model | API provider, model asked for, model name returned by the API |
| temperature, reasoning | 0 or default; none |
| prompt, prompt_sha256 | prompt file and its SHA-256 |
| time, usage | call time in UTC, token counts |
| raw | the reply text, unchanged |
| parsed | the reply parsed as JSON, `{"record_id": ..., "terms": [{"surface", "category", "wearer", "context"}]}` |

## merge_table.csv

| Column | Meaning |
|---|---|
| side | it or zh |
| surface | spelling as extracted |
| concept | concept label |
| generic | 1 if the word is generic |
| category | category set for the concept |
| note | the rule applied |

A spelling not in the table keeps its own form as concept label (lower case, simplified characters) and is marked reviewed=0.

## attestations.csv (output of build_concepts.py)

record_id, side, unit, year, group, genre, surface, concept, category, generic, wearer, reviewed, context.

## concepts.csv (output of build_concepts.py)

side, concept, alt_labels, category, generic, male_only, reviewed, n_att, n_records, first_year, first_record, first_law_year, first_other_year.

## clause_coding.csv

| Column | Meaning |
|---|---|
| record_id, unit, year | the law clause |
| code_human | the author's final code, item, rank or mixed |
| code_model | the main model's code, first run |
| non_dress | 1 if the clause regulates no dress (guest numbers, for example) |
| title_or_preface | 1 for titles and preambles |

## m1_concepts_w25.csv (output of measure.py)

unit, concept, cls, subclass, first_law, first_other.
