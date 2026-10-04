# Changelog

## Release prepared 2026-10-04

Packaging of the working material: data files given uniform headers and formats, the scripts rewritten into the
small set in code/, all figures recomputed from the release folder (`python code/reproduce.py`).

Figures in the documentation that differ from the working notes, because the recomputed value differs or because
the note was imprecise:

- **Held-out word classes.** Four cells of the class table differ by one word (S1 stable 51/59, working notes
  51/58; S2 stable 21/32, notes 21/33; S1 unstable 17/28, notes 17/29; S2 unstable 3/12, notes 3/11), and the
  character accuracy of copy 41 C at LM weight 0.5 is 0.558 (notes 0.556; mean 0.583 against 0.582). Totals and the
  figures at weight 0.4 are unchanged. Cause: in the working runs the language model was trained on a plaintext
  file that still contained two comment lines; the release strips them. The class precisions quoted with each word
  of letter 39 changed accordingly (0.88 to 0.86, 0.64 to 0.66, 0.59 to 0.61, 0.27 to 0.25).
- **Machine decode of letter 39 at LM weight 0.4.** For the same reason the unread stretch of line 2 now decodes
  as "uerts pays il lendeur" (working notes: "uort sans parlendeur"). Nothing else in the three decodes changed.
- **Sign `14`**: null in 10 of 12 aligned occurrences (the notes had 7 of 8, from an earlier count).
- **Sign `A` in NAF 6638 N. 5**: the whole word "pour" in 11 of 21 occurrences; the "16 of 21" of the notes also
  counts partial alignments (po, pou).
- **Unread signs of letter 39**: 36 in four places (the notes said "about 35" in three spans and did not count
  the single sign L08.17).
- **Expected number of right words under the grades**: 66.5 of 100 (the notes said "about 67").
- **Falgairolle's "douze / onze"**: the +4.4 of the notes is the combined variant "mille ou douze cens" against "mil
  ou onze cens"; douze against onze alone is +2.2.
- **Sign counts**: early estimates in the notes (about 10,000 signs in fr. 3151, about 480 to 550 in letter 39,
  about 250 and 4,200 in NAF 6638) are replaced by counts of the transcriptions: 8,361 + 405, 264, 4,284 (4,261
  after joining).

## History of the reading of letter 39

**2026-10-03, first stage.** Key from letter 40 and the first block of letter 44 (about 2,200 aligned signs).
Transcription by one reader. Result: the gist only (Seure wants to leave; two years; the peace), with most of
lines 1-10 and 18-20 unread.

**2026-10-04, second stage.** Key from all known plaintext (letters 40, 41, 43, 44; 8,361 signs). Second,
independent transcription of letter 39; 17 signs changed after comparison. Confidence classes measured on
held-out block C. Changes to the reading:

- Line 1: "dont vous ..." became "dont noz".
- Lines 2-3: "[retraite des gens?]" became "a retraite des [musulmans?]" (low).
- Lines 4-6, until then unread, became "qu'ilz [disent?] verité, que la [ch?]ose sera aultrement, et ne l'aye [...]
  quoy qu'il en soit" (medium and low; "qu'il en soit" high).
- Lines 7-8: "[me sera ...] ... entendre la ... [apparence]" became "ce me sera plaisir d'en entendre la
  resolu[ti]on, car [.] commence" (medium and low). "apparence" was withdrawn.
- Line 9: "on [s'a/a] approcher du temps" became "on a aprocher du temps" (same sense).
- Lines 10-11: "deux ans avons tenu icy la ..." became "ses deux ans y avons tenu icy la paix".
- Line 12: the machine's "la nature helene" became "la paix [pour] [faict]e" (medium to low).
- Line 13: "[sera?] qui [f]aisoit encores" became "sera, qui m'y faisoit encores".
- Lines 15-16: a non-word became "icy gueres", and "longuement [mais?]" became "longuement, et a pis aller".
- Line 17: "[aller?] ne veux" became "aller n'y veux".
- Lines 18-19: "je suis en [...] [j'ay eu?] tout plein de" became "je suis en necessité, et ay eu tout plein de".
  "necessité" had been tested and rejected at the first stage; with the fuller key it is the decoder's own choice.
- Line 20: "[ce qu'il y]" became "[d]ettes? ces et de [...] ce qui [con...]" (low). "dettes" had been rejected at the
  first stage and is now only a conditional possibility.

**2026-10-04, third stage: values from NAF 6638.** `mt` = au, `A` = pour, `P` = que, `V` = h or faict; `t` = m
confirmed (never c); `4b`, `14`, `13`, `12` confirmed. Changes to the reading:

- Line 5: "aultrement" became "autrement" (spelling only).
- Line 16: "a pis aller" became "au pis aller" (same sense; now the best-scoring form).
- Line 13: "encores" downgraded from medium to low-medium; the sign in question was checked on the image and is
  a `t`.
- Line 12: basis corrected (`A` = pour is the sign's main value); grade unchanged.
- Line 17: "veux que" is now also given by the decoder at LM weight 0.4.
- No change to "musulmans", "resolution", "necessité", "dettes" (their scores move by 0.2 or less). Lines 1-3, the
  gap in line 10 and line 20 remain unread. Held-out accuracy unchanged.
