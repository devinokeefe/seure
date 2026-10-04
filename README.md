# Michel de Seure's cipher: letters from Lisbon, December 1558

Devin O'Keefe, 2026. Working release, not peer-reviewed.

In December 1558 Michel de Seure, the French ambassador in Portugal, wrote five letters partly in a cipher of drawn
signs and numerals. They survive in Paris (BnF ms. français 3151). Decipherments made at the time are bound in the
same volume and cover four of the letters. The fifth, letter 39, has none.

This repository rebuilds the key from those decipherments and uses it to read about two thirds of letter 39.

## What letter 39 says

The cipher passage, as far as it can be read. `[...]` is a gap and `[word?]` is a weak reading.

> ... dont noz [...] a retraite des [musulmans?] [...] qu'ilz [disent?] verité, que la [ch?]ose sera autrement, et ne
> l'aye [...] quoy qu'il en soit. Ce me sera plaisir d'en entendre la resolu[ti]on, car [.] commence on a aprocher
> du temps que [...] ses deux ans. Y avons tenu icy la paix [pour faicte?]; ie ne scay ce qu'il en sera, qui m'y
> [f]aisoit encores avoir plus de doute. Ie ne veulx plus demeurer icy gueres longuement, et au pis aller n'y veux
> que achever mes deux ans. Ie suis en necessité, et ay eu tout plein de [dettes?], ces et de [...] ce qui [con...]

In English:

> ... of which our [...] the withdrawal of the [Muslims?] [...], if they are telling the truth, that the [matter]
> will turn out otherwise, and I have not [...] it; whatever the case, I shall be glad to learn the decision on it,
> for we are beginning to approach the time when [...] two years. Here we have taken the peace as concluded; I do
> not know what will come of it, which made me doubt all the more. I no longer wish to stay here much longer, and at
> worst I want only to complete my two years here. I am in want, and have had a great many [debts?] ... and of ...
> which ...

The peace is the one France and Spain were negotiating that winter, signed at Cateau-Cambrésis in April 1559. Seure
got his wish: Jean Nicot replaced him in Lisbon the same year.

How far to trust it: the second half (from "Y avons tenu icy la paix") is read nearly in full, and the opening and
the last line are mostly unread. Of the 405 signs, 36 are unread. Of the 100 words read, 45 are graded high, 39
medium and 16 low, which puts the expected number of correct words at about two thirds. No other copy or
decipherment of this letter is known, so the reading cannot be checked against anything. The evidence for every word
is in [docs/LETTER39.md](docs/LETTER39.md).

## How the cipher works

A letter can be written with several different signs. Some signs stand for a syllable or a whole word, and some
mean nothing. Here is a phrase from line 14, in the ASCII labels this repository uses for the signs:

| | ie | ne | veulx | plus | demeurer |
|---|---|---|---|---|---|
| signs | `##` `ff` | `mm` `1` | `3` `ff` `3` `+d` `m` | `EE` `cl` `d` `W` | `R` `m` `3s` `d` `Hr` `1` `h` |
| values | i e | n e | u e u l x | p l u s | de m e u r e r |

Three different signs write e. Two each write u, l and r. The sign `m` is an x in "veulx" and an m in "demeurer",
and `R` is the syllable de. (u and v are one letter, as are i and j.)

The key gives a value to 159 signs: [docs/KEY.md](docs/KEY.md). The labels are described in
[docs/SYMBOLS.md](docs/SYMBOLS.md).

## How it was read

The key was not broken blind. The decipherments in the volume give the plaintext of 8,361 cipher signs, and lining
the two up yields the value of each sign.

To measure how well that key reads text it has not seen, a 1,057-sign postscript was kept out of the key building
and then decoded by program. It survives in three separately enciphered copies; the program got 51%, 55% and 70% of
their letters right. A decoder that is right a little over half the time needs a person to finish the job, and
cannot finish all of it. That is why letter 39 is a partial reading. Details are in
[docs/METHOD.md](docs/METHOD.md).

## A second finding

BnF ms. NAF 6638 is a 19th-century copy of Seure's despatches of 1559. It reproduces two cipher blocks from February
1559, about 4,500 signs, in the same cipher. The clear text on pp. 29-34 of that copy turns out to be the
decipherment of those blocks. Falgairolle printed that text in 1895 without connecting it to the cipher.
See [docs/NAF6638.md](docs/NAF6638.md).

## Limits

- Letter 39 is not solved. 36 signs are unread, about a third of the words read are probably wrong, and the
  confidence grades are judgment.
- 83 of the 159 key values are of low confidence. One sign in letter 39, `Rr`, has no value at all.
- The transcriptions contain errors. Two independent transcriptions of letter 39 agree on 84% of the signs.
- No published key or reading of letter 39 was found. One article that prints two letters from this volume
  (Serrão 1969) could not be consulted. What was checked is listed in [docs/LITERATURE.md](docs/LITERATURE.md).

## Check it yourself

```
python code/reproduce.py
```

Python 3.9 or later, no other packages, about 15 minutes. It recomputes every figure quoted in this repository and
prints it next to the documented value. `python code/reproduce.py --check` compares without recomputing.

The manuscript is on Gallica: <https://gallica.bnf.fr/ark:/12148/btv1b9059865k>. Letter 39 is fo. 71r (view 72,
right-hand page). The decipherments are on fo. 74r (view 75) and fo. 85r-v (views 86-87). Each transcription file
in `data/` names its folio and view and has one text line per manuscript line. No manuscript images are included
here.

## Contents

| path | what |
|---|---|
| [docs/LETTER39.md](docs/LETTER39.md) | letter 39: the reading, word by word, with the evidence |
| [docs/KEY.md](docs/KEY.md) | the key: every sign, its value, and how often the value is attested |
| [docs/SYMBOLS.md](docs/SYMBOLS.md) | the sign labels used in the transcriptions |
| [docs/METHOD.md](docs/METHOD.md) | how the key was built and tested |
| [docs/NAF6638.md](docs/NAF6638.md) | the cipher blocks of February 1559 and their decipherment |
| [docs/LITERATURE.md](docs/LITERATURE.md) | sources, earlier work, what was and was not checked |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | history of the reading |
| [data/](data/README.md) | transcriptions, plaintexts, key files, language-model text |
| [code/](code/README.md) | the scripts |
| results/ | their output |

## Sources

- The manuscripts: Bibliothèque nationale de France, Français 3151 and NAF 6638, consulted through Gallica.
- Edmond Falgairolle, "Le chevalier de Seure, ambassadeur de France en Portugal au XVIe siècle", *Mémoires de
  l'Académie de Nîmes* XVIII (1895), pp. 49-85. It prints Seure's letters of 1559, including the text discussed
  under "A second finding".
- Edmond Falgairolle, *Jean Nicot, ambassadeur de France en Portugal au XVIe siècle: sa correspondance diplomatique
  inédite* (Paris, 1897). Its scanned text (Internet Archive) trains the language model.
- Daniel Bourdeau's catalogue of unsolved historical ciphers (dbourdeau.github.io/cyphersolver), which lists these
  letters as open and drew attention to them.

## Licence

Code: MIT. Text, transcriptions and data: CC BY 4.0. The scanned 1897 book in `data/lm/` is third-party material
under neither licence. See [LICENSE.md](LICENSE.md).
