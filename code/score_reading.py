"""Score competing readings of a span of letter 39 against the signs and the language model.

    score = emission + 0.4 * LM
    emission = log P(signs | reading) under the key model, for the best division of the reading into the units the
               signs stand for (letters, letter groups, word signs, nulls)
    LM       = log probability of the reading under the character language model

Higher (less negative) is better. A difference of a few units is not decisive; see docs/LETTER39.md.

    python code/build_key.py        (first)
    python code/score_reading.py    all the tests of data/fr3151/letter39_tests.tsv, for every key variant;
                                    writes results/letter39_tests.txt
    python code/score_reading.py --span L16.14-L17.3 "et au pis aller" "et a pis aller"
                                    one span (line.sign counted from 0, both ends inclusive), readings in normalised
                                    letters (u for v, i for j); [word] = a word written with one word sign
"""
import argparse
import math
import re

import common as C
import decoder as D

TESTS = 'data/fr3151/letter39_tests.tsv'
LMW = 0.4


def emission(key, span, reading):
    """-> (log P(span | reading) for the best segmentation, segmentation as text)"""
    s = re.findall(r'\[[a-z]+\]|[a-z]', reading)
    n, m = len(span), len(s)
    NEG = -1e9
    floor = math.log(1e-4)
    best = [[NEG] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(n):
        c = dict(key.cands(span[i]))
        for j in range(m + 1):
            if best[i][j] <= NEG / 2:
                continue
            v = best[i][j]
            x = v + c.get('_', floor)
            if x > best[i + 1][j]:
                best[i + 1][j] = x
                back[i + 1][j] = (j, '_')
            for k in range(1, 5):
                if j + k > m:
                    break
                if any(y.startswith('[') for y in s[j:j + k]) and k > 1:
                    break
                u = ''.join(s[j:j + k])
                lp = c.get(u, floor if (k == 1 and not u.startswith('[')) else None)
                if lp is None:
                    continue
                if v + lp > best[i + 1][j + k]:
                    best[i + 1][j + k] = v + lp
                    back[i + 1][j + k] = (j, u)
    seg = []
    j = m
    for i in range(n, 0, -1):
        if back[i][j] is None:
            break
        pj, u = back[i][j]
        seg.append(f'{span[i - 1]}={u}')
        j = pj
    return best[n][m], ' '.join(seg[::-1])


def span_tokens(cipher, span):
    lines, labels = C.read_lines(cipher, labels=True)
    start = {}
    o = 0
    for lab, line in zip(labels, lines):
        start[lab] = o
        o += len(line)
    toks = [t for line in lines for t in line]

    def pos(x):
        lab, k = x.split('.')
        return start[lab] + int(k)

    a, b = span.split('-')
    return toks[pos(a):pos(b) + 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('readings', nargs='*')
    ap.add_argument('--span')
    ap.add_argument('--cipher', default=C.LETTER39)
    ap.add_argument('--update', nargs='+', default=list(D.UPDATES), choices=D.UPDATES)
    ap.add_argument('--keydir', default='results')
    ap.add_argument('--out', default='results/letter39_tests.txt')
    a = ap.parse_args()
    if a.span:
        tests = [('command line', a.cipher, a.span, a.readings)]
    else:
        tests = []
        with open(C.P(TESTS), encoding='utf8') as f:
            for raw in f:
                if raw.startswith('%') or not raw.strip():
                    continue
                name, cf, span, cands = raw.rstrip('\n').split('\t')
                tests.append((name, f'data/fr3151/cipher/{cf}.txt', span, cands.split(' | ')))
    keys = {u: D.KeyModel(D.updated_counts(u, include_heldout=True, outdir=a.keydir)) for u in a.update}
    lm = D.make_lm(with_block_c=True)
    L = [f'Scores = emission + {LMW} * LM, per key variant ({", ".join(a.update)}); higher is better; * = best of the '
         'readings tried for that variant. em = emission alone. "impossible" = the signs cannot give the reading',
         'even with off-key single letters (a letter group or word sign is needed that the sign never has).']
    for name, cf, span, cands in tests:
        toks = span_tokens(cf, span)
        L += ['', f'## {name}: {C.stem(cf)} {span}: {" ".join(toks)}',
              f'{"reading":34s} {"LM":>6s}  ' + '  '.join(f'{u + " em / score":>20s}' for u in a.update)]
        sc = {}
        for c in cands:
            lmv, _ = lm.score(' ', c.replace('[', '').replace(']', '') + ' ')
            sc[c] = (lmv, {u: emission(keys[u], toks, c) for u in a.update})
        best = {u: max(cands, key=lambda c: sc[c][1][u][0] + LMW * sc[c][0]) for u in a.update}
        for c in cands:
            lmv, em = sc[c]
            cells = []
            for u in a.update:
                e = em[u][0]
                cells.append(f'{"impossible":>20s}' if e < -1e8 else
                             f'{e:9.1f} / {e + LMW * lmv:7.1f}{"*" if best[u] == c else " "}')
            L.append(f'{c!r:34s} {lmv:6.1f}  ' + '  '.join(cells))
            first = a.update[0]
            if em[first][0] > -1e8:
                L.append(f'      {first}: {em[first][1]}')
    text = '\n'.join(L) + '\n'
    if not a.span:
        with open(C.P(a.out), 'w', encoding='utf8', newline='\n') as f:
            f.write(text)
    print(text)


if __name__ == '__main__':
    main()
