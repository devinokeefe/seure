# Code

Python 3.9 or later, standard library only (see requirements.txt). Run everything from the top folder of the
repository. The scripts read from data/ and write to results/. Several of them use all processor cores.

## Everything at once

```
python code/reproduce.py            # run all steps, then print each documented figure next to the recomputed one
python code/reproduce.py --check    # print the comparison from the result files already present
python code/reproduce.py --only key heldout    # run only some steps
```

A full run took about 14 minutes on the desktop computer on which the release was prepared (32 threads, with other
work running at the same time); allow 15 to 30 minutes. The comparison table is written to results/reproduce_summary.txt; the exit status is 1 if a figure differs.

## The steps one by one

| command | what it does | writes | time |
|---|---|---|---|
| `python code/build_key.py` | aligns the known-plaintext sets with their plaintext and re-estimates the key until it is stable; compares the result with data/key/key.csv | results/align_*.txt, key_train.tsv, key.csv, key.json, build_log.txt | 1 min |
| `python code/build_key.py --publish` | the same, then copies key.csv and key.json to data/key/ and regenerates the tables in docs/KEY.md and docs/SYMBOLS.md | as above, and those files | 1 min |
| `python code/build_key.py --seed data/key/seed_letter40.tsv --out results/seed_letter40` | the same from another starting key; reports how the key differs | results/seed_letter40/ | 1 min |
| `python code/heldout.py --update none n5maj n5orig n5all` | decodes the three copies of the held-out block C blind and scores them; with the key as built and with three ways of applying the revised values | results/heldout.txt, heldout_classes.tsv | 6 min |
| `python code/decode39.py` | machine decode of letter 39 at three language-model weights, with the class of every word; checks and tallies the proposed reading | results/letter39_decode.txt | 2 min |
| `python code/decode39.py --update n5orig --beam 400` | the same with the revised values | results/letter39_decode_n5orig.txt | 2 min |
| `python code/score_reading.py` | scores the competing readings listed in data/fr3151/letter39_tests.tsv | results/letter39_tests.txt | 10 s |
| `python code/score_reading.py --span L16.14-L17.3 "et au pis aller" "et a pis aller"` | scores readings of your own for any span (line.sign, counted from 0, both ends included; write u for v and i for j) | prints only | 10 s |
| `python code/compare_readers.py` | agreement between the two transcriptions of letter 39 | results/letter39_readers.txt | 1 s |
| `python code/keyfit_control.py` | does the letter-40 key fit letter 39: real order against shuffled order and permuted key | results/keyfit_control.txt | 1 min |
| `python code/naf6638_check.py` | NAF 6638: the two cipher blocks against the copy's clear text, with shuffled controls, per-page tests and Falgairolle's variants | results/naf6638_check.txt, align_N5.txt | 2 min |

`build_key.py` must be run before the scripts that use the key (they read results/align_*.txt), and `heldout.py`
before `decode39.py` if the class precisions are to be shown. The result files of the last run are included in
results/, so every script can also be run by itself.

## Modules

- **common.py**: file formats, normalisation of the plaintext, reading of the alignment listings.
- **aligner.py**: the known-plaintext aligner (a banded dynamic programme; the costs are at the top of the file).
- **decoder.py**: key model, character language model, beam-search decoder, word classes, and the key updates
  `none`, `n5maj`, `n5orig`, `n5all`.

Key updates: `none` is the key as built from fr. 3151. `n5maj` adds, for the nine signs re-read from NAF 6638, the
count of their majority value there. `n5orig` is `n5maj` with the two alignment artefacts (`mt`, `A`) also
corrected in the fr. 3151 counts. `n5all` adds every unit aligned with those signs in NAF 6638.

## Determinism

The scripts use fixed random seeds for their shuffled controls and no other source of randomness. On the machine
used, repeated runs gave identical output. Results could differ in the last digit on a Python build whose
floating-point library rounds differently; the comparison in reproduce.py is on the printed digits.

## Not included

The programs used along the way for image segmentation, for the first key of letter 40, for sorting sign crops
and for the many abandoned attempts are exploratory and are not part of this release. The key update values in
data/key/naf6638_n5_values.tsv were read off with one of those programs; here they are data.
