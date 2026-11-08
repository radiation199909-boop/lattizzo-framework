# Method

This file explains how the numbers in the paper are produced. Each step has a script in `src/` and runs on the demo.

## Corpus

Two legislative units are compared. Florence has 55 dress clauses and 41 other records. Ming central has 61 dress clauses and 49 other records. A record is one law clause or one dated passage from another kind of source, such as a letter, an account book, a story, a gazetteer or a miscellany. Each record carries its year, its unit, its group (law or other) and its source. Years follow a 1 January start. Only women's dress is counted. Clauses whose addressees are men only are left out on both sides.

## Step 1. Extraction

A model reads one record at a time and lists every word or short phrase that names a garment, a piece of headwear or jewellery, a material or technique, a colour or a pattern. For each it gives the category, the wearer (female, male, both, unclear) and a short context. The prompt is `prompts/extraction_prompt_v3.txt`.

Three models ran on the full corpus. The main model was chosen by its F1 on the gold standard in the first of two runs, with the scoring rule fixed before any score was computed. The gold standard was annotated by hand before any model run. Its guidelines are in `docs/annotation/`. The gold standard is also the set used to choose the model, so the error rates in the paper are development-set figures.

`src/extract.py` keeps every raw reply with the model name returned by the API, the prompt hash and the call time.

## Step 2. Review

Every term the model returned from a law went through a review sheet like the one from `src/review_sheet.py`. On the other side a random 30% of records in each language was reviewed the same way, and the rest was checked during merging. Words in the gold standard that the model missed were decided one by one and added. The reviewer checks the term against the source text and keeps it, drops it, or marks it as generic. The paper uses reviewed data only. In the demo this step is skipped, so the demo shows raw model output.

## Step 3. Concepts

One concept is one dress name on one side. Spellings become one concept only through the merge table, which a person fills in by reading each spelling in context. The rules are in `merge_rules.md`. `src/merge_audit.py` helps by listing candidate pairs, and a person decides each one.

Merging is the decision that most affects the results. In Florence, leaving spellings unmerged would raise the number of concepts from 331 to 482, and the count of outside-first against law-first concepts would change from 13 against 13 to 12 against 8. The demo shows the same effect on single words.

## Step 4. Measures

For a concept in a unit, L is its first year in a law and N its first year in any other record. Only the main categories count (garments, headwear and jewellery, materials and techniques). Generic words and terms for men only are left out.

| Class | Rule |
|---|---|
| outside-first | N before L, and the unit has a collected dress law before N |
| law-first | L before N, and at least 3 other records of the unit fall in the w years before L |
| same year | L equals N |
| not named | the concept never appears in a law, and the unit has a collected dress law after N |
| law only | only in laws, with at least 3 other records within w years of L |
| undecided | everything else |

The coverage conditions stop a class from being assigned when the sources are too thin to tell. An outside-first concept is called lagging when a collected law between N and L does not name it. The main window is 25 years, with 10 and 50 as checks.

The not-named share M3 counts the concepts first seen outside the law after the unit's first law, and asks how many of them no collected law ever names. Its denominator is the four classes outside-first, same year, law-first and not named.

New concepts per clause (H2a) counts, for each dress clause from 1400 in Florence and from 1425 in Ming central, the concepts that no earlier law of the same unit had named.

Each clause is also coded as item, rank or mixed (M2). The codebook is in `docs/codebook/`. The author's codes are used. A model coded all clauses twice as a check, and a second human coder coded a registered sample of 30 clauses. H3 compares the rank share of early and late clauses.

`src/measure.py` computes all of these. The decision rules for H1 to H3 are in the pre-registration.

## Step 5. Vocabulary

Concepts are written as SKOS, one scheme per side. The concept label is the preferred label and every other spelling an alternative label. First years and record identifiers go into history notes. Concepts seen in three or more records were checked against the Getty AAT, and each close match was confirmed by the author. `src/build_vocab.py` writes the SKOS file, and `sample/concepts_sample.ttl` shows 14 concepts from the paper.

## What a person decides

| Decision | Who | When |
|---|---|---|
| Gold standard | author | before any model run |
| Keep or drop each extracted term | author | after extraction, before merging |
| Merge spellings | author, by registered rules | before measurement; audited again after first results |
| Clause codes | author, blind to model codes | before opening model codes |
| AAT matches | author | after merging |

The model proposes terms and codes. Every number in the paper rests on these human decisions.
