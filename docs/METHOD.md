# Method

How the key was recovered, how the decoder works, and how both were tested. Every figure here is recomputed by
`python code/reproduce.py` ([results/reproduce_summary.txt](../results/reproduce_summary.txt)).

## 1. Material

BnF ms. fr. 3151 contains five letters of Seure with cipher, and two contemporary decipher sheets:

| no. | fo. | letter | cipher | plaintext available |
|---|---|---|---|---|
| 39 | 71r-v | to de Fresne, 12 Dec 1558 | one block, 405 signs | none |
| 40 | 73r-v | to Henri II, 27 Dec 1558 | main block, 1,082 signs (a short postscript block is not transcribed) | decipher sheet, fo. 74r |
| 41 | 76r-77r | to Henri II, 12 Dec 1558 (copy) | blocks A, B, C: 1,883 signs | the text of no. 44 |
| 43 | 80r-82r | to Henri II, 12 Dec 1558 (copy, almost wholly in cipher) | 3,522 signs | the text of no. 44, clear parts included |
| 44 | 84r-86r | to Henri II, 12 Dec 1558 | blocks A, B, C: 1,874 signs | decipher sheet, fo. 85r-v |

No. 42 (fo. 78) is a letter of another writer and has nothing to do with the cipher. The library catalogue and
earlier descriptions pair the letters differently (41 as a duplicate of 40); the opening words and the date line of
no. 41 show that it is the letter of 12 December ([LITERATURE.md](LITERATURE.md)).

The letter of 12 December therefore exists in three separately enciphered copies. They are not sign-for-sign
identical: the clerk chose among the homophones afresh each time, and no. 43 enciphers passages that the other two
leave in clear.

Transcription was done from the Gallica images, line by line, into ASCII labels ([SYMBOLS.md](SYMBOLS.md)). The
plaintexts were transcribed from the decipher sheets and, for the clear parts of no. 44, from the letter itself
([data/README.md](../data/README.md)).

## 2. Alignment and key

A key gives each sign one unit: a letter, a group of two to four letters, a whole word, or null. Given a key, the
aligner ([code/aligner.py](../code/aligner.py)) finds the cheapest way to lay the cipher signs along the plaintext
letters, in order:

| move | cost |
|---|---|
| the sign takes exactly its key unit | 0 |
| the sign takes another unit of 1 to 3 letters within a word | 2.0, plus 0.4 per letter beyond the first |
| the sign takes nothing | 0.2 if its key value is null; 0.4 inside an unread gap of the decipher sheet; otherwise 2.2 |
| a plaintext letter has no sign | 2.0 (0.6 or 0 at the two ends, where cipher and plaintext need not begin and end together; set per text in data/sets.tsv) |
| the sign takes a whole word | 0 if that word is its key value; otherwise 3.5 |
| an unreadable sign (`?`) | 1.0 for one letter, plus 0.3 per further letter |

The key is then re-estimated: each sign gets the unit it was aligned with most often. Alignment and re-estimation
are repeated until no sign changes ([code/build_key.py](../code/build_key.py)). Only the training sets count; the
three copies of block C are aligned with the finished key but never contribute to it.

The procedure needs a starting key, and the result depends on it to a small degree:

- Started from an empty key it fails: with every sign equally wrong the alignment has nothing to hold on to (in
  the working runs the cost stayed above 10,000).
- The first key was made from letter 40 alone, with a probabilistic aligner that needs no starting key (an
  expectation-maximisation over sign-to-letter correspondences; exploratory code, not part of this release), and
  then refined by the iteration described here. The other letters were added in stages, each pass starting from
  the key of the pass before.
- The default seed of this release is the key of the last-but-one pass
  ([data/key/seed_previous_pass.tsv](../data/key/seed_previous_pass.tsv)). From it the procedure converges in two
  iterations (training cost 5522.5) to the documented key.
- Started instead from the letter-40 key ([data/key/seed_letter40.tsv](../data/key/seed_letter40.tsv)), it
  converges in three iterations to a slightly *lower* cost (5512.2) and to a key that differs in 10 of 159 signs,
  which carry 214 of the 8,361 aligned occurrences (2.6%). Nine of the ten are low-confidence signs; the tenth is
  `a` (null 12 of 19 in the documented key, b 8 of 19 in the other). The documented key is thus a fixed point of the
  procedure, not a proven optimum. It was kept because every later figure was computed with it. The differences
  are listed in [results/seed_letter40/build_log.txt](../results/seed_letter40/build_log.txt).

Result: 156 signs have a value from the training sets; with block C aligned afterwards the table has 159 signs
(46 high, 30 medium, 83 low confidence; [KEY.md](KEY.md)).

## 3. Decoder

For a cipher text without plaintext ([code/decoder.py](../code/decoder.py)):

- **Key model.** The alignment counts are turned into probabilities P(sign | unit), smoothed. A sign with fewer
  than 8 aligned occurrences may also stand for any single letter with a small probability (0.003); a sign never
  seen with plaintext may stand for any letter or null (0.02 each).
- **Language model.** A character 7-gram model (Witten-Bell smoothing) over the letters a-z and the space, trained
  on the scanned text of Falgairolle's edition of Jean Nicot's correspondence (1897; Nicot was Seure's successor in
  Lisbon), plus the plaintexts of letters 40 and 44. The scanned text is raw OCR and contains the editor's
  modern-French introduction and notes as well as the 16th-century letters.
- **Search.** A beam search over the signs, left to right, choosing for each sign a unit and whether a word ends
  after it. Score = sum of log P(sign | unit) + w × log P(text), with LM weight w = 0.3, 0.4 or 0.5 and a fixed
  penalty for word signs. Beam width 300.

The decoder's output is a string of words, many of them wrong. It is a tool for proposing readings, not a
reading.

## 4. How good is it? The held-out test

Block C, the postscript of the letter of 12 December ("Ilz debvoient huit cens mil escuz aux foires de Medina
..."), has a contemporary decipherment (fo. 85v) and exists in three copies: 41 fo. 77r (373 signs), 43 fo. 82r
(382 signs), 44 fo. 86r (302 signs). It was excluded from key building and from the language model, and each copy
was then decoded blind ([code/heldout.py](../code/heldout.py), [results/heldout.txt](../results/heldout.txt)).

**Character accuracy** (1 - edit distance / length of the true text, 441 letters):

| copy | LM weight 0.3 | 0.4 | 0.5 |
|---|---|---|---|
| 44 C | 0.508 | 0.508 | 0.497 |
| 41 C | 0.551 | 0.553 | 0.558 |
| 43 PS | 0.705 | 0.705 | 0.694 |
| mean | 0.588 | 0.589 | 0.583 |

This is the honest measure of what the key and decoder achieve on unseen text of the same kind: somewhat more
than half of the letters. According to the working notes, the key of the previous pass, built before the last
transcription files were added, gave much the same accuracy; that comparison is not regenerated here. The limit
seems to be the noise of sign reading together with the ambiguity built into the cipher, not the amount of data.

**Which words can be trusted.** Each decoded word of two or more letters is put into a class by two properties
that can be computed without knowing the answer:

- *Support*: the share of its letters that come from a "strong" sign (at least 6 aligned occurrences, at least 60%
  of them on one value) decoded to that value. S1: 0.99 or more; S2: 0.75 to 0.99; S3: below 0.75.
- *Stability*: the decoder gives the same word over the same signs at all three LM weights.

On block C a word counts as right if it occurs in the true text within 25 characters of its expected position:

| class | right / words | precision |
|---|---|---|
| S1 stable | 51 / 59 | 0.86 |
| S2 stable | 21 / 32 | 0.66 |
| S3 stable | 37 / 64 | 0.58 |
| S1 unstable | 17 / 28 | 0.61 |
| S2 unstable | 3 / 12 | 0.25 |
| S3 unstable | 19 / 76 | 0.25 |
| all stable | 109 / 155 | 0.70 |
| all unstable | 39 / 116 | 0.34 |
| all | 148 / 271 | 0.55 |

So a well-supported word on which the decoder does not waver is right about six times in seven, and an
ill-supported, unstable one about once in four. These classes are what the confidence grades of the letter-39
reading start from ([LETTER39.md](LETTER39.md)). The numbers are small (three copies of one text of 441 letters),
and the criterion is lenient for short words.

**With the revised values from NAF 6638** ([KEY.md](KEY.md)) the mean character accuracy at LM weight 0.4 is
0.593, 0.595 or 0.587, depending on how the revision is applied (majority value only; the same with the two
alignment artefacts corrected; all aligned units). Against 0.589 that is no measurable change: the signs
concerned are rare in block C.

**A note on exact reproduction.** The class table above differs in four cells by one word from the table in the
working notes of 2026-10-04 (S1 stable 51/58, S2 stable 21/33, S1 unstable 17/29, S2 unstable 3/11), and the
accuracy of 41 C at weight 0.5 differs by 0.002. The cause was found: in the working runs the language model had
been trained on a plaintext file that still included two comment lines of file header. The figures given here are
those of the released code and data.

## 5. Does the key fit letter 39 at all?

Before reading letter 39 it was checked that it is in the same cipher
([code/keyfit_control.py](../code/keyfit_control.py)). With the key from letter 40 alone, the decoder score of the
first 350 signs was compared with two controls: the same signs in shuffled order, and the right order decoded with
the key's values permuted among the signs (six runs each). Letter 44, known to be in the cipher of letter 40,
serves as the positive example:

| text | real | shuffled order | permuted key |
|---|---|---|---|
| letter 44, fo. 84r | -1174.5 | -1220.1 ± 5.3 (z = 8.6) | -1469.3 ± 26.2 (z = 11.3) |
| letter 39, fo. 71r | -1124.3 | -1212.2 ± 6.0 (z = 14.8) | -1488.4 ± 30.5 (z = 11.9) |

Letter 39 behaves like letter 44. This test was made at the first stage of the work and is reproduced with the
inputs it had then: the letter-40 key, the earliest transcription of letter 39, and a language model without
spaces trained on the Nicot text alone.

## 6. Reading letter 39

Three things are combined ([LETTER39.md](LETTER39.md)):

1. the machine decode at three LM weights, with the class of each word;
2. for each doubtful span, a direct comparison of candidate readings ([code/score_reading.py](../code/score_reading.py)):
   score = log P(signs | reading), for the best way of dividing the reading among the signs, + 0.4 × log P(reading)
   under the language model;
3. judgment: sense, syntax, and a look at the image where two readers disagreed.

The third component is not measured. The grades H, M, L attached to each word are the editor's estimate, anchored
on the class precisions above but not themselves calibrated. That is the main reason why the reading is offered as
partial and provisional.

## 7. Limits of the method

- **One transcriber per page, mostly.** Only letter 39 was transcribed twice. The two transcriptions agree on
  84% of signs before reconciliation; the other letters were not double-checked in this way, and their errors are
  inside the key counts.
- **The alignment is itself a model.** Where the decipher sheet abbreviates, omits or rewords, or where the clerk
  made an enciphering mistake, the aligner forces signs onto wrong units. Two such systematic artefacts were found
  only because NAF 6638 exposed them (`mt`, `A`); there may be more.
- **The language model is small and impure** (about 600,000 characters of raw OCR including modern French).
- **Held-out text is of the same letter** as part of the training text. For a letter on another subject, to
  another addressee, the class precisions are an upper bound.
- **No clean tuning set.** The alignment costs and the class thresholds were set by hand in the course of the
  work, with the known plaintext in view. The decoder settings (smoothing, order and weight of the language model)
  were compared on two of the three copies of block C; accuracy was flat around the settings used, but to that
  extent the held-out figures are not untouched.
