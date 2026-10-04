# The cipher of Michel de Seure's letters from Lisbon, December 1558 (BnF ms. fr. 3151)

Author: Devin O'Keefe
Status: working release, 2026-10-04. Nothing in it has been peer-reviewed.

Michel de Seure, knight of Malta, was the French ambassador in Portugal from 1557 to 1559. Five of his letters from
Lisbon, dated 12 and 27 December 1558, survive in Paris, Bibliothèque nationale de France, ms. français 3151
(nos. 39, 40, 41, 43 and 44; digitised on Gallica). Long passages of them are written in a cipher of drawn signs and
numerals. This repository contains a transcription of those passages, a reconstruction of the key, a partial reading
of the one letter for which no contemporary decipherment is known, and one finding about a related manuscript.

## What the cipher is

A homophonic substitution cipher: each letter of the alphabet can be written with several different signs
(e, for instance, with at least four), and there are also signs for syllables (de, le, es, qui, pa, que), signs for
whole words (pour, faict and others), and nulls (signs that mean nothing, among them most of the numerals). u/v and
i/j are not distinguished. About 160 sign classes are distinguished in the transcription. See
[docs/KEY.md](docs/KEY.md) and [docs/SYMBOLS.md](docs/SYMBOLS.md).

## What has been done

1. **Transcription.** All cipher blocks of letters 40, 41, 43 and 44 (8,361 signs) and of letter 39 (405 signs) were
   transcribed from the Gallica images into ASCII sign labels ([data/](data/README.md)).
2. **Key, from known plaintext.** The volume itself contains contemporary decipherments: a sheet for letter 40
   (fo. 74r) and a sheet for letter 44 (fo. 85r-v). Letters 41 and 43 are further copies of the letter of 12 December
   that is no. 44, enciphered separately. The key was therefore **not broken blind**: it was recovered by aligning
   the cipher with these plaintexts. The result gives a value to 159 signs, 46 of them with high confidence, 30 with
   medium and 83 with low confidence ([docs/KEY.md](docs/KEY.md), [docs/METHOD.md](docs/METHOD.md)).
3. **A measured error rate.** The postscript of the letter of 12 December exists in three separately enciphered
   copies (1,057 signs). It was kept out of the key building and then decoded blind by the same program that is used
   for letter 39. The decoded text has a character accuracy of 0.51, 0.55 and 0.70 on the three copies (mean 0.59).
   So the automatic decoder gets a little more than half of the letters right; what is right clusters in words that
   can be recognised by measurable criteria ([docs/METHOD.md](docs/METHOD.md)).
4. **Letter 39 (fo. 71r), a partial reading.** No decipherment of this letter is known. About two thirds of its
   cipher passage is read here, word by word, each word with a confidence grade
   ([docs/LETTER39.md](docs/LETTER39.md)). The readable part says that Seure regards the peace as made, does not know
   what will come of it, does not want to stay in Lisbon much longer and at worst wants only to complete his two
   years, and is short of money.
5. **BnF ms. NAF 6638.** This 19th-century copy of Seure's despatches of 1559 (the originals are in St Petersburg)
   reproduces two cipher blocks of February 1559, sign by sign. They are in the same cipher. The clear text that the
   copy gives on pp. 29-34 turns out to be the decipherment of those two blocks. Falgairolle printed that text in
   1895 without saying, and apparently without noticing, that it is the content of the cipher
   ([docs/NAF6638.md](docs/NAF6638.md)).

## What is and is not claimed

Claimed:

- The sign values in the "high" rows of the key table are well established (each rests on at least 8 aligned
  occurrences, at least three quarters of them agreeing). Anyone can check them against the decipher sheets.
- The cipher of letter 39 is the cipher of letters 40-44 (a control test is in docs/LETTER39.md).
- The NAF 6638 cipher blocks encipher the clear text of pp. 29-34 of that copy (alignment against word-shuffled
  controls: z = -23 for the short block, z = -280 for the long one).

Not claimed:

- **Letter 39 is not solved.** The reading is partial. Of the 405 signs, 36 are left unread; lines 1-3 and line 20
  are mostly unread or weak. Of the 100 words that are read, 45 are graded high, 39 medium and 16 low, and the grades
  are judgment, not measurement. If the grades mean what they are intended to mean, about two thirds of the 100 words
  are right. There is no external text against which the reading could be verified.
- The key is not complete. 83 of the 159 values are of low confidence, some sign classes are mixtures that could
  not be separated by eye, and one sign of letter 39 (`Rr`) has no value at all.
- The transcriptions contain errors. Two independent transcriptions of letter 39 agree on 84% of the signs (89% if
  the second reader's marked alternatives are counted).
- No claim of priority is made beyond the statement in [docs/LITERATURE.md](docs/LITERATURE.md), which lists what
  was checked and what could not be checked (in particular Serrão 1969, which was not available).

## How to check it

Requirements: Python 3.9 or later; no other packages.

```
python code/reproduce.py
```

runs every step (15 to 30 minutes) and prints each figure quoted in this repository next to the value it has just
recomputed. `python code/reproduce.py --check` compares without recomputing. The individual scripts are described
in [code/README.md](code/README.md). The table of the last run is in
[results/reproduce_summary.txt](results/reproduce_summary.txt).

To check the transcription and the key by eye:

- BnF fr. 3151 on Gallica: <https://gallica.bnf.fr/ark:/12148/btv1b9059865k>. The viewer shows openings: folio N
  recto is the right-hand page of view N+1, folio N verso is the left-hand page of view N+2. Letter 39 is fo. 71r
  (view 72); the decipher sheets are fo. 74r (view 75) and fo. 85r-v (views 86-87).
- Each transcription file in data/ states its folio and view, and has one text line per manuscript line. For
  letter 39, read view 72 (right-hand page) against
  [data/fr3151/cipher/39_f71r.txt](data/fr3151/cipher/39_f71r.txt).
- The alignments from which every key value was counted are in results/align_*.txt (sign=value, sign by sign).

## Contents

| path | what |
|---|---|
| [docs/KEY.md](docs/KEY.md) | the key: every sign, its value, the evidence for it |
| [docs/SYMBOLS.md](docs/SYMBOLS.md) | the sign labels used in the transcriptions, with descriptions |
| [docs/LETTER39.md](docs/LETTER39.md) | letter 39: transcription, machine decode, reading with a grade per word, open points |
| [docs/NAF6638.md](docs/NAF6638.md) | the cipher blocks of February 1559 and their decipherment in the copy |
| [docs/METHOD.md](docs/METHOD.md) | how the key was built and how the decoder was tested |
| [docs/LITERATURE.md](docs/LITERATURE.md) | sources, earlier work, and what was and was not checked |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | history of the reading and of this release |
| [data/](data/README.md) | transcriptions, plaintexts, key files, language-model corpus |
| [code/](code/README.md) | the scripts |
| results/ | output of the scripts (alignments, key, test results) |

No manuscript images are included. The manuscripts can be viewed on Gallica at the addresses given above and in
[docs/LITERATURE.md](docs/LITERATURE.md).

## Sources and credits

- The manuscripts: Bibliothèque nationale de France, Département des manuscrits, Français 3151 and NAF 6638,
  consulted through Gallica (gallica.bnf.fr). Folio numbers and letter numbers follow the library's catalogue.
- Edmond Falgairolle, "Le chevalier de Seure, ambassadeur de France en Portugal au XVIe siècle", *Mémoires de
  l'Académie de Nîmes* XVIII (1895), pp. 49-85: prints Seure's letters of 1559 from the St Petersburg
  manuscript, including the text discussed in docs/NAF6638.md.
- Edmond Falgairolle, *Jean Nicot, ambassadeur de France en Portugal au XVIe siècle: sa correspondance diplomatique
  inédite* (Paris, 1897): the scanned text of this edition (Internet Archive) is the main corpus of the language
  model.
- Daniel Bourdeau's open catalogue of unsolved historical ciphers (dbourdeau.github.io/cyphersolver), where these
  letters are listed as open; it is what drew attention to them.
- The other works consulted are listed in docs/LITERATURE.md.

## Licence

Code under the MIT licence; text, transcriptions and data under CC BY 4.0. The scanned text of the 1897 book in
data/lm/ is third-party material and is **not** covered by either licence; see [LICENSE.md](LICENSE.md).
