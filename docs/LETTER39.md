# Letter 39: Seure to de Fresne, Lisbon, 12 December 1558

Source: BnF ms. fr. 3151, no. 39, fo. 71r (Gallica <https://gallica.bnf.fr/ark:/12148/btv1b9059865k>, view 72,
right-hand page). The letter is in clear except for one cipher block of 20 lines (405 signs). It ends on fo. 71v
with "De Lisbonne le xiie jour de decembre 1558". No contemporary decipherment of this letter was found in the
volume, and none is known to us from elsewhere.

## The reading

`[...]` marks a gap, `[word?]` a weak reading, and square brackets inside a word mark letters that the signs do not
support. Punctuation, word division and apostrophes are editorial.

Period spelling:

> [clear: ... non la facon] dont noz [...] a retraite des [musulmans?] [...] qu'ilz [disent?] verité, que la [ch?]ose
> sera autrement, et ne l'aye [...] quoy qu'il en soit. Ce me sera plaisir d'en entendre la resolu[ti]on, car [.]
> commence on a aprocher du temps que [...] ses deux ans. Y avons tenu icy la paix [pour faicte?]; ie ne scay ce
> qu'il en sera, qui m'y [f]aisoit encores avoir plus de doute. Ie ne veulx plus demeurer icy gueres longuement, et
> au pis aller n'y veux que achever mes deux ans. Ie suis en necessité, et ay eu tout plein de [dettes?], ces et de
> [...] ce qui [con...] [clear text resumes]

English:

> ... of which our [...] the withdrawal of the [Muslims?] [...], if they are telling the truth, that the [matter] will
> turn out otherwise, and I have not [...] it; whatever the case, I shall be glad to learn the decision on it, for we
> are beginning to approach the time when [...] two years. Here we have taken the peace as concluded; I do not know
> what will come of it, which made me doubt all the more. I no longer wish to stay here much longer, and at worst I
> want only to complete my two years here. I am in want, and have had a great many [debts?] ... and of ... which ...

Modern French:

> ... dont nos [...] la retraite des [musulmans ?] [...], s'ils disent vrai, que la [chose] tournera autrement, et je
> ne l'ai [...] ; quoi qu'il en soit, je serai heureux d'en apprendre la décision, car on commence à approcher du
> moment où [...] deux ans. Ici, nous avons tenu la paix pour faite ; je ne sais ce qu'il en sera, ce qui me faisait
> douter encore davantage. Je ne veux plus guère demeurer ici longtemps, et au pis aller je ne veux qu'y achever mes
> deux ans. Je suis dans le besoin, et j'ai eu quantité de [dettes ?] ... et de ... ce qui ...

The renderings smooth over the gaps and are no more certain than the word-by-word reading in section 3.

Background, not evidence for the reading:

- In December 1558 the peace talks between France and Spain, begun at Cercamp in the autumn, were under way; they
  led to the treaty of Cateau-Cambrésis in April 1559. A remark from Lisbon that "here we have taken the peace as
  made" fits that moment.
- Seure's wish to leave Portugal and his want of money agree with his clear letters of January and February 1559,
  printed by Falgairolle (1895). He was replaced by Jean Nicot in 1559.

## How far to trust it

This is a partial reading.

- Lines 11-19 are read nearly in full. Lines 4-10 are read in part (line 10 has a gap of 12 signs). Lines 1-3 and
  line 20 are mostly unread or weak.
- 100 words are read, each with a grade: 45 high, 39 medium, 16 low. 36 signs in four places are left unread.
- The grades are judgment. They combine the decoder's class for the word (table below), the sign-by-sign key
  evidence and the comparison of competing readings, and they were not calibrated separately. They are meant to
  correspond roughly to a chance of being right of 0.85 (high), 0.6 (medium) and 0.3 (low). On that footing about
  66 of the 100 words are right, and probably fewer for the reasons below.
- There is nothing to check the reading against. It will stand or fall with an independent re-reading of the
  signs, with further known plaintext, or with the discovery of a decipherment.

The class of a word comes from a test on text whose plaintext is known and was withheld: three copies of a
1,057-sign postscript, decoded blind ([METHOD.md](METHOD.md), section 4). Each decoded word falls into a class by
its support (S1 best, S3 worst) and by whether the decoder gives it at all three language-model weights (stable):

| class | right / words in the test | precision |
|---|---|---|
| S1 stable | 51 / 59 | 0.86 |
| S2 stable | 21 / 32 | 0.66 |
| S3 stable | 37 / 64 | 0.58 |
| S1 unstable | 17 / 28 | 0.61 |
| S2 unstable | 3 / 12 | 0.25 |
| S3 unstable | 19 / 76 | 0.25 |

For letter 39 these precisions are an upper bound:

- Letter 39 has its own transcription noise: two transcriptions agreed on 84-89% of its signs (section 1).
- One of its signs, `Rr`, has no key value.
- Its subject is less well covered by the language model than the test text, which comes from the same letter as
  part of the model's training text.

The letter is in the same cipher as the others. Under the letter-40 key its decoder score stands as far above
shuffled and permuted controls as that of letter 44, which is known to be in this cipher (z = 14.8 and 11.9; table
in [METHOD.md](METHOD.md), section 5).

Not used as evidence: Seure's clear letters of January and February 1559, printed by Falgairolle, played no part
in the decoding, in the language model or in the tests. Their wording ("ny puis gueres demeurer") resembles lines
14-16 here. That is consistent with the reading and does not prove it.

## 1. Transcription

File: [data/fr3151/cipher/39_f71r.txt](../data/fr3151/cipher/39_f71r.txt). Sign labels are explained in
[SYMBOLS.md](SYMBOLS.md); the page is view 72 (right-hand page) of the Gallica copy. Line 1 starts
after the clear words "... toutesfoys le dommaige a estimee non la facon". Clear text resumes after line 20.

```
L01  2 * #p 14 = ooo 13 f 6 7
L02  n 3 #1 S oo B C = # lo E mm Q R 3 o +f Nf Hr ff ii Qb h
L03  o sl M * Aq 1 R 12 z ### f + W ^ Cz +d ### o Cs
L04  mm # Q B vl n 6 J z 3s = Aq 3 ff +f Rr Qb 9 P cl Nf
L05  1 #1 # 3s z 1 h #b mt ooo +f 3s m ff f Aq Zb mm 9 vl
L06  o oo 3s # J ff 3 1 To ^ 6 oo N +d 3s = W #p II Qb 7
L07  s ts ff z 1 6 #b 8p vl o # 6 +f R f 3s xx ooo ff f * 7
L08  +f 3s cl Nf Hr ff W #p v d +f sl 8 xx + #b 6 C ss m
L09  ff mm s #1 f # o 100 #b EE Hr #p p U 9 +f 6 ^ ooo 3s ts
L10  g z P c Nf ### C #b oo ff #b +f th V d 3s z ff W R ^
L11  x o f # C Nf 3 #1 mm W Aq 1 = d sl + Cx +d o 8p
L12  #b Lc m A To Tr V 3s ## ff f 1 W + o oo s N +d 3s =
L13  # ff 8 Nf N m Cx 3 #b sl z 6 cc Qb 3s = t #p +f 1 W
L14  o ^ #1 # Hr 8p vl 3 # R * 6 d a ooo 3s ## ff mm 1 3
L15  ff 3 +d m EE cl d W R m 3s d Hr 1 h # p Cx x ^
L16  sl ff +f 1 Wl cl 6 mm Cx d 3s ts ff f Q Rq mt EE cc z
L17  o +d E h = Cx ^ ff ^ x P o + th 3s d 1 +f ### 3s Wl
L18  R ii 3 x o f # Rl ff z ^ ## # 3s = Ak mm 9 s Wl sl oo
L19  ff 4b o Cx 1 ^ 12 Aq #1 14 d Qb 13 EE +d ff 2 cc f R 7
L20  3s Qb 3s z 100 + J Zb R Tr J 12 ff 12 Cz Cx s N Tr x
```

**Two-reader check** (`python code/compare_readers.py`,
[results/letter39_readers.txt](../results/letter39_readers.txt)). The block was transcribed a second time,
independently, by shape alone and without sight of the first transcription, of the key or of any decoding
([39_f71r_reader2.txt](../data/fr3151/cipher/39_f71r_reader2.txt)).

- First transcription against the second: the same label on 341 of 405 signs (0.842); 359 (0.886) if the
  alternatives that the second reader marked are counted. So a single reader gets roughly one sign in eight to one
  in ten wrong.
- Every position on which the two differed was looked at again on the image. This changed 17 signs of the first
  transcription and gave the final one (in the file comments: "v4"; the first transcription,
  [39_f71r_reader1.txt](../data/fr3151/cipher/39_f71r_reader1.txt), is "v3"). 13 changes went to the second
  reader's label, 2 to one of the second reader's alternatives, and 2 to a third reading (`+` to `+d`, `m` to `mt`).
- Final transcription against the second reader: 353 of 405 (0.872); 369 (0.911) with alternatives.
- The comments in the transcription file record every change and every remaining doubt. The main ones: L02 signs
  20-22; L04 sign 2; L06 signs 4, 13, 18; L07 sign 11; L08 sign 8 (`v` or `vl`) and sign 12; L13 sign 7; L16 sign
  16; L20 sign 0 (a squiggle on the descender of an `ff` of line 19, possibly not a sign). Signs are counted from 0
  within the line.
- Many disagreements do not affect the value: `=` and `xx` are both n, `9` and `1` both e, `cl` and `vl` both l,
  `t` and `ts` both m.
- A variant transcription with two of the doubtful places read the other way (L08 sign 8 = `vl`; L20 sign 0
  omitted) is in [39_f71r_alt.txt](../data/fr3151/cipher/39_f71r_alt.txt) and is used in section 3.

**Signs peculiar to this letter.** `Rr` (L04) has no known-plaintext occurrence anywhere; the decoder treats it as
unknown. The other signs that are rare or absent in letter 40 have values from letters 41, 43 and 44
([KEY.md](KEY.md)):

| sign | value | evidence (fr. 3151) | NAF 6638 N. 5 |
|---|---|---|---|
| `Lc` | i | 43/45 | |
| `Rq` | et | 8/10 | |
| `4b` | et | 8/10 | et 3 of 5 |
| `mt` | **au** (table: a 31/34) | the "a" is an alignment artefact, see KEY.md | au 7 of 11 |
| `14` | null | 10/12 | null 3 of 3 |
| `13` | null | 6/6 | null 1 of 1 |
| `Tr` | null | 40/49 | |
| `lo` | null | 7/13 (weak) | no usable data |

**Revised values.** The known plaintext of NAF 6638 ([NAF6638.md](NAF6638.md)) corrects four values and confirms
others; the readings below use them:

| sign | value used | evidence |
|---|---|---|
| `mt` | au | see above |
| `A` | pour (word or syllable) | N. 5: pour 11 of 21, or 16 of 21 with partial alignments. fr. 3151: "ur" 22/42, an alignment artefact |
| `P` | que | N. 5: 40 of 47. fr. 3151: q 33, que 17 of 83 |
| `V` | h (as in "ch") or faict | N. 5: faict 5 of 8. fr. 3151: h 9, faict 6 of 20 |
| `t` | m, not c | N. 5: m 17 of 25, c 0. fr. 3151: m 16, c 1 of 42 |

The revision does not raise the measured accuracy on the held-out text (0.589 against 0.587-0.595). The changes
it makes to the reading therefore rest on the sign evidence alone.

## 2. Machine decode

`python code/decode39.py` ([results/letter39_decode.txt](../results/letter39_decode.txt)): key as built from
fr. 3151, language model with word boundaries, beam 300. This is raw program output, kept as the record. It is
**not** the reading.

- **LM weight 0.3:** dont noz uorts gens il lendeur a retraite des m n c sul mans quilz des sent uerte que la liose
  sera aultrement et ne laye les euequoy quil en soit ce me sera plaisir de n en tendre la resolu rioncay commence
  on sait pro cher du temps que lamyayer h hue ses deux ans y auons tenu icy la paix urge ie ne scay ce quil en
  sera qui au guaisoit en mores auoir plus de doubte ie ne ueulx plus de meurer icy guieres longue men et apis
  aller ny ueux que acheuer mes deux ans ie suis en necessite et ay eu tout plein etes ces et de esg ce qui con
- **LM weight 0.4 (main):** dont noz uerts pays il lendeur a retraite des musul mans quilz des sent uerte que la
  liose sera aultrement et ne laye les euequoy quil en soit ce me sera plaisir de n en tendre laredo surin carne
  commence on sait pro cher du temps que a m payer h faue ses deux ans y auons tenu icy la paix he ie ne scay ce
  quil en sera qui mai soit encores auoir plus de doute ie ne ueulx plus de meurer icy gueres longue men et agis
  aller ny eu acheuer mes deux ans ie suis en necessite et ay eu tout plein ete ses et de esg ce qui con
- **LM weight 0.5:** dont noz uerts pays lendeur a retraite des musul mans quilz des sent uerte que la liose sera
  aultrement et ne laye les euequoy quil en soit cesse d aplaisir de n en tendre la resolucion luy ay commence on a
  pro cher du temps que a m payer haures deux ans y auons tenu par la paix he ie ne scay ce quil en sera qui mai
  soit encores auoir plus de doute ie ne ueulx plus de meurer icy gueres longue men et agis aller ny eu acheuer mes
  deux ans ie suis en necessite et a este toute plein ete ses et de ce qui

Of the 107 decoded words of two letters or more (weight 0.4), 35 are S1 stable, 15 S2 stable, 24 S3 stable, 8 S1
unstable, 7 S2 unstable, 18 S3 unstable. At the held-out precisions that would be 65 words right of 107 (0.61), as
an upper bound.

With the revised values (`python code/decode39.py --update n5orig --beam 400`,
[results/letter39_decode_n5orig.txt](../results/letter39_decode_n5orig.txt)) the decode changes in a few places:
"autrement" for "aultrement" at all three weights; "et au pis aller" at weight 0.3 (the non-word "auis" at 0.4 and
0.5); "ny ueux que acheuer" at 0.3 and 0.4; "en mores" for "encores" at 0.3 and 0.4.

Could the decoder simply be reciting its training text? The following phrases of the decode occur nowhere in the
language-model corpus: "pis aller", "pour faicte", "plein de", "gueres demeurer", "faisoit encores", "plus de
doute". "deux ans", "necessite" and "demeurer" occur only in the Nicot part of the corpus, not in Seure's own
letters.

## 3. Reading, word by word

Each entry gives:

- the **span**: line.sign to line.sign, signs counted from 0 within the line;
- the **signs**, then the **reading**;
- the **grade** (H, M, L, or between two): judgment, as explained above;
- the **decoder**: what the machine decode at weight 0.4 has there, its class and the held-out precision of that
  class;
- the **basis**: key values, and scores of competing readings where they were compared. Scores are
  log-probabilities (signs given the reading, plus 0.4 × language model); higher, i.e. less negative, is better. All
  scores are in [results/letter39_tests.txt](../results/letter39_tests.txt) (`python code/score_reading.py`).
  Scores are with the key as built unless "revised values" is said; where two figures are then given, as in
  "-33.2 / -31.9", they are for the two ways of applying the revision (`n5maj` / `n5orig`, see
  [code/README.md](../code/README.md)). Differences of one or two units between readings are not decisive.

"6 = r 11/205" means that 11 of the 205 aligned occurrences of sign `6` in the known plaintext have the value r.
The same list in machine-readable form: [data/fr3151/letter39_reading.tsv](../data/fr3151/letter39_reading.tsv).

### Lines 1-4

- **L01.0** `2`: null.
- **L01.1-5** `* #p 14 = ooo`: **dont**. Grade M. Decoder: dont, S2 stable, 0.66.
  - Basis: d o _ n t. It follows the clear words "... non la facon".
- **L01.6** `13`: null.
- **L01.7-L02.0** `f 6 7 n`: **noz**. Grade M. Decoder: noz, S3 stable, 0.58.
  - Basis: n o _ z. Scores: noz -26.8, uoz -30.0, nous -35.8.
- **L02.1-16** `3 #1 S oo B C = # lo E mm Q R 3 o +f`: **[unread]**. Decoder: "uerts pays il lendeur" (0.4), "uorts
  gens il lendeur" (0.3), "uerts pays lendeur" (0.5).
  - Basis: the first nine signs are a language-model fill; the three weights disagree (S3 unstable, 0.25). The last
    seven signs have well-attested values (le, n, null, de, u, a or null, r) and the decoder gives the letter string
    "lendeur" at all three weights (S1 stable), but no word or word division was recognised in it. L02 signs 20-22
    are among the doubtful transcriptions.
- **L02.17** `Nf`: **a**. Grade H. Decoder: a, S1 stable, 0.86.
- **L02.18-L03.5** `Hr ff ii Qb h o sl M * Aq 1`: **retraite**. Grade H. Decoder: retraite, S1 stable, 0.86.
  - Basis: r e _ t r a i _ _ t e.
- **L03.6-8** `R 12 z`: **des**. Grade H. Decoder: des, S1 stable, 0.86.
- **L03.9-L04.1** `### f + W ^ Cz +d ### o Cs mm #`: **[musulmans?]**. Grade L. Decoder: musul (S2 unstable, 0.25) +
  mans (S2 stable, 0.66).
  - Basis: m u _ s u _ l m a _ n s. This needs f = u (2/207) and `+` as a null.
  - Scores: "des musul" -64.8, against "des gens" -80.1, "des turcs" -79.6, "des soldatz" -88.8.
  - The word is rare in French of 1558. The string "musul" occurs once in the language-model corpus, in a modern
    editorial note. Treat it as a lead, not a reading.
- **L04.2** `Q`: null.
- **L04.3-5** `B vl n`: **qu'ilz**. Grade L-M. Decoder: quilz, S3 stable, 0.58.
  - Basis: B = qui is not the key value (B is s, 33/68).
- **L04.6-11** `6 J z 3s = Aq`: **d[..]sent** (disent?). Grade L. Decoder: des (S3 stable) sent (S1 stable).
  - Basis: scores "des sent" -57.2, "disent" -61.6 (needs J = i).
- **L04.12-17** `3 ff +f Rr Qb 9`: **verité**. Grade M. Decoder: uerte, S1 stable, 0.86.
  - Basis: u e r [Rr] t e. `Rr` has no key value; i is assumed.
- **L04.18-20** `P cl Nf`: **que la**. Grade H. Decoder: que (S3 stable) la (S1 stable).

### Lines 5-6

- **L05.0-3** `1 #1 # 3s`: **[.]ose** (chose?). Grade L. Decoder: liose, S3 stable.
  - Basis: the sense wants "chose", but `1` is e (170/199) and never ch; under the key the signs cannot give
    "chose" at all.
- **L05.4-7** `z 1 h #b`: **sera**. Grade H. Decoder: sera, S1 stable, 0.86.
- **L05.8-15** `mt ooo +f 3s m ff f Aq`: **autrement**. Grade M. Decoder: aultrement (S3 stable) with the key as
  built; autrement (S1 stable) with the revised values.
  - Basis: au-t-r-e-m-e-n-t with `mt` = au; `ooo` = t 124/140, never "lt". Scores with the revised values:
    autrement -16.4 / -15.1, aultrement -19.7 / -17.6. The sense is the same either way.
- **L05.16** `Zb`: **et**. Grade M. Decoder: et, S3 stable, 0.58.
  - Basis: Zb = et 11/32.
- **L05.17-18** `mm 9`: **ne**. Grade H. Decoder: ne, S1 stable, 0.86.
- **L05.19-L06.2** `vl o oo 3s`: **l'aye**. Grade M. Decoder: laye, S2 stable, 0.66.
- **L06.3-7** `# J ff 3 1`: **[les/ses eue?]**. Grade L (counted as two words). Decoder: les eue..., S3 stable.
  - Basis: the sense is unclear. Scores: "les eue" -43.3, "ses eue" -45.3, "sceue" -53.7.
- **L06.8-11** `To ^ 6 oo`: **quoy**. Grade L-M. Decoder: (eue)quoy, S3 stable.
  - Basis: To = q is not a key value (`To` is null 10/21). Read from the fixed phrase "quoy qu'il en soit".
- **L06.12-15** `N +d 3s =`: **qu'il en**. Grade H. Decoder: quil en, S1 stable, 0.86.
- **L06.16-19** `W #p II Qb`: **soit**. Grade M-H. Decoder: soit, S2 stable, 0.66.
- **L06.20** `7`: null.

### Lines 7-8

- **L07.0-6** `s ts ff z 1 6 #b`: **ce me sera**. Grade M. Decoder: ce me sera, unstable, 0.25.
  - Basis: 6 = r 11/205. Scores: "ce me sera plaisir d'en entendre" -61.8; the decode at weight 0.5, "cesse
    d'aplaisir ...", -67.6.
- **L07.7-12** `8p vl o # 6 +f`: **plaisir**. Grade M. Decoder: plaisir, S3 unstable, 0.25.
  - Basis: this needs 6 = si, which is not a key value. L07 sign 11 may be `B` (s), as the second reader has it.
- **L07.13-16** `R f 3s xx`: **d'en**. Grade H. Decoder: de n en, S1 stable, 0.86.
- **L07.17-L08.1** `ooo ff f * 7 +f 3s`: **(en)tendre**. Grade H. Decoder: tendre, S2 stable, 0.66.
- **L08.2-3** `cl Nf`: **la**. Grade H. The decoder has "la" at weights 0.3 and 0.5.
- **L08.4-13** `Hr ff W #p v d +f sl 8 xx`: **resolu[ti]on**. Grade L-M. Decoder: resolu... (0.3), laredo surin
  (0.4; S2 unstable, 0.25), resolucion (0.5).
  - Basis: r e s o l u [t/c] i o n. This needs L08 sign 8 = `vl` (the second reader's label; the final
    transcription keeps `v`) and +f = t or c (not key values).
  - Scores on the final transcription: resolucion -33.7, laredo surin -33.3, resolution -35.7.
  - Scores on the variant with `vl`: resolucion -29.8, resolution -31.8, laredo surin -36.4.
- **L08.14-16** `+ #b 6`: **car**. Grade L-M. Decoder: carne, S3 unstable.
  - Basis: scores "car commence" -26.2, "carne commence" -26.4.
- **L08.17** `C`: **[unread]**, one sign.
  - Basis: `C` is pa or y. Possibly "ja" ("car ja commence on ..."), but that is not supported (-37.5).
- **L08.18-L09.2** `ss m ff mm s`: **commence**. Grade M. Decoder: commence, S3 stable, 0.58.
  - Basis: ss = com is weak (1 of 5 occurrences; the sign has no settled value).

### Lines 9-10

- **L09.3-4** `#1 f`: **on**. Grade H. Decoder: on, S1 stable, 0.86.
- **L09.5-15** `# o 100 #b EE Hr #p p U 9 +f`: **a aprocher**. Grade M (two words). Decoder: sait (S3 unstable) pro
  (S1 stable) cher (S2 stable).
  - Basis: _ a _ a p r o c h e r. Sign evidence alone: "on a aprocher" -42.3, "on sait pro cher" -42.7; with the
    language model the decoder's version scores better (-64.6 against -66.8). The `#` is unexplained.
- **L09.16-17** `6 ^`: **du**. Grade M-H. Decoder: du, S3 stable, 0.58.
  - Basis: 6 = d 27/205.
- **L09.18-L10.1** `ooo 3s ts g z`: **temps**. Grade H. Decoder: temps, S2 stable, 0.66.
- **L10.2-3** `P c`: **que**. Grade M. Decoder: que, S3 unstable.
- **L10.4-15** `Nf ### C #b oo ff #b +f th V d 3s`: **[unread]**, 12 signs. Decoder: "a m payer h faue" (unstable,
  0.25-0.61).
  - Basis: the key values give a m pa/y a y e a r h h u e. No convincing word division was found.
- **L10.16-18** `z ff W`: **ses**. Grade M. Decoder: ses, S1 unstable, 0.61.
  - Basis: z = s 96/141. "mes" would fit the later "mes deux ans" but needs z = m.
- **L10.19-L11.3** `R ^ x o f #`: **deux ans**. Grade H. Decoder: deux (S2 stable) ans (S3 stable).

### Lines 11-13

- **L11.4** `C`: **y**. Grade M. Decoder: y, S3 stable, 0.58.
  - Basis: scores "ans y avons" -35.5, "ans avons" -37.4.
- **L11.5-13** `Nf 3 #1 mm W Aq 1 = d`: **avons tenu**. Grade H. Decoder: auons tenu, S1 stable, 0.86.
- **L11.14-16** `sl + Cx`: **icy**. Grade M. Decoder: icy, S3 unstable, 0.25.
  - Basis: i c y; + = c 76/224, Cx = y 22/86.
- **L11.17-18** `+d o`: **la**. Grade H. Decoder: la, S1 stable, 0.86.
- **L11.19-L12.2** `8p #b Lc m`: **paix**. Grade M-H. Decoder: paix, S2 stable, 0.66.
  - Basis: p a i x; Lc = i 43/45, m = x 7/64.
- **L12.3-7** `A To Tr V 3s`: **[pour] [faict]e**. Grade M-L (counted as one word). Decoder: he, S3 unstable.
  - Basis: `A` = pour and `V` = faict are values established or supported by NAF 6638; `To` and `Tr` are nulls.
  - The signs favour this reading (sign evidence -11.1 to -11.5 with the revised values, the best by about 3), but
    the language model prefers "he" or "urge" (totals -19.7 to -20.1, against -22.0 to -22.5).
- **L12.8-20** `## ff f 1 W + o oo s N +d 3s =`: **ie ne scay ce qu'il en**. Grade H (six words). Decoder: the same;
  S1 stable except scay and ce (S3 stable).
- **L13.0-3** `# ff 8 Nf`: **sera**. Grade M. Decoder: sera, S3 stable, 0.58.
  - Basis: 8 = r is weak.
- **L13.4** `N`: **qui**. Grade H. Decoder: qui, S1 stable, 0.86.
- **L13.5-13** `m Cx 3 #b sl z 6 cc Qb`: **m'y faisoit**. Grade L-M (two words). Decoder: mai soit, unstable.
  - Basis: sign evidence "my faisoit" -18.2 (the best); totals -26.7, against -26.2 for "mai soit".
  - 3 = f is weak (2/215), and L13 sign 7 may be part of the flourish of `Cx`.
- **L13.14-20** `3s = t #p +f 1 W`: **encores**. Grade L-M. Decoder: encores (S2 unstable) with the key as built; "en
  mores" at weights 0.3 and 0.4 with the revised values.
  - Basis: "encores" needs t = c, which is attested once in 67 occurrences (fr. 3151 and NAF 6638 together); `t` is
    m in 33 of 67. Scores: "en mores" -17.2, "encores" -18.0. The sense strongly favours "encores" ("qui m'y
    faisoit encores avoir plus de doute").
  - L13 sign 16 was looked at again on the image: it is a clear `t` (small knob on the crossbar, long curved tail),
    not `+` or `p`. So no c-sign rescues the word; the reading rests on sense.

### Lines 14-17

- **L14.0-15** `o ^ #1 # Hr | 8p vl 3 # | R | * 6 d a ooo 3s`: **avoir plus de doute**. Grade H (four words). Decoder:
  the same; auoir and plus S2 stable, de S1 stable, doute S3 unstable.
  - Basis: at weight 0.3 the decoder gives "doubte", the same word; the sign `a` between u and t is null in 12 of
    19 occurrences and b in 3.
- **L14.16-L15.14** `## ff mm 1 3 ff 3 +d m EE cl d W R m 3s d Hr 1 h`: **ie ne veulx plus demeurer**. Grade H (five
  words). Decoder: the same, S1 stable (ueulx S2 stable), 0.66-0.86.
- **L15.15-17** `# p Cx`: **icy**. Grade M. Decoder: icy, S3 stable, 0.58.
- **L15.18-L16.4** `x ^ sl ff +f 1 Wl`: **gueres** (guieres). Grade M. Decoder: gueres, S3 unstable, 0.25.
  - Basis: x = g 13/113. The decode at weight 0.3 has "guieres".
- **L16.5-14** `cl 6 mm Cx d 3s ts ff f Q`: **longuement**. Grade H-M. Decoder: longue men, S3 stable, 0.58.
  - Basis: l o n g u e m e n [t?]; Cx = g 28/86. `Q` is null 12/20.
- **L16.15** `Rq`: **et**. Grade H. Decoder: et, S1 stable, 0.86.
- **L16.16-L17.3** `mt EE cc z | o +d E h`: **au pis aller**. Grade M (three words). Decoder: agis aller with the key
  as built; with the revised values "au pis aller" at weight 0.3 and the non-word "auis aller" at 0.4 and 0.5
  (unstable).
  - Basis: `mt` = au, EE = p 45/51. Scores of "et au pis aller": -43.5 with the key as built, -33.2 / -31.9 with
    the revised values, where it also has the best sign evidence (-20.2 / -18.9). "et a pis aller" -34.9 / -37.4;
    "et agis aller" -33.0 / -35.5.
- **L17.4-5** `= Cx`: **n'y**. Grade M. Decoder: ny, S3 stable, 0.58.
- **L17.6-10** `^ ff ^ x P`: **veux que**. Grade M-H (two words). Decoder: eu (S1 unstable) with the key as built;
  "ueux que" at weights 0.3 and 0.4 with the revised values.
  - Basis: u e u x que. Scores of "ny ueux que": -19.9 with the key as built, -19.0 with the revised values.
- **L17.11-17** `o + th 3s d 1 +f`: **achever**. Grade H. Decoder: acheuer, S2 stable, 0.66.
- **L17.18-20** `### 3s Wl`: **mes**. Grade M. Decoder: mes, S3 stable, 0.58.

### Lines 18-20

- **L18.0-14** `R ii 3 x o f # Rl ff z ^ ## # 3s =`: **deux ans ie suis en**. Grade H (five words). Decoder: the
  same, stable (S1, S2 or S3).
- **L18.15-L19.0** `Ak mm 9 s Wl sl oo ff`: **necessité**. Grade M. Decoder: necessite, S3 stable, 0.58.
  - Basis: _ n e ce ss i t e; oo = t 25/105, Wl = ss 1/5.
  - Scores: "en necessite" -26.3, against -41.6 for "en une ce di e", which was the reading at an earlier stage.
- **L19.1** `4b`: **et**. Grade H. Decoder: et, S1 stable, 0.86.
- **L19.2-5** `o Cx 1 ^`: **ay eu**. Grade M (two words). Decoder: ay (S3 unstable, 0.25) eu (S1 unstable, 0.61).
- **L19.6-11** `12 Aq #1 14 d Qb`: **tout**. Grade M-H. Decoder: tout, S1 unstable, 0.61.
- **L19.12-18** `13 EE +d ff 2 cc f`: **plein**. Grade H. Decoder: plein, S1 stable, 0.86.
- **L19.19-20** `R 7`: **de**. Grade M-H. The decoder at weight 0.4 leaves `R` without a value here; R = de 186/216.
- **L20.0-3** `3s Qb 3s z`: **[d]ettes?**. Grade L. Decoder: ete / etes.
  - Basis: the signs give (e)tes, and L20 sign 0 may not be a sign at all. "plein de dettes" would need a d that
    is not there: on the variant transcription "de tes ces" scores -21.0 and "dettes ces" (without "de") -22.0,
    against -44.0 for "de dettes ces".
- **L20.4-6** `100 + J`: **ces**. Grade L-M.
- **L20.7-8** `Zb R`: **et de**. Grade M (two words).
- **L20.9-15** `Tr J 12 ff 12 Cz Cx`: **[unread]**, 7 signs. Decoder: esg.
- **L20.16-17** `s N`: **ce qui**. Grade M (two words).
- **L20.18-19** `Tr x`: **[con...]**. Grade L.
  - Basis: the word continues into the clear text that follows, which has not been transcribed.

### Tally

`python code/decode39.py` checks that the spans above cover each of the 405 signs exactly once, and counts:

- 365 signs in spans that are read, 4 signs taken as nulls between words, 36 signs unread (16 in L02, 1 in L08, 12
  in L10, 7 in L20);
- 100 words read (elided forms such as "qu'il" count as one word; "[pour] [faict]e" counts as one; "[les/ses eue?]"
  as two);
- 45 graded H or H-M, 39 graded M or M-H, 16 graded L, L-M or M-L.

Because the grades are judgment, the number of correct words cannot be read off this tally. Under the intended
meaning of the grades (H about 0.85, M about 0.6, L about 0.3) it would be 66.5 of 100, and probably fewer for the
reasons given under "How far to trust it".

## 4. Alternatives and open points

1. **Lines 1-3.** "dont noz" is fairly secure. The rest of line 2 is unread. "musulmans" is the best-scoring of the
   readings tried, but it needs an off-key value for `f` and a null `+`.
2. **Lines 4-6.**
   - "verité" depends on `Rr`, which has no key value.
   - "[ch]ose" cannot come from sign `1`.
   - "les/ses eue" is unread in substance.
   - "quoy" rests on To = q, which no key evidence supports. "qu'il en soit" is solid.
3. **Lines 7-8.**
   - "plaisir" needs one off-key value (6 = si).
   - "resolution" needs L08 sign 8 = `vl` and +f = t or c. With `vl`, "la resolucion" outscores "laredo surin" by
     6.6; with `v` the two are level.
4. **Line 10.** The 12 signs between "que" and "ses deux ans" are unread. "ses" (his, her, their) is what the signs
   give; "mes" would need z = m.
5. **Line 12, "pour faicte".** The signs favour it; the language model alone would choose "paix he".
6. **Line 13, "m'y faisoit".** This needs 3 = f. "mai soit" scores the same, so the word is open. The "encores"
   that follows needs t = c (1 in 67) and rests on sense only.
7. **Line 16, "au pis aller".** With `mt` = au this has the best sign evidence and the best score, but the decoder
   gives it only at weight 0.3.
8. **Line 18, "necessité".** This is the decoder's own choice and clearly the best of the readings compared. It
   still rests on thin evidence: oo = t in 25 of 105 alignments, Wl = ss in 1 of 5. At an earlier stage, with a key
   from less material, the reading was rejected.
9. **Line 20.** "dettes" depends on whether L20 sign 0 is a sign, and even then the text would be "de tes", not "de
   dettes". It remains a possibility only.

## 5. Hard limits

- **`Rr`** occurs nowhere in the known plaintext.
- **Sign-reading noise.** The two readers disagree on 11-16% of the signs. Several disputed signs fall exactly in
  the unread or weak spans (L02 signs 20-22, L04 sign 2, L06, L08 signs 8 and 12, L20 sign 0).
- **Mixed classes** ([KEY.md](KEY.md)): `#` (s 136, i 81 of 338), `+` (c 76 of 224), `6` (o 95, d 27 of 205; also
  null and r), `x` (x 14, g 13 of 113), `Cx` (g 28, y 22 of 86), `C` (pa 17, y 11 of 40). Each occurrence has to be
  resolved from context.
- **Language model.** Even at its best (stable, fully supported words) about one word in seven is wrong on the
  held-out text; in unstable, poorly supported spans about three in four are wrong.
- **No external check.** No decipherment of letter 39 is known. One publication that prints letters from this
  volume, Serrão (1969), could not be consulted ([LITERATURE.md](LITERATURE.md)).

## Files

- Transcriptions: data/fr3151/cipher/39_f71r.txt (final), 39_f71r_reader1.txt, 39_f71r_reader2.txt,
  39_f71r_alt.txt, 39_f71r_reader1_early.txt (used only by the key-fit control).
- Reading: data/fr3151/letter39_reading.tsv. Competing readings: data/fr3151/letter39_tests.tsv.
- Outputs: results/letter39_decode.txt, results/letter39_decode_n5orig.txt, results/letter39_tests.txt,
  results/letter39_readers.txt, results/keyfit_control.txt.
