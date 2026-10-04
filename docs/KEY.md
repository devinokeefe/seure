# The key

The key of the cipher used by Michel de Seure in his letters from Lisbon of December 1558 (BnF ms. fr. 3151,
nos. 39-44), as recovered from the contemporary decipherments bound in the same volume.

Machine-readable versions: [data/key/key.csv](../data/key/key.csv) and [data/key/key.json](../data/key/key.json).
The table below is generated from the same data by `python code/build_key.py --publish`.

## The system

- **Homophonic substitution.** Each letter has several signs. Well-attested examples: e = `ff`, `1`, `3s`, `9`;
  n = `xx`, `=`, `mm`, `f`; a = `#b`, `o`, `Nf`; u = `^`, `d`, `3`; t = `ooo`, `Qb`, `Aq`; s = `W`, `z`; r = `Hr`,
  `h`, `+f`.
- **Syllable signs:** `R` = de, `E` = le, `J` = es, `N` = qui, `Rq` and `4b` = et, `C` = pa (weak), `P` = que
  (see "Revised values"), and others.
- **Word signs:** `ta` = navires (11 of 11), `A` = pour and `V` = faict (see "Revised values"); two rare signs were
  each aligned once with a whole word (Castille, Peru). Word values are written in square brackets in the tables,
  e.g. `[pour]`. Square-bracketed words also turn up in the "other alignments" of many signs; those are alignment
  noise, not word values.
- **Nulls:** `7`, `M`, `12`, `13`, `14`, `100`, `2`, `Tr`, `ii`, `Ak` and others; most numerals are nulls. Written
  `_` in the tables.
- u/v and i/j are not distinguished; k is written c and w is written u in the normalised plaintext.
- Words are not separated. A syllable or word sign can run across a word boundary.

## Where the values come from

Every value is a count. The cipher blocks of letters 40, 41, 43 and 44 (8,361 signs) were aligned, sign by sign,
with their plaintext:

| letter | cipher (fo.) | signs | plaintext |
|---|---|---|---|
| 40, Seure to Henri II, 27 Dec 1558 | 73r-v | 1,082 | decipher sheet, fo. 74r |
| 44, Seure to Henri II, 12 Dec 1558 | 84r-v, 86r | 1,874 | decipher sheet, fo. 85r-v (blocks A, B, C) |
| 41, another copy of the letter of 12 Dec | 76r-77r | 1,883 | the same text (blocks A, B, C of no. 44) |
| 43, another copy of the letter of 12 Dec, almost wholly in cipher | 80r-82r | 3,522 | the whole text of no. 44, clear parts included |

The value of a sign is the plaintext unit it was aligned with most often. The alignment and the key were refined
in turn until they stopped changing ([METHOD.md](METHOD.md)). The alignments themselves are in
results/align_*.txt.

Two things follow from this and should be kept in mind when the table is used:

- The counts contain noise from two sources: signs that were misread in transcription, and places where the
  alignment is wrong. A long tail of single odd alignments in the "other alignments" column is that noise, not
  evidence of extra values.
- The postscript (block C: 41 fo. 77r, 43 fo. 82r, 44 fo. 86r; 1,057 signs) was kept out while the key was built,
  so that it could serve as a test. The table below does include it, aligned afterwards with the finished key. The
  key built from the training sets alone has 156 signs ([results/key_train.tsv](../results/key_train.tsv)); the
  table has 159.

## Columns

- **sign**: transcription label ([SYMBOLS.md](SYMBOLS.md)).
- **value**: the most frequent aligned unit. `_` = null; `[word]` = a whole word.
- **evidence**: occurrences aligned with that value / all aligned occurrences.
- **conf**: high = at least 8 occurrences and at least 75% on the value; medium = at least 4 occurrences and at
  least 60%; low = everything else. Of the 159 signs, 46 are high, 30 medium, 83 low.
- **other alignments**: the full distribution.
- **n40, n44, n41, n43, n39**: occurrences of the sign in the transcription of each letter.

## Revised values (from NAF 6638)

The cipher block "N. 5" of BnF ms. NAF 6638 ([NAF6638.md](NAF6638.md)) gives 4,261 further signs with known
plaintext, in a 19th-century copy. The copyist regularised the sign shapes, so that material was **not** added to
the counts below. It was used only for nine signs whose shape in the copy matches the original sign unmistakably
([data/key/revised_values.tsv](../data/key/revised_values.tsv),
[data/key/naf6638_n5_values.tsv](../data/key/naf6638_n5_values.tsv)):

| sign | table below | revised | basis |
|---|---|---|---|
| `mt` | a (31/34) | **au** | N. 5: au 7 of 11. In fr. 3151 the alignment gave the sign "a" and left the following u without a sign: an alignment artefact. |
| `A` | ur (22/42) | **[pour]** | N. 5: the word pour 11 of 21 (16 of 21 if the partial alignments po, pou are counted). In fr. 3151 the sign before `A` was forced to "po", leaving "ur": an artefact. |
| `P` | q (33/83) | **que** | N. 5: que 40 of 47. fr. 3151: q 33, que 17 of 83 (q followed by a skipped "ue"). |
| `V` | h (9/20) | **h or [faict]** | N. 5: faict 5 of 8 (3 as the whole word, 2 as its last letters). fr. 3151: h 9, [faict] 6 of 20. Both values seem to be real; not decided. |
| `t` | m (16/42) | **m** (confirmed) | N. 5: m 17 of 25, never c. |
| `4b` | et (8/10) | **et** (confirmed) | N. 5: et 3 of 5. |
| `14`, `13`, `12` | null | **null** (confirmed) | N. 5: 3 of 3, 1 of 1, 2 of 3. |

These revisions do not change the measured accuracy on the held-out text (mean character accuracy 0.589 without
them, 0.587 to 0.595 with them, depending on how they are applied; the signs concerned are rare there). They matter
for a few words of letter 39 ([LETTER39.md](LETTER39.md)).

## Known weaknesses

- **Mixed classes.** For some labels no clean visual distinction could be found between occurrences with
  different values. Each occurrence has to be resolved from context:
  - `#`: s 136, i 81 of 338;
  - `+`: c 76, r 35 of 224 (many of the r and l alignments are probably the look-alike signs `+f` and `+d`
    misread);
  - `6`: o 95, d 27, null 17, r 11 of 205;
  - `x`: x 14, g 13 of 113;
  - `Cx`: g 28, y 22 of 86;
  - `C`: pa 17, y 11 of 40;
  - `oo`: y 57, t 25 of 105 (the t cases are probably the three-loop sign `ooo` misread);
  - also `*`, `s`, `8`, `B`, `c`, `p`, `v`.
- **Classes split late.** `oo` (two loops) / `ooo` (three loops), `8` / `8p`, `p` / `po`, `cc` / `cl`, `t` / `ts`
  were first transcribed as one class each and separated afterwards, when occurrences sorted by their aligned value
  showed a visible difference. That evidence is selection-biased; the visual difference is real, but some
  occurrences are certainly on the wrong side.
- **Rare signs.** 83 of the 159 values are of low confidence, most of them because the sign occurs only a few
  times. Labels beginning with `N_` are provisional names for shapes seen once or twice.
- **`Rr`** occurs once, in letter 39, and nowhere in the known plaintext. It has no value.
- **Several readers.** The transcriptions of letters 41, 43 and 44 were made in separate passes; differences of
  labelling habit between passes are part of the distributions.

## Validation

The key was tested on text that was not used to build it: the three copies of block C were decoded with the
training-only key and a language model that had not seen block C. Character accuracy: 0.508 (44 C), 0.553 (41 C),
0.705 (43 PS); mean 0.589. Details and the word-level results are in [METHOD.md](METHOD.md). The accuracy is
limited by sign-reading noise and by the homophone and syllable ambiguity of the cipher, not only by the key.

## Key table

<!-- key-table:start (generated by code/build_key.py --publish) -->
| sign | value | evidence | conf | other alignments | n40 | n44 | n41 | n43 | n39 |
|---|---|---|---|---|---|---|---|---|---|
| `ff` | e | 297/359 | high | e:297 _:12 a:9 [mais]:5 l:3 n:2 ais:2 d:2 m:2 t:2 as:1 nt:1 u:1 la:1 mer:1 i:1 bie:1 feu:1 [iamais]:1 po:1 ux:1 h:1 nee:1 uou:1 q:1 fic:1 o:1 lad:1 par:1 r:1 arr:1 s:1 is:1 | 46 | 86 | 75 | 152 | 21 |
| `#` | s | 136/338 | low | s:136 i:81 _:25 a:18 l:6 e:6 t:5 r:5 o:5 f:4 bi:4 fi:3 po:2 ir:2 ib:1 y:1 par:1 er:1 qu:1 ci:1 ue:1 ues:1 ra:1 mez:1 [quelques]:1 mm:1 por:1 nou:1 li:1 il:1 c:1 mbi:1 p:1 le:1 m:1 [daultant]:1 n:1 [iamais]:1 q:1 ip:1 it:1 di:1 uoi:1 de:1 g:1 lli:1 ui:1 [marchandises]:1 he:1 ie:1 | 35 | 74 | 82 | 147 | 13 |
| `3s` | e | 242/282 | high | e:242 _:7 f:7 a:4 r:4 p:3 n:2 po:1 tie:1 o:1 [royaulme]:1 y:1 q:1 l:1 mer:1 la:1 t:1 ff:1 iep:1 bie:1 | 31 | 69 | 66 | 116 | 20 |
| `+` | c | 76/224 | low | c:76 r:35 _:12 l:10 m:9 t:8 i:7 o:6 u:6 s:3 n:3 mm:3 re:3 e:2 d:2 uel:2 a:2 la:2 q:1 [lest]:1 go:1 yn:1 uru:1 g:1 lli:1 ffr:1 les:1 le:1 sr:1 to:1 cqu:1 lqu:1 our:1 rm:1 x:1 tr:1 rip:1 ur:1 esc:1 eur:1 ltr:1 luy:1 rs:1 er:1 [despaigne]:1 ues:1 fr:1 apr:1 po:1 b:1 ndr:1 | 20 | 53 | 60 | 91 | 6 |
| `R` | de | 186/216 | high | de:186 _:7 e:6 a:4 t:3 i:2 d:1 [faict]:1 r:1 u:1 p:1 co:1 uou:1 ire:1 | 32 | 49 | 44 | 91 | 9 |
| `3` | u | 149/215 | medium | u:149 r:10 e:9 _:9 s:5 p:4 ire:2 f:2 t:1 me:1 ce:1 n:1 usq:1 et:1 and:1 ldr:1 pp:1 te:1 eul:1 [sorte]:1 y:1 pui:1 [royne]:1 [quelques]:1 ie:1 er:1 [quoy]:1 ro:1 ra:1 o:1 [dict]:1 rr:1 nt:1 | 18 | 50 | 53 | 94 | 10 |
| `f` | n | 176/207 | high | n:176 i:5 _:3 o:2 u:2 q:1 c:1 uue:1 el:1 e:1 s:1 ins:1 cul:1 est:1 la:1 nee:1 eux:1 ten:1 me:1 b:1 par:1 x:1 ste:1 d:1 | 21 | 48 | 48 | 90 | 11 |
| `6` | o | 95/205 | low | o:95 d:27 _:17 r:11 p:7 a:6 ce:4 u:2 ch:2 l:2 rd:2 e:2 i:1 c:1 qu:1 den:1 q:1 luy:1 que:1 [bien]:1 ion:1 lot:1 [faire]:1 ue:1 h:1 x:1 si:1 il:1 er:1 g:1 al:1 ard:1 m:1 t:1 y:1 b:1 f:1 rr:1 el:1 pre:1 | 28 | 42 | 50 | 85 | 10 |
| `1` | e | 170/199 | high | e:170 _:6 r:3 n:2 que:2 a:2 lz:1 mez:1 il:1 ost:1 li:1 u:1 ens:1 s:1 nee:1 rre:1 p:1 par:1 ien:1 m:1 | 32 | 44 | 44 | 79 | 13 |
| `^` | u | 170/195 | high | u:170 _:7 d:3 e:2 l:2 [quoy]:2 o:1 p:1 b:1 eus:1 bon:1 s:1 a:1 z:1 fa:1 | 20 | 41 | 45 | 89 | 10 |
| `E` | le | 130/181 | medium | le:130 _:11 n:4 p:4 l:3 la:3 c:3 s:2 ue:2 g:2 [leuer]:1 ett:1 es:1 f:1 r:1 i:1 [faire]:1 a:1 nn:1 [peru]:1 fl:1 co:1 po:1 en:1 d:1 ore:1 h:1 | 27 | 39 | 39 | 76 | 2 |
| `#1` | o | 144/179 | high | o:144 _:5 e:4 s:2 en:2 n:2 [marie]:1 i:1 tr:1 es:1 rr:1 a:1 toi:1 l:1 [bien]:1 q:1 m:1 u:1 [uiceroy]:1 for:1 ne:1 ion:1 te:1 lot:1 ict:1 ir:1 | 31 | 38 | 35 | 75 | 6 |
| `o` | a | 148/175 | high | a:148 _:6 il:3 e:2 o:2 m:1 rty:1 sil:1 g:1 el:1 bi:1 pas:1 ssi:1 r:1 c:1 p:1 ue:1 oit:1 ui:1 | 21 | 34 | 46 | 74 | 14 |
| `#b` | a | 145/170 | high | a:145 _:6 u:2 nt:2 ro:1 ain:1 [dargent]:1 c:1 st:1 car:1 r:1 i:1 que:1 fi:1 o:1 e:1 pas:1 it:1 [auoient]:1 | 22 | 39 | 39 | 70 | 8 |
| `Aq` | t | 122/170 | medium | t:122 r:6 _:6 i:4 l:3 il:2 e:2 s:2 a:2 o:1 [pour]:1 bi:1 [uous]:1 oct:1 ul:1 p:1 d:1 [mais]:1 qu:1 q:1 uue:1 lh:1 rm:1 art:1 [portugal]:1 ir:1 pr:1 c:1 iu:1 [nauires]:1 | 18 | 31 | 43 | 78 | 5 |
| `d` | u | 131/162 | high | u:131 _:3 s:3 h:2 d:2 a:2 l:2 on:1 ai:1 ff:1 r:1 i:1 [uostre]:1 e:1 n:1 moy:1 q:1 dud:1 ys:1 eus:1 c:1 eur:1 il:1 as:1 | 24 | 38 | 34 | 66 | 9 |
| `mm` | n | 130/157 | high | n:130 x:6 au:5 a:5 _:2 m:1 eau:1 nee:1 [france]:1 eru:1 [espaigne]:1 lx:1 e:1 [nauires]:1 | 21 | 34 | 35 | 67 | 8 |
| `W` | s | 126/151 | high | s:126 _:5 d:4 t:2 r:2 n:1 de:1 les:1 lle:1 c:1 ssi:1 ul:1 l:1 u:1 [armez]:1 e:1 h:1 | 22 | 32 | 38 | 59 | 8 |
| `Nf` | a | 133/149 | high | a:133 _:3 i:2 t:1 g:1 e:1 car:1 me:1 gra:1 [permise]:1 ont:1 m:1 s:1 r:1 | 16 | 31 | 32 | 70 | 6 |
| `xx` | n | 130/148 | high | n:130 le:3 p:2 do:2 l:2 a:2 nne:1 lle:1 e:1 _:1 o:1 de:1 nee:1 | 29 | 37 | 26 | 56 | 2 |
| `sl` | i | 108/144 | high | i:108 par:8 r:5 _:3 a:2 per:2 e:2 o:2 y:2 al:1 rip:1 ro:1 que:1 c:1 [despaigne]:1 toi:1 re:1 et:1 ue:1 | 14 | 36 | 39 | 55 | 6 |
| `z` | s | 96/141 | medium | s:96 g:6 _:5 u:3 l:3 n:3 p:3 po:2 ues:2 f:2 luy:1 ff:1 ar:1 m:1 e:1 er:1 ig:1 i:1 ce:1 d:1 ug:1 o:1 gn:1 res:1 qu:1 r:1 | 11 | 22 | 28 | 80 | 10 |
| `ooo` | t | 124/140 | high | t:124 ent:2 u:2 is:1 e:1 i:1 ult:1 r:1 [uingt]:1 tes:1 _:1 bi:1 b:1 p:1 ung:1 | 17 | 34 | 31 | 58 | 5 |
| `s` | ce | 69/139 | low | ce:69 _:21 p:8 e:5 r:4 a:3 c:2 d:2 is:2 pp:2 t:1 ep:1 ff:1 roy:1 [royne]:1 ee:1 ur:1 ier:1 i:1 [uiceroy]:1 fr:1 sr:1 q:1 s:1 n:1 u:1 l:1 ue:1 que:1 rr:1 [alloit]:1 | 21 | 37 | 23 | 58 | 5 |
| `Qb` | t | 121/139 | high | t:121 _:2 art:2 i:2 que:2 ic:1 [ueult]:1 ult:1 ge:1 n:1 po:1 ell:1 ent:1 par:1 c:1 | 6 | 32 | 38 | 63 | 6 |
| `Hr` | r | 116/132 | high | r:116 po:3 m:2 arm:1 _:1 y:1 roy:1 oit:1 i:1 el:1 e:1 bi:1 est:1 [faict]:1 | 24 | 29 | 27 | 52 | 5 |
| `#p` | o | 106/131 | high | o:106 a:7 _:2 de:1 p:1 e:1 en:1 n:1 sto:1 lot:1 as:1 ion:1 y:1 [argent]:1 l:1 rou:1 bon:1 q:1 m:1 | 11 | 29 | 27 | 64 | 5 |
| `*` | d | 58/130 | low | d:58 s:12 _:6 o:6 ss:5 e:4 [dargent]:3 l:2 p:2 i:2 r:2 z:2 b:1 po:1 ilz:1 qu:1 tar:1 as:1 [royne]:1 [despaigne]:1 mm:1 mme:1 se:1 m:1 u:1 urr:1 rri:1 rr:1 oc:1 us:1 arg:1 nn:1 q:1 t:1 ues:1 tt:1 n:1 c:1 | 25 | 21 | 28 | 56 | 4 |
| `9` | e | 107/126 | high | e:107 r:3 a:2 o:2 rs:1 po:1 il:1 que:1 [quilz]:1 l:1 f:1 pp:1 nne:1 t:1 h:1 uco:1 | 16 | 27 | 30 | 53 | 4 |
| `x` | x | 14/113 | low | x:14 g:13 y:8 _:8 com:6 con:5 s:5 p:4 r:4 i:3 c:3 q:3 t:2 a:2 l:2 m:2 n:2 is:1 ul:1 my:1 ce:1 nn:1 d:1 cc:1 res:1 co:1 mm:1 f:1 e:1 par:1 ong:1 ll:1 cel:1 li:1 ch:1 ire:1 luy:1 eu:1 ces:1 o:1 toi:1 ue:1 ac:1 b:1 | 17 | 26 | 32 | 38 | 5 |
| `8` | o | 49/111 | low | o:49 b:9 d:7 _:6 h:5 et:4 pp:3 p:3 rr:2 r:2 a:2 [uous]:2 u:2 com:1 [uiceroy]:1 ch:1 le:1 de:1 mm:1 i:1 ap:1 au:1 rd:1 dis:1 ue:1 roy:1 x:1 y:1 | 8 | 23 | 28 | 52 | 2 |
| `+f` | r | 74/105 | medium | r:74 _:4 l:3 n:3 i:2 o:2 [faire]:2 s:1 [dargent]:1 au:1 ipr:1 q:1 c:1 que:1 uu:1 [fort]:1 po:1 p:1 b:1 ee:1 f:1 ons:1 | 19 | 21 | 20 | 45 | 11 |
| `oo` | y | 57/105 | low | y:57 t:25 _:3 i:3 est:2 ent:2 n:1 ei:1 is:1 b:1 a:1 s:1 it:1 p:1 et:1 [peru]:1 e:1 bi:1 tz:1 | 13 | 17 | 21 | 54 | 6 |
| `=` | n | 92/104 | high | n:92 m:2 _:2 e:1 or:1 [aucunes]:1 y:1 te:1 l:1 a:1 s:1 | 10 | 11 | 34 | 49 | 9 |
| `vl` | l | 63/89 | medium | l:63 b:4 g:3 uel:2 u:1 our:1 i:1 luy:1 be:1 [portugal]:1 ire:1 bre:1 con:1 r:1 _:1 ch:1 s:1 q:1 ub:1 f:1 che:1 | 12 | 19 | 18 | 40 | 4 |
| `n` | z | 68/86 | high | z:68 s:4 d:3 les:1 siz:1 y:1 [pourrez]:1 l:1 _:1 oy:1 [pour]:1 i:1 [passez]:1 ctz:1 | 16 | 16 | 15 | 39 | 2 |
| `Cx` | g | 28/86 | low | g:28 y:22 _:9 r:4 a:3 luy:2 p:2 uel:1 ue:1 est:1 ys:1 bi:1 ai:1 my:1 oy:1 ed:1 e:1 [marchandises]:1 ph:1 l:1 de:1 z:1 c:1 | 6 | 19 | 16 | 45 | 7 |
| `c` | f | 33/86 | low | f:33 l:20 s:2 y:2 o:2 g:2 [portugal]:2 n:2 _:2 uel:2 a:2 il:1 omb:1 q:1 que:1 se:1 ue:1 [maieste]:1 lle:1 uil:1 ldr:1 u:1 b:1 h:1 [nauires]:1 yn:1 | 8 | 21 | 22 | 35 | 1 |
| `P` | q | 33/83 | low | q:33 que:17 _:5 ue:3 de:3 [quelque]:2 c:2 ge:1 ha:1 luy:1 [faire]:1 f:1 ues:1 z:1 s:1 rge:1 uel:1 t:1 [perdu]:1 [uostre]:1 [daultant]:1 e:1 g:1 h:1 esc:1 | 6 | 21 | 19 | 37 | 3 |
| `+d` | l | 70/81 | high | l:70 u:2 les:2 [philippe]:1 r:1 qu:1 d:1 cel:1 uos:1 c:1 | 5 | 16 | 19 | 41 | 7 |
| `###` | m | 67/78 | high | m:67 e:2 [nauires]:2 is:1 u:1 t:1 i:1 tr:1 [arrester]:1 par:1 | 5 | 20 | 18 | 35 | 4 |
| `N` | qui | 64/74 | high | qui:64 _:5 as:1 ues:1 p:1 par:1 a:1 | 10 | 15 | 18 | 31 | 4 |
| `J` | es | 51/71 | medium | es:51 u:5 p:3 _:2 r:2 e:1 st:1 lme:1 b:1 a:1 er:1 la:1 s:1 | 11 | 16 | 14 | 30 | 4 |
| `h` | r | 53/71 | medium | r:53 p:3 e:2 z:2 is:1 _:1 for:1 bre:1 per:1 s:1 pp:1 luy:1 que:1 a:1 [faict]:1 | 17 | 15 | 18 | 21 | 4 |
| `##` | i | 44/69 | medium | i:44 r:8 p:2 mm:1 a:1 _:1 y:1 l:1 pr:1 ro:1 rq:1 us:1 [mais]:1 u:1 lle:1 [iamais]:1 fo:1 rr:1 | 10 | 15 | 18 | 26 | 3 |
| `B` | s | 33/68 | low | s:33 d:6 [uous]:3 _:2 r:2 eul:2 arg:2 o:1 tr:1 tre:1 f:1 que:1 ne:1 po:1 ip:1 c:1 m:1 qui:1 roy:1 luy:1 [empereur]:1 i:1 pp:1 u:1 p:1 | 9 | 15 | 13 | 31 | 2 |
| `cl` | l | 58/68 | high | l:58 i:3 n:1 _:1 [armez]:1 eru:1 d:1 a:1 u:1 | 4 | 13 | 18 | 33 | 4 |
| `p` | c | 36/67 | low | c:36 f:3 il:3 t:3 e:2 [faire]:2 n:2 ou:1 uff:1 p:1 o:1 y:1 a:1 q:1 tic:1 luy:1 up:1 [argent]:1 et:1 [despaigne]:1 r:1 i:1 l:1 | 13 | 14 | 14 | 26 | 2 |
| `m` | m | 41/64 | medium | m:41 x:7 u:3 au:3 _:2 e:1 a:1 oys:1 [uostre]:1 [marie]:1 [espaigne]:1 ulm:1 ul:1 | 13 | 18 | 14 | 19 | 6 |
| `v` | s | 30/64 | low | s:30 h:4 e:3 _:3 y:2 luy:2 g:2 el:1 sfa:1 ue:1 r:1 omp:1 po:1 [dire]:1 f:1 cha:1 pue:1 uel:1 l:1 i:1 urr:1 ues:1 o:1 a:1 lar:1 | 10 | 34 | 11 | 9 | 1 |
| `7` | _ | 41/55 | medium | _:41 est:5 e:2 ay:1 moy:1 que:1 s:1 t:1 is:1 rem:1 | 7 | 12 | 18 | 18 | 4 |
| `EE` | p | 45/51 | high | p:45 g:3 _:2 al:1 | 3 | 9 | 12 | 27 | 4 |
| `Tr` | _ | 40/49 | high | _:40 b:3 i:3 ch:1 u:1 d:1 | 1 | 8 | 12 | 28 | 3 |
| `y` | s | 14/46 | low | s:14 _:6 dit:4 e:3 [dict]:3 r:2 i:2 l:2 arg:1 omm:1 en:1 x:1 rg:1 lad:1 d:1 pri:1 [cest]:1 [faict]:1 | 6 | 11 | 9 | 20 | 0 |
| `Lc` | i | 43/45 | high | i:43 _:1 [faict]:1 | 0 | 9 | 13 | 23 | 1 |
| `A` | ur | 22/42 | low | ur:22 [pour]:9 _:3 e:3 p:2 po:1 oye:1 c:1 | 8 | 8 | 8 | 18 | 1 |
| `t` | m | 16/42 | low | m:16 t:7 n:3 u:3 _:2 e:1 c:1 nu:1 ict:1 die:1 il:1 s:1 [partit]:1 [quelle]:1 i:1 h:1 | 12 | 7 | 3 | 20 | 1 |
| `C` | pa | 17/40 | low | pa:17 y:11 per:2 a:1 po:1 iay:1 d:1 [part]:1 ne:1 r:1 ge:1 i:1 n:1 | 6 | 9 | 13 | 12 | 4 |
| `cc` | i | 28/39 | medium | i:28 l:4 p:1 est:1 uel:1 qu:1 ul:1 che:1 r:1 | 8 | 5 | 13 | 13 | 3 |
| `Phi` | t | 16/39 | low | t:16 f:6 que:2 onf:1 p:1 [daultant]:1 i:1 [dargent]:1 [quelque]:1 u:1 e:1 fl:1 pe:1 ge:1 q:1 ux:1 _:1 po:1 | 5 | 9 | 7 | 18 | 0 |
| `g` | p | 27/35 | high | p:27 r:3 u:1 br:1 iue:1 luy:1 g:1 | 5 | 7 | 4 | 19 | 1 |
| `mt` | a | 31/34 | high | a:31 u:1 ul:1 [royaulme]:1 | 1 | 11 | 5 | 17 | 2 |
| `Zb` | et | 11/32 | low | et:11 _:8 ge:1 [uous]:1 p:1 g:1 [peru]:1 q:1 que:1 u:1 ue:1 a:1 r:1 l:1 e:1 | 5 | 5 | 7 | 15 | 2 |
| `ae` | et | 5/31 | low | et:5 [portugal]:4 i:3 u:2 r:2 l:2 o:2 toi:1 t:1 con:1 a:1 ais:1 com:1 de:1 _:1 roy:1 ce:1 n:1 | 7 | 4 | 8 | 12 | 0 |
| `S` | r | 20/30 | medium | r:20 si:2 d:2 ph:1 p:1 [uostre]:1 co:1 con:1 que:1 | 1 | 3 | 10 | 16 | 1 |
| `M` | _ | 28/28 | high | _:28 | 5 | 7 | 7 | 9 | 1 |
| `po` | il | 9/28 | low | il:9 c:7 _:3 t:2 f:2 a:1 o:1 n:1 ic:1 l:1 | 3 | 3 | 1 | 21 | 0 |
| `II` | i | 8/27 | low | i:8 o:4 a:3 t:2 n:1 r:1 e:1 p:1 sa:1 _:1 z:1 re:1 y:1 luy:1 | 4 | 9 | 5 | 9 | 1 |
| `2` | _ | 19/25 | high | _:19 que:2 t:1 bt:1 [apres]:1 yn:1 | 7 | 7 | 6 | 5 | 2 |
| `th` | h | 22/25 | high | h:22 r:1 f:1 [cest]:1 | 4 | 1 | 6 | 14 | 2 |
| `8p` | p | 18/22 | high | p:18 l:1 la:1 g:1 [payez]:1 | 4 | 4 | 7 | 7 | 3 |
| `12` | _ | 21/22 | high | _:21 ue:1 | 2 | 5 | 8 | 7 | 4 |
| `To` | _ | 10/21 | low | _:10 moy:4 i:1 q:1 u:1 [peru]:1 moi:1 est:1 m:1 | 3 | 2 | 6 | 10 | 2 |
| `Q` | _ | 12/20 | medium | _:12 et:2 que:2 i:2 sd:1 [uostre]:1 | 3 | 6 | 2 | 9 | 3 |
| `V` | h | 9/20 | low | h:9 [faict]:6 ict:1 fa:1 s:1 g:1 a:1 | 5 | 2 | 2 | 11 | 2 |
| `100` | _ | 17/19 | high | _:17 ss:1 que:1 | 2 | 1 | 8 | 8 | 2 |
| `a` | _ | 12/19 | medium | _:12 b:3 u:1 uel:1 sch:1 i:1 | 4 | 6 | 4 | 5 | 1 |
| `?` | _ | 13/19 | medium | _:13 t:2 b:1 u:1 beau:1 f:1 | 2 | 5 | 5 | 7 | 0 |
| `23` | _ | 16/18 | high | _:16 s:1 [peru]:1 | 4 | 2 | 8 | 4 | 0 |
| `Ve` | t | 9/17 | low | t:9 que:3 r:3 u:1 _:1 | 10 | 7 | 0 | 0 | 0 |
| `+o` | _ | 15/16 | high | _:15 i:1 | 0 | 6 | 1 | 9 | 0 |
| `Rl` | i | 13/16 | high | i:13 que:1 [ainsi]:1 s:1 | 0 | 3 | 1 | 12 | 1 |
| `r` | i | 5/14 | low | i:5 g:3 _:2 l:1 z:1 es:1 s:1 | 3 | 7 | 2 | 2 | 0 |
| `lo` | _ | 7/13 | low | _:7 il:2 r:1 ui:1 t:1 par:1 | 0 | 1 | 3 | 9 | 1 |
| `Ob` | l | 8/12 | medium | l:8 ur:1 t:1 e:1 nco:1 | 2 | 0 | 0 | 10 | 0 |
| `14` | _ | 10/12 | high | _:10 ier:1 que:1 | 0 | 6 | 4 | 2 | 2 |
| `ta` | [nauires] | 11/11 | high | [nauires]:11 | 3 | 0 | 2 | 6 | 0 |
| `Ce` | _ | 7/11 | medium | _:7 g:4 | 2 | 1 | 3 | 5 | 0 |
| `L` | e | 6/11 | low | e:6 deb:1 i:1 o:1 _:1 s:1 | 2 | 7 | 1 | 1 | 0 |
| `Cz` | _ | 4/10 | low | _:4 g:3 p:1 i:1 z:1 | 1 | 3 | 3 | 3 | 2 |
| `Rq` | et | 8/10 | high | et:8 de:1 l:1 | 0 | 0 | 1 | 9 | 1 |
| `4b` | et | 8/10 | high | et:8 a:1 u:1 | 0 | 1 | 2 | 7 | 1 |
| `k` | g | 2/9 | low | g:2 uel:1 cc:1 f:1 pl:1 i:1 u:1 l:1 | 4 | 1 | 4 | 0 | 0 |
| `cc?` | l | 3/9 | low | l:3 i:2 mbi:1 ipt:1 ain:1 _:1 | 0 | 9 | 0 | 0 | 0 |
| `ii` | _ | 7/8 | high | _:7 n:1 | 2 | 2 | 1 | 3 | 2 |
| `Ak` | _ | 7/8 | high | _:7 di:1 | 1 | 1 | 3 | 3 | 1 |
| `uT` | s | 2/7 | low | s:2 l:1 n:1 e:1 ge:1 a:1 | 2 | 0 | 0 | 5 | 0 |
| `pa` | ent | 5/7 | medium | ent:5 e:1 [argent]:1 | 1 | 2 | 2 | 2 | 0 |
| `Dt` | t | 6/7 | medium | t:6 a:1 | 1 | 6 | 0 | 0 | 0 |
| `vt` | s | 3/7 | low | s:3 l:1 e:1 b:1 p:1 | 2 | 0 | 5 | 0 | 0 |
| `U` | h | 5/7 | medium | h:5 urq:1 est:1 | 1 | 2 | 1 | 3 | 1 |
| `oo?` | t | 5/7 | medium | t:5 y:2 | 0 | 7 | 0 | 0 | 0 |
| `=o` | _ | 6/7 | medium | _:6 n:1 | 0 | 6 | 1 | 0 | 0 |
| `Cs` | e | 4/6 | medium | e:4 _:1 m:1 | 1 | 0 | 2 | 3 | 1 |
| `13` | _ | 6/6 | medium | _:6 | 1 | 2 | 1 | 2 | 2 |
| `l` | il | 2/5 | low | il:2 ue:1 les:1 e:1 | 3 | 1 | 0 | 1 | 0 |
| `ts` | m | 4/5 | medium | m:4 x:1 | 4 | 0 | 0 | 1 | 3 |
| `C3` | a | 3/5 | medium | a:3 r:1 ire:1 | 1 | 1 | 2 | 1 | 0 |
| `ss` | q | 1/5 | low | q:1 com:1 om:1 c:1 ais:1 | 1 | 2 | 0 | 2 | 1 |
| `Cd` | p | 1/5 | low | p:1 yer:1 fe:1 a:1 cel:1 | 2 | 2 | 1 | 0 | 0 |
| `4` | est | 1/5 | low | est:1 e:1 a:1 r:1 l:1 | 1 | 1 | 3 | 0 | 0 |
| `Tq` | re | 1/5 | low | re:1 m:1 u:1 po:1 te:1 | 0 | 1 | 1 | 3 | 0 |
| `Wl` | ss | 1/5 | low | ss:1 ess:1 is:1 _:1 u:1 | 0 | 3 | 0 | 2 | 3 |
| `re` | _ | 3/5 | medium | _:3 s:1 i:1 | 0 | 4 | 0 | 1 | 0 |
| `c?` | l | 2/5 | low | l:2 e:1 q:1 f:1 | 0 | 5 | 0 | 0 | 0 |
| `8?` | o | 3/5 | medium | o:3 con:1 b:1 | 0 | 5 | 0 | 0 | 0 |
| `Ca` | _ | 3/4 | medium | _:3 ir:1 | 1 | 1 | 0 | 2 | 0 |
| `N_lb` | que | 2/4 | low | que:2 q:1 qu:1 | 0 | 0 | 4 | 0 | 0 |
| `Pb` | o | 1/3 | low | o:1 e:1 que:1 | 1 | 1 | 1 | 0 | 0 |
| `+2` | i | 3/3 | low | i:3 | 3 | 0 | 0 | 0 | 0 |
| `ma` | e | 1/3 | low | e:1 [espaigne]:1 [lespaigne]:1 | 1 | 0 | 1 | 1 | 0 |
| `dd` | _ | 3/3 | low | _:3 | 1 | 0 | 0 | 2 | 0 |
| `30` | _ | 3/3 | low | _:3 | 1 | 0 | 1 | 1 | 0 |
| `40` | a | 3/3 | low | a:3 | 0 | 2 | 1 | 0 | 0 |
| `p?` | f | 2/3 | low | f:2 c:1 | 0 | 3 | 0 | 0 | 0 |
| `Sh` | f | 1/3 | low | f:1 por:1 r:1 | 0 | 3 | 0 | 0 | 0 |
| `N_Phib` | que | 3/3 | low | que:3 | 0 | 3 | 0 | 0 | 0 |
| `O` | t | 1/2 | low | t:1 y:1 | 2 | 0 | 0 | 0 | 0 |
| `8b` | r | 1/2 | low | r:1 t:1 | 2 | 0 | 0 | 0 | 0 |
| `ca` | la | 1/2 | low | la:1 [marie]:1 | 1 | 0 | 0 | 1 | 0 |
| `N_ven` | t | 1/2 | low | t:1 q:1 | 0 | 0 | 2 | 0 | 0 |
| `Ll` | oys | 1/2 | low | oys:1 _:1 | 0 | 0 | 0 | 2 | 0 |
| `CR` | i | 1/2 | low | i:1 g:1 | 0 | 2 | 0 | 0 | 0 |
| `sm` | t | 1/2 | low | t:1 _:1 | 0 | 2 | 0 | 0 | 0 |
| `t?` | n | 2/2 | low | n:2 | 0 | 2 | 0 | 0 | 0 |
| `3o` | y | 1/2 | low | y:1 _:1 | 0 | 2 | 0 | 0 | 0 |
| `Xs` | g | 2/2 | low | g:2 | 0 | 2 | 0 | 0 | 0 |
| `N_ang` | bl | 1/2 | low | bl:1 o:1 | 0 | 2 | 0 | 0 | 0 |
| `bar` | _ | 1/1 | low | _:1 | 1 | 0 | 0 | 0 | 0 |
| `Pt` | que | 1/1 | low | que:1 | 1 | 0 | 0 | 0 | 0 |
| `yb` | r | 1/1 | low | r:1 | 1 | 0 | 0 | 0 | 0 |
| `cx` | il | 1/1 | low | il:1 | 1 | 0 | 0 | 0 | 0 |
| `H` | lz | 1/1 | low | lz:1 | 1 | 0 | 0 | 0 | 0 |
| `tl` | u | 1/1 | low | u:1 | 1 | 0 | 0 | 0 | 0 |
| `Lam` | s | 1/1 | low | s:1 | 1 | 0 | 0 | 0 | 0 |
| `#x` | li | 1/1 | low | li:1 | 1 | 0 | 0 | 0 | 0 |
| `Il` | _ | 1/1 | low | _:1 | 1 | 0 | 0 | 0 | 0 |
| `Td` | [castille] | 1/1 | low | [castille]:1 | 1 | 0 | 0 | 0 | 0 |
| `N_bb` | i | 1/1 | low | i:1 | 0 | 0 | 1 | 0 | 0 |
| `Lcs` | [peru] | 1/1 | low | [peru]:1 | 0 | 0 | 0 | 1 | 0 |
| `N_lo0` | b | 1/1 | low | b:1 | 0 | 0 | 0 | 1 | 0 |
| `Et` | _ | 1/1 | low | _:1 | 0 | 1 | 0 | 0 | 0 |
| `D` | e | 1/1 | low | e:1 | 0 | 1 | 0 | 0 | 0 |
| `CS` | i | 1/1 | low | i:1 | 0 | 1 | 0 | 0 | 0 |
| `Cv` | g | 1/1 | low | g:1 | 0 | 1 | 0 | 0 | 0 |
| `Pl` | a | 1/1 | low | a:1 | 0 | 1 | 0 | 0 | 0 |
| `rr` | p | 1/1 | low | p:1 | 0 | 1 | 0 | 0 | 0 |
| `N_pt` | _ | 1/1 | low | _:1 | 0 | 0 | 0 | 1 | 0 |
| `N_mo` | m | 1/1 | low | m:1 | 0 | 0 | 0 | 1 | 0 |

Signs that occur in letter 39 but in no known-plaintext alignment (no key value): `Rr`.

### Inverse key (high and medium confidence only)

| plaintext | signs |
|---|---|
| _ | `7` (41/55), `Tr` (40/49), `M` (28/28), `2` (19/25), `12` (21/22), `Q` (12/20), `100` (17/19), `a` (12/19), `?` (13/19), `23` (16/18), `+o` (15/16), `14` (10/12), `Ce` (7/11), `ii` (7/8), `Ak` (7/8), `=o` (6/7), `13` (6/6), `re` (3/5), `Ca` (3/4) |
| a | `o` (148/175), `#b` (145/170), `Nf` (133/149), `mt` (31/34), `C3` (3/5) |
| e | `ff` (297/359), `3s` (242/282), `1` (170/199), `9` (107/126), `Cs` (4/6) |
| h | `th` (22/25), `U` (5/7) |
| i | `sl` (108/144), `##` (44/69), `Lc` (43/45), `cc` (28/39), `Rl` (13/16) |
| l | `vl` (63/89), `+d` (70/81), `cl` (58/68), `Ob` (8/12) |
| m | `###` (67/78), `m` (41/64), `ts` (4/5) |
| n | `f` (176/207), `mm` (130/157), `xx` (130/148), `=` (92/104) |
| o | `#1` (144/179), `#p` (106/131), `8?` (3/5) |
| p | `EE` (45/51), `g` (27/35), `8p` (18/22) |
| r | `Hr` (116/132), `+f` (74/105), `h` (53/71), `S` (20/30) |
| s | `W` (126/151), `z` (96/141) |
| t | `Aq` (122/170), `ooo` (124/140), `Qb` (121/139), `Dt` (6/7), `oo?` (5/7) |
| u | `3` (149/215), `^` (170/195), `d` (131/162) |
| z | `n` (68/86) |
| [nauires] | `ta` (11/11) |
| de | `R` (186/216) |
| ent | `pa` (5/7) |
| es | `J` (51/71) |
| et | `Rq` (8/10), `4b` (8/10) |
| le | `E` (130/181) |
| qui | `N` (64/74) |
<!-- key-table:end -->
