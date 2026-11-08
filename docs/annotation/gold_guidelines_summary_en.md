# Gold standard guidelines, English summary

The full guidelines are in Chinese in `gold_guidelines_zh.md`. They were used to annotate the gold standard by hand before any model was run.

## Basic rules

- No model output and no large language model may be used while annotating. Ordinary machine translation and printed glossaries may be used for Italian, and the tool used is noted.
- The annotator copies the spelling as it stands in the source. No translation, no correction, no change between traditional and simplified characters. OCR errors are copied too, with the correct form in notes.
- One row per dress word. A record with no dress word gets one row with an empty surface and the note "none".

## Fields

| Field | Content |
|---|---|
| surface | the spelling in the source |
| category | garment, headwear_jewelry, material_technique, color, pattern, generic |
| wearer | female, male, both, unclear |
| renamed | 1 when the text says the thing has another name ("commonly called", *detto*) |
| negated | 0 allowed or neutral (including required), 1 forbidden, 2 allowed up to a limit |
| combo | a shared label for words that together form the regulated thing |
| notes | doubts, OCR corrections, addressees, limits |

## Main decisions

- Attached decoration goes by where it is attached. Fringes, trims, embroidery and buttons sewn on clothes are material_technique. Things hung from a headdress, the hair, the ears or the neck are headwear_jewelry. A belt tied on its own is garment.
- Pearls, gold, silver and stones are material_technique when they are the material of a named thing, and headwear_jewelry when worn on their own.
- Compounds of material and object are split until each part is a dress word on its own, for example 金钗 into 金 and 钗. A compound is kept whole when a part would not stand alone, when the split is ambiguous, or when the first part gives shape or size rather than material.
- Named crowns and court dress are kept whole, for example 珠翠冠.
- Generic words (衣, 服, 饰, *vestimento*, *panni*) are generic only when they refer to dress in general. A word that points back to a named object takes that object's category.
- Verbs are not marked. Real flowers or charms worn on the body are marked by where they are worn.
- Wearers not marked by sex are decided in a fixed order. The text first, then a separate list of women in the same record, then fixed gender of an office or profession, then unclear.
- Spelling variants are each recorded. Merging is done later.

## Two-level combo

A letter stands for one whole thing and a letter with a number for one part of it, such as a crown (a) with its kingfisher dragons (a1) and golden phoenixes (a2). Things listed side by side each get a letter. Each record starts again from a.
