"""Held-out accuracy of the decoder on block C (the postscript of the letter of 12 December 1558).

Block C survives in three separately enciphered copies (letter 41 fo. 77r, letter 43 fo. 82r, letter 44 fo. 86r)
and has a contemporary decipher (fo. 85v). It is never used to build the key. Here each copy is decoded blind:
key = the training alignments only, language model = without the text of block C. The decode is then compared
with the true plaintext.

    python code/build_key.py            (first: writes results/align_<set>.txt)
    python code/heldout.py              character accuracy and word-class precision; writes results/heldout.txt
    python code/heldout.py --update none n5maj n5orig n5all     the same with the key updates from NAF 6638 N. 5

Character accuracy = 1 - edit distance(decoded letters, true letters) / number of true letters (spaces ignored).
Word classes: see decoder.py (support bin S1/S2/S3 x stable/unstable across LM weights 0.3, 0.4, 0.5).
"""
import argparse
import collections
import os

import common as C
import decoder as D


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--update', nargs='+', default=['none'], choices=D.UPDATES)
    ap.add_argument('--beam', type=int, default=300)
    ap.add_argument('--procs', type=int, default=min(9, os.cpu_count() or 1))
    ap.add_argument('--keydir', default='results', help='folder with the align_<set>.txt files of build_key.py')
    ap.add_argument('--out', default='results/heldout.txt')
    a = ap.parse_args()
    held = [s for s in C.load_sets() if s.role == 'heldout']
    toks = {s.tag: C.read_tokens(s.cipher)[0] for s in held}
    truth = {s.tag: ''.join(w for w in C.plain_words(s.plain) if w != '#') for s in held}
    cnt = {u: D.updated_counts(u, include_heldout=False, outdir=a.keydir) for u in a.update}
    jobs = [((s.tag, u), toks[s.tag], cnt[u], False, lmw, a.beam) for u in a.update for s in held for lmw in D.LMWS]
    outs = {(name, lmw): out for name, lmw, sc, out in D.run_jobs(jobs, a.procs)}
    L = [f'Held-out block C: {len(held)} copies, {sum(len(t) for t in toks.values())} signs; key from the training '
         f'alignments in {a.keydir}/ only; language model without block C; beam {a.beam}.']
    for u in a.update:
        S = D.strong(cnt[u])
        L += ['', f'== key update: {u}', 'character accuracy',
              f'{"set":6s} {"file":16s} {"signs":>5s} {"letters":>7s}  ' + '  '.join(f'lmw {l}' for l in D.LMWS)]
        acc = collections.defaultdict(dict)
        for s in held:
            for lmw in D.LMWS:
                flat = D.flat(outs[((s.tag, u), lmw)])
                acc[s.tag][lmw] = 1 - C.edit_distance(flat, truth[s.tag]) / len(truth[s.tag])
            L.append(f'{s.tag:6s} {C.stem(s.cipher[0]):16s} {len(toks[s.tag]):5d} {len(truth[s.tag]):7d}  '
                     + '  '.join(f'{acc[s.tag][l]:7.3f}' for l in D.LMWS))
        L.append(f'{"mean":6s} {"":16s} {"":5s} {"":7s}  '
                 + '  '.join(f'{sum(acc[s.tag][l] for s in held) / len(held):7.3f}' for l in D.LMWS))
        bins = collections.defaultdict(lambda: [0, 0])
        decs = []
        for s in held:
            spans = {l: D.word_spans(toks[s.tag], outs[((s.tag, u), l)], S) for l in D.LMWS}
            cl = D.classify(spans)
            tot = sum(len(w) for w, *_ in cl)
            pos = 0
            for w, sup, stable, i, j in cl:
                if len(w) >= 2:
                    ok = D.word_found(w, pos, tot, truth[s.tag])
                    k = (D.support_bin(sup), 'stable' if stable else 'unstable')
                    for kk in (k, ('all', k[1]), ('all', 'all')):
                        bins[kk][0] += ok
                        bins[kk][1] += 1
                pos += len(w)
            decs.append(f'{s.tag} lmw 0.4: ' + ' '.join(w for w, *_ in cl))
        L += ['', 'word classes (decode at LM weight 0.4; words of 2 letters or more; right = the word occurs within 25',
              'characters of its proportional position in the true text)', f'{"class":14s} right/words  precision']
        keys = D.CLASSES + [('all', 'stable'), ('all', 'unstable'), ('all', 'all')]
        for k in keys:
            g, n = bins[k]
            name = 'all words' if k == ('all', 'all') else k[0] + ' ' + k[1]
            L.append(f'{name:14s} {g:5d}/{n:<5d}  {g / max(1, n):.2f}')
        L += ['', 'decodes'] + decs
        if u == 'none':
            with open(C.P(D.CLASS_FILE), 'w', encoding='utf8', newline='\n') as f:
                f.write('% Word-class precision on held-out block C (code/heldout.py, no key update). '
                        'Columns: support bin, stability, right, words.\n')
                for k in keys:
                    f.write(f'{k[0]}\t{k[1]}\t{bins[k][0]}\t{bins[k][1]}\n')
    with open(C.P(a.out), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
