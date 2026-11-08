# Pre-registration, English summary

The original is in Chinese. `prereg_frozen_995a0d0.md` is the version committed on 2026-10-20 at 16:41:22 +02:00 (SHA-256 `cf31ce0d81655b2e4f87c5cfaff23dcff4e0410f003890826d533eedd8a20b6d`). After freezing, changes were only appended to section 11 of the project file, with date, content and reason. This summary follows the section numbers of the original and ends with an overview of section 11.

## 0. What had been seen before registration

The structure of the existing data tables and some of their entries. Pages 62 to 102 of Wu Renshu (1999) on women's dress. One rough string match between Italian non-law words and key sentences of the laws, with no full text, no merging and no coverage check. It was not used to set any hypothesis or parameter. No extraction, review, merging, coding or measurement had been done.

## 1. Research questions

RQ1. Does a dress name appear first in a law or first in other records, and how many years apart? How do the Italian cities and Ming China differ?
RQ2. When a law acts, does it target an object, or does it define what a rank may wear? How does the share of each kind change over time?
RQ3. Can model-assisted extraction with human review build a reliable dated vocabulary from Italian vernacular and Classical Chinese? Where do the errors fall?

## 2. Hypotheses

H1. In the Italian cities a good share of dress names appear outside the law first and enter the law later.
H2. After the Hongwu and Yongle reigns, Ming central laws rarely name new women's dress. New late Ming fashions appear in gazetteers and commentary, often described as appropriating rank dress.
H3. The share of rank clauses in the Italian laws rises in the sixteenth century. Ming laws are mainly rank clauses from the start.

## 3. Decision rules

The sample is small and purposive, so there are no significance tests. Results are reported as n/N. The main window w is 25 years, with 10 and 50 as sensitivity checks.

H1 is read in Florence, with Venice reported on its own. Among decidable concepts, outside-first must outnumber law-first. The result counts as stable support only if it holds in at least two of the three windows.

H2 needs both parts. H2a: from 1425, Ming central law clauses name fewer new concepts per clause than Florentine clauses from 1400. A new concept is one not seen in any earlier law of the same unit. H2b: the not-named share M3 is higher in Ming central than in Florence.

H3 needs both parts. H3a: in Florence the share of rank clauses from 1500 is at least 15 points higher than before 1500. H3b: in Ming central laws of 1368 to 1424 the rank share is at least 50%. Mixed clauses are counted on their own, and the result must hold with mixed counted as rank and as item.

## 4. Known cases

Eight cases with expected results written before the run (K1 to K8), used as a check of the pipeline. They include buttons, ermine and cut hat tails in the Florentine law of 1356 with Sacchetti's novella 137, the Florentine law of 1562 on gold and silver by rank, the Tianshun 2 (1458) ban on python and flying-fish patterns, and the Hongwu 3 (1370) rule on the ornaments of commoners' wives.

## 5. Corpus and scope

Legislative units Florence, Venice, Ming central and Ming local. Years 1355 to 1600, Ming accounts up to 1644 marked apart. Word classes garments, headwear and jewellery, materials and techniques. Colours and patterns go to an appendix. Generic words do not enter M1 or M3. Sources are grouped as laws, law-derived records (registrations, seizures, prosecutions, not used in M1 or M3) and independent records (inventories, account books, letters, gazetteers, notes, sermons, literature, objects). Calendar years are converted to a 1 January start.

## 6. Measures

L is the first year a concept appears in a unit's laws, N its first year in the unit's independent records, k = 3 records.

| Case | Condition | Class |
|---|---|---|
| N before L | the unit has a collected dress law before N | outside-first, lag L minus N |
| L before N | the unit has at least k independent records in the w years before L | law-first, lag N minus L |
| L equals N | | same year |
| only N | the unit has a collected dress law after N | not named |
| only L | at least k independent records within w years of L | law only |
| otherwise | | undecided |

Outside-first is split into lagging (a collected law between N and L did not name the concept) and first response. Known laws missing from the corpus are counted, and a lag is then reported as an upper bound. M3 is the share of not named among concepts first seen in independent records after the unit's first law, over the four classes outside-first, same year, law-first and not named. M2 codes each clause as item, rank or mixed, with the decision order given in `docs/codebook/`. The Ming expectation was written down in advance. Most Ming central laws are early and most Ming independent records are late, so many Ming concepts were expected to be undecided in M1, and the Ming side rests mainly on M2 and M3.

## 7. Extraction

One prompt revision was allowed after a trial on 20 records outside the gold standard. Model names and settings were to be registered before the run. Temperature 0. The gold standard is run twice and the agreement between runs reported.

## 8. Gold standard

Stratified random sample by language and source group, seed 20261020, annotated before any model run without looking at model output, frozen after annotation.

## 9. Validation

V1 precision, recall and F1 by language with error types. V2 the known cases. V3 the sensitivity analyses of section 5 and the three windows. V4 a second coding of about a third of the law clauses.

## 10. Checkpoint

A rule for 26 October on the number of Ming accounts, with fixed thresholds for continuing, narrowing or switching design. The design continued.

## 11. Changes after freezing

Every row gives date, section, content and reason. The main groups, in order.

**Before any data processing (2026-10-20 to 10-28).** The second human annotator of the gold standard was replaced by a blind re-annotation by the author after seven days, because no second annotator was available, and model coding of all clauses was added as a check. Ming central law text taken from the *Mingshi*. Ming independent records exclude literature; Italian literature kept, with a sensitivity test. Women's dress only, the same rule on both sides. Textile production records set aside from the main analysis and added back as a test. Latin dropped. Gold standard changed to 140 records. Annotation fields refined. Prompt v2 added the wearer field; v3 was the one permitted revision after the trial. Three models registered with their settings.

**Before measurement (2026-10-29 to 11-03).** Scoring rule for choosing the main model fixed before any score was computed; gpt-6-sol chosen. Review scheme for model output. Errata to the gold standard by a mechanical rule, with the frozen file left unchanged. Concept and attestation tables built. Clause coding by the author frozen before any model code was opened; disagreements adjudicated. Implementation details of the measures fixed before running them.

**After first results (2026-11-04 to 11-06), reported as deviations.** A source audit removed historians' summaries mixed into some Italian records. The merge audit, prompted by reviewer comments, applied the merge rules again to all concepts and joined 26 groups of spellings. It changed H1 from supported to not supported (13 to 13 in the main window, 13 to 2 at w = 10); H2 and H3 did not change. Exploratory analyses that change no decision. A second human coder for 30 clauses, registered before coding (kappa 0.87 against the final codes, H3 unchanged).
