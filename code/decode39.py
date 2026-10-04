"""Decode letter 39 (BnF ms. fr. 3151, fo. 71r), for which no contemporary decipher is known.

    python code/build_key.py     (first: writes results/align_<set>.txt)
    python code/heldout.py       (first, optional: writes the word-class precisions used below)
    python code/decode39.py                                 the decode recorded in docs/LETTER39.md, section 2
    python code/decode39.py --update n5orig --beam 400      with the key values revised from NAF 6638 N. 5
    python code/decode39.py --cipher data/fr3151/cipher/39_f71r_alt.txt

Key = counts from all alignments (held-out block C included), optionally updated; language model = Nicot
correspondence + the plaintexts of letters 40 and 44 (block C included); decodes at LM weights 0.3, 0.4, 0.5.

The output is a MACHINE decode. It is not the reading proposed in docs/LETTER39.md, which also rests on a sign-by-sign
check of competing readings (score_reading.py) and on judgment. The script ends by checking and tallying that
proposed reading (data/fr3151/letter39_reading.tsv).
"""
import argparse
import collections
import os

import common as C
import decoder as D

READING = 'data/fr3151/letter39_reading.tsv'
GRADE_GROUPS = [('H', ('H', 'H-M')), ('M', ('M', 'M-H')), ('L', ('L', 'L-M', 'M-L'))]
TARGET = {'H': 0.85, 'M': 0.6, 'L': 0.3}


def class_precisions():
    prec = {}
    if os.path.exists(C.P(D.CLASS_FILE)):
        with open(C.P(D.CLASS_FILE), encoding='utf8') as f:
            for raw in f:
                if raw.startswith('%') or not raw.strip():
                    continue
                a, b, g, n = raw.split('\t')
                prec[(a, b)] = int(g) / max(1, int(n))
    return prec


def tally_reading(lines):
    """Check that the spans of the reading table tile the transcription, and count words by grade."""
    start = {}
    o = 0
    for k, line in enumerate(lines, 1):
        start[k] = o
        o += len(line)
    total = o

    def pos(x):
        ln, k = x[1:].split('.')
        assert int(k) < len(lines[int(ln) - 1]), x
        return start[int(ln)] + int(k)

    nxt = 0
    words = collections.Counter()
    signs = collections.Counter()
    spans = collections.Counter()
    with open(C.P(READING), encoding='utf8') as f:
        for raw in f:
            if raw.startswith('%') or not raw.strip():
                continue
            a, b, status, reading, n, grade = raw.rstrip('\n').split('\t')
            i, j = pos(a), pos(b)
            assert i == nxt and j >= i, f'the spans do not tile the transcription at {a}'
            nxt = j + 1
            signs[status] += j - i + 1
            spans[status] += 1
            if status == 'read':
                g = [name for name, members in GRADE_GROUPS if grade in members]
                assert len(g) == 1, grade
                words[g[0]] += int(n)
    assert nxt == total, 'the spans do not reach the end of the transcription'
    return words, signs, spans, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cipher', default=C.LETTER39)
    ap.add_argument('--update', default='none', choices=D.UPDATES)
    ap.add_argument('--beam', type=int, default=300)
    ap.add_argument('--procs', type=int, default=min(3, os.cpu_count() or 1))
    ap.add_argument('--keydir', default='results')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    lines, labels = C.read_lines(a.cipher, labels=True)
    toks = [t for line in lines for t in line]
    starts = []
    o = 0
    for line in lines:
        starts.append(o)
        o += len(line)

    def loc(i):
        j = max(j for j in range(len(starts)) if starts[j] <= i)
        return f'{labels[j]}.{i - starts[j]}'

    cnt = D.updated_counts(a.update, include_heldout=True, outdir=a.keydir)
    S = D.strong(cnt)
    res = D.run_jobs([('39', toks, cnt, True, lmw, a.beam) for lmw in D.LMWS], a.procs)
    outs = {lmw: (sc, out) for name, lmw, sc, out in res}
    spans = {l: D.word_spans(toks, outs[l][1], S) for l in D.LMWS}
    cl = D.classify(spans)
    prec = class_precisions()
    L = [f'Letter 39, {a.cipher}: {len(toks)} signs in {len(lines)} lines. Key: all alignments in {a.keydir}/, '
         f'update {a.update}. Language model with block C. Beam {a.beam}.',
         f'Signs without a key value: {sorted(set(t for t in toks if t not in cnt)) or "none"}', '',
         '== machine decodes (words as divided by the decoder; nulls omitted)']
    for l in D.LMWS:
        L.append(f'LM weight {l} (score {outs[l][0]:.1f}): ' + ' '.join(w for w, *_ in spans[l]))
    L += ['', '== words of the decode at LM weight 0.4',
          'word           support class        held-out precision of the class   signs (line.sign, counted from 0)']
    comp = collections.Counter()
    for w, sup, stable, i, j in cl:
        k = (D.support_bin(sup), 'stable' if stable else 'unstable')
        if len(w) >= 2:
            comp[k] += 1
        p = f'{prec[k]:.2f}' if k in prec else ' n/a'
        L.append(f'{w:14s} {sup:4.2f}    {k[0]} {k[1]:8s}  {p}   {loc(i)}-{loc(j - 1)}  ' + ' '.join(toks[i:j]))
    n = sum(comp.values())
    L += ['', f'== classes of the {n} decoded words of 2 letters or more (LM weight 0.4)']
    for k in D.CLASSES:
        L.append(f'{k[0]} {k[1]:8s} {comp[k]:3d}' + (f'   held-out precision {prec[k]:.2f}' if k in prec else ''))
    if prec:
        e = sum(comp[k] * prec[k] for k in D.CLASSES)
        L.append(f'If the held-out precisions carried over to this letter, {e:.1f} of the {n} words ({e / n:.2f}) would be '
                 'right. They are an upper bound here (docs/LETTER39.md).')
    L += ['', '== sign by sign, LM weight 0.4 ("|" = end of a word, "_" = null)']
    for lab, s0, line in zip(labels, starts, lines):
        out = outs[0.4][1][s0:s0 + len(line)]
        L.append(f'{lab} ' + ' '.join(f'{t}={u.strip() or "_"}{"|" if u.endswith(" ") else ""}' for t, u in zip(line, out)))
    if a.cipher == C.LETTER39:
        words, signs, nspans, total = tally_reading(lines)
        nw = sum(words.values())
        exp = sum(words[g] * TARGET[g] for g in TARGET)
        L += ['', f'== proposed reading ({READING}): the spans tile all {total} signs',
              f'signs: {signs["read"]} in read spans, {signs["null"]} taken as nulls, {signs["unread"]} unread '
              f'({nspans["unread"]} spans)',
              f'words read: {nw}; graded H or H-M {words["H"]}, M or M-H {words["M"]}, L, L-M or M-L {words["L"]}',
              f'under the intended meaning of the grades (H about {TARGET["H"]}, M about {TARGET["M"]}, L about '
              f'{TARGET["L"]}) about {exp:.1f} of the {nw} words would be right ({exp / nw:.2f}); the grades are '
              'judgment, not measurement']
    out = a.out or ('results/letter39_decode' + ('' if a.update == 'none' else '_' + a.update)
                    + ('' if a.cipher == C.LETTER39 else '_' + C.stem(a.cipher)) + '.txt')
    with open(C.P(out), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))
    print(f'\nwritten: {out}')


if __name__ == '__main__':
    main()
