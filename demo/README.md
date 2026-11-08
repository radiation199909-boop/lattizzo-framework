# Demo

Nineteen real records, chosen because the paper discusses them or because they show one step of the method. Twelve are Florentine (seven law clauses and five other records) and seven are Ming central (four law clauses and three other records). The texts come from the editions listed in the `source` column.

| File | Content |
|---|---|
| `records.csv` | the 19 records |
| `model_output.jsonl` | replies of the main model, gpt-6-sol, prompt v3, called on 2026-10-28 and 29, unchanged |
| `merge_table.csv` | reviewed merge decisions for the sample concepts only. Other spellings fall back to their own form |
| `clause_coding.csv` | author's final code and the main model's code for the 11 law clauses |
| `expected/` | output of `run_demo.sh` for comparison |

Editor footnotes at the end of FI-03 and FI-05 were removed from the text shown here. The model saw them and extracted nothing from them.

The model output in the demo has not been reviewed. In the paper every term passed through the review of step 2 before merging.

Records worth reading first.

| Record | Why |
|---|---|
| LE-02 | Sacchetti, novella 137. The notary cannot write down *lattizzi* and *coppelle* |
| FI1472-03 | the law of 1472 that names *lattitij* |
| FI-05, FI1472-10 | *manichini* in an account book of 1447 and in a law of 1472 |
| FI1356-006, FI1562-02 | *ghirlanda* in 1356 and *grillanda* in 1562 |
| MING-I-ZSFF | Tan Qian's note on 仰心髻, a hairstyle no collected law names |
| MING-C-15, MING-C-64 | the rank clause of 1370 and the item clause of 1458 in Table 2 of the paper |
