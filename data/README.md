# Data

All files are UTF-8 text with Unix line ends. In every file a line that begins with `%` is a comment. (`#` cannot
be the comment mark, because `#`, `#1`, `#b`, `##` and others are sign labels.)

## Finding the manuscript pages

| manuscript | Gallica | how views relate to folios or pages |
|---|---|---|
| BnF, Français 3151 | <https://gallica.bnf.fr/ark:/12148/btv1b9059865k> | the viewer shows openings: fo. N recto is the right-hand page of view N+1; fo. N verso is the left-hand page of view N+2 |
| BnF, NAF 6638 | <https://gallica.bnf.fr/ark:/12148/btv1b525105423> | p. N of the copy is view N+12 (p. 29 = f41; pp. 35-43 = f47-f55) |

Every transcription file names its folio or page and its view in the header.

## fr3151/cipher/: transcriptions of the cipher

One text line per manuscript line; sign labels separated by spaces ([docs/SYMBOLS.md](../docs/SYMBOLS.md)). A
comment `% Lnn` at the end of a line gives its number within the cipher block. In the files of letter 39 the
comments also record doubts and changes.

| file | letter, folio | view | signs | plaintext |
|---|---|---|---|---|
| 39_f71r.txt | 39, fo. 71r: final transcription | 72 | 405 | none known |
| 39_f71r_reader1.txt | the same, first reader before comparison | 72 | 405 | |
| 39_f71r_reader2.txt | the same, independent second reader (`?` = uncertain, `a?\|b` = alternatives) | 72 | 402 | |
| 39_f71r_alt.txt | the same, variant with two doubtful places read the other way | 72 | 404 | |
| 39_f71r_reader1_early.txt | the same, earliest transcription (used only by code/keyfit_control.py) | 72 | | |
| 40_f73r.txt, 40_f73v.txt | 40, fo. 73r and 73v, main cipher block | 74, 75 | 456 + 626 | plain/40_decipher_f74r.txt |
| 41_f76r.txt, 41_f76v.txt | 41, block A | 77, 78 | 357 + 726 | 12dec1558_text.tsv, segment A |
| 41_f77r_B.txt | 41, block B | 78 | 427 | segment B |
| 41_f77r_C.txt | 41, block C (postscript) | 78 | 373 | segment C |
| 43_f80r.txt, 43_f80v.txt, 43_f81r.txt, 43_f81v.txt | 43, main text | 81, 82, 82, 83 | 904 + 825 + 842 + 569 | segments CLEAR1 + A + CLEAR2 + B |
| 43_f82r_PS.txt | 43, postscript | 83 | 382 | segment C |
| 44_f84r.txt, 44_f84v.txt | 44, block A | 85, 86 | 353 + 791 | segment A |
| 44_f86r_B.txt | 44, block B | 87 | 428 | segment B |
| 44_f86r_C.txt | 44, block C (postscript) | 87 | 302 | segment C |

Not transcribed: the short postscript cipher at the foot of fo. 73v (letter 40).

The transcriptions were made in several passes, not all with the same care. Letter 40 and letter 39 were worked
over most; large parts of letters 41, 43 and 44 were transcribed in a single pass. The files give the final label
sequence; the line-by-line reading notes of the working files were not carried over, except for letter 39.

## fr3151/plain/: the plaintexts

Lower case, no punctuation, apostrophes dropped, abbreviations expanded. u/v and i/j are written as in modern
spelling in these files; the scripts normalise j to i, v to u, w to u and k to c before use. `GAP` marks a stretch
of a decipher sheet that could not be read.

- **40_decipher_f74r.txt**: the contemporary decipherment of the main cipher block of letter 40, from fo. 74r,
  line by line.
- **40_decipher_f74r_PS.txt**: the decipherment of the postscript cipher of letter 40 (same sheet). Not used by the
  scripts.
- **12dec1558_text.tsv**: the whole letter of 12 December 1558 from no. 44, as segments `TAG<TAB>text`: the clear
  parts (CLEAR0 to CLEAR3) from the letter, the cipher parts A, B, C from the decipher sheet fo. 85r-v. Letters 41
  and 43 encipher the same text.

## fr3151/letter39_reading.tsv, letter39_tests.tsv

The proposed reading of letter 39 as a table of spans (first sign, last sign, status, reading, number of words,
grade), covering all 405 signs; and the list of competing readings that were scored against each other. Both are
explained in [docs/LETTER39.md](../docs/LETTER39.md) and read by code/decode39.py and code/score_reading.py.

## sets.tsv

Which cipher files are aligned with which plaintext, and with what role: `train` (counted when the key is built)
or `heldout` (block C in its three copies; aligned afterwards, never counted). Columns are described in the
header.

## key/

| file | what |
|---|---|
| key.csv, key.json | the key: per sign its value, the count on the value, the count of all aligned occurrences, the confidence class, occurrences per letter, the full distribution, and (for nine signs) the revised value. Written by `python code/build_key.py --publish`. |
| revised_values.tsv | the values revised or confirmed from NAF 6638, with the reason |
| naf6638_n5_values.tsv | the units aligned with those nine signs in the NAF 6638 N. 5 block |
| sign_descriptions.tsv | verbal descriptions of the sign shapes |
| seed_previous_pass.tsv | starting key of build_key.py (the key of the previous pass of the same procedure) |
| seed_letter40.tsv | key from letter 40 alone, made at the first stage; alternative starting key, and the fixed key of two tests |
| letter40_first_alignment.txt | the alignment from which seed_letter40.tsv was counted (used by code/keyfit_control.py) |

Opening key.csv in a spreadsheet program: import it as text. Several sign labels (`=`, `+`, `+f`, `=o`, `1`, `12`)
would otherwise be taken for formulas or numbers. In the distribution column, `_` is null and `[word]` a whole
word.

## naf6638/

- **cipher/N4_p29.txt**: the cipher block of piece N. 4 (264 signs).
- **cipher/N5_p35-36.txt, N5_p37-39.txt, N5_p40-43.txt**: the cipher block of piece N. 5 (970 + 1,450 + 1,864 =
  4,284 signs as written). Comment lines `% p. NN` start a page. `label?` = uncertain, `a?|b` = alternatives. The
  headers list the conventions by which the copyist's regularised shapes were given labels; these differ from file
  to file for a few provisional labels (NEW1, NEW2, ...), which the scripts keep apart.
- **plain/copy_p29-34.txt**: the clear text of the copy from the middle of p. 29 to the end of p. 34, line by line,
  in the copy's spelling. `=` marks the copyist's hyphen; `*` his reference mark; the lines `% FN31:` give his
  footnote on p. 31.
- **plain/copy_p29_after_N4_first_reading.txt**, **plain/copy_p28-29_before_N4.txt**: the text just after and
  just before the N. 4 block, as first read; kept because the N. 4 test was made with them.

## lm/

**nicot_falgairolle_1897_ocr.txt**: the scanned text (raw OCR, unedited) of Edmond Falgairolle, *Jean Nicot,
ambassadeur de France en Portugal au XVIe siècle: sa correspondance diplomatique inédite* (Paris, 1897), as
distributed by the Internet Archive (identifier jeannicotambassa00nico). It is used only to train the character
language model. The book was published in 1897 and is, as far as we can tell, in the public domain; the OCR text
is included so that the results can be reproduced exactly (see LICENSE.md). It contains the editor's introduction and notes in modern French as well as the
16th-century letters, and a great many OCR errors.
