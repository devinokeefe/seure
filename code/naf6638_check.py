"""BnF ms. NAF 6638: are the two cipher blocks of February 1559 enciphered versions of the clear text that the
copy itself gives after the first block?

NAF 6638 is a 19th-century copy of two letters of Seure (St Petersburg, National Library of Russia, ms. 110). The
copyist drew the cipher signs of two blocks ("N. 4", p. 29, 264 signs; "N. 5", pp. 35-43) and copied the clear text.
This script aligns each block with the clear text of pp. 29-34 under a FIXED key from BnF fr. 3151 (nothing is
learned from NAF 6638) and compares the alignment cost with that of the same text with its words shuffled.

    python code/build_key.py           (first: the N. 5 test uses the key of results/align_<set>.txt)
    python code/naf6638_check.py       writes results/naf6638_check.txt and results/align_N5.txt

N. 4: key from letter 40 alone (data/key/seed_letter40.tsv), as the test was first made.
N. 5: the final key (each sign = its most frequent unit over all alignments of fr. 3151).
"""
import collections
import multiprocessing as mp
import os
import random
import re
import statistics as st

import aligner
import common as C

N4 = 'data/naf6638/cipher/N4_p29.txt'
N5 = ['data/naf6638/cipher/N5_p35-36.txt', 'data/naf6638/cipher/N5_p37-39.txt', 'data/naf6638/cipher/N5_p40-43.txt']
COPY = 'data/naf6638/plain/copy_p29-34.txt'
N4_AFTER = 'data/naf6638/plain/copy_p29_after_N4_first_reading.txt'
N4_BEFORE = 'data/naf6638/plain/copy_p28-29_before_N4.txt'
SEED40 = 'data/key/seed_letter40.tsv'
# the letter-40 key was made before these sign classes were split
UNSPLIT = {'8p': '8', 'po': 'p', 'cl': 'cc', 'ts': 't'}
# N. 5, structural edits applied when the three files are joined (the files themselves keep what is written):
# DROP: the copyist wrote 26 signs twice (p. 41 line 28 signs 1-13 and line 29 = p. 41 line 30 and p. 42 line 0 signs
#   0-11); the second copy is dropped. Entries: (page, line, from sign, to sign), (page, line, sign) of the first copy.
# INSERT: three clear words written in the copy's text hand between cipher signs: (page, line, after sign, word,
#   reading of that sign as a check).
DROP = [((41, 30, 0, 14), (41, 28, 1)), ((42, 0, 0, 12), (41, 29, 1))]
INSERT = [(41, 8, 12, 'pour', 'ooo'), (43, 13, 9, 'po~', 'Phi?|oo'), (43, 14, 2, 'pour', 'c')]
CLEAR_WORDS = {'pour': '[pour]', 'po~': '[pour]'}
# the provisional labels NEW1, NEW2, ... name different shapes in different files
RENAME = {1: {'NEW1': 'NEW1a', 'NEW2': 'NEW2a', 'NEW3': 'NEW3a'}, 2: {'NEW1': 'NEW1b', 'NEW2': 'NEW2b'}}
# readings of Falgairolle's printed text (1895) that differ from the copy: (label, words of the copy, words printed)
VARIANTS = [
    ('"mille ou douze cens" / "mil ou onze cens"', ['mille', 'ou', 'douze', 'cens'], ['mil', 'ou', 'onze', 'cens']),
    ('   of which douze / onze alone', ['mille', 'ou', 'douze', 'cens'], ['mille', 'ou', 'onze', 'cens']),
    ('   of which mille / mil alone', ['mille', 'ou', 'douze', 'cens'], ['mil', 'ou', 'douze', 'cens']),
    ('clause "pour envoyer hors d\'Espaigne ... a Barselonne" present / omitted',
     ['barselonne', 'pour', 'enuoyer', 'hors', 'despaigne', 'quant', 'a', 'celluy', 'que', 'on', 'porte', 'a', 'barselonne'],
     ['barselonne']),
    ('"ne trouveront gueres" / "ne trouverons gueres"', ['ne', 'trouueront', 'gueres'], ['ne', 'trouuerons', 'gueres']),
    ('"sans soy guieres" / "sans ny gueres"', ['sans', 'soy', 'guieres'], ['sans', 'ny', 'gueres']),
    ('"ilz pourroient desmollir" / "ilz porront desmollir"', ['ilz', 'pourroient', 'desmollir'], ['ilz', 'porront', 'desmollir']),
    ('"assez desnuez d\'hommes" / "desnuez d\'hommes"', ['assez', 'desnuez', 'dhommes'], ['desnuez', 'dhommes']),
]
NSHUF = 20


# ----------------------------------------------------------------------------------------------- reading the files
def first(tok):
    return C.parse_reading(tok)[0][0]


def read_block(path, k):
    """-> records {tok, page, line, idx}; the page comes from the comment lines '% p. NN'"""
    out = []
    page, line, last = None, -1, None
    with open(C.P(path), encoding='utf8') as f:
        for raw in f:
            m = re.match(r'\s*%\s*p\.\s*(\d+)', raw)
            if m:
                page = int(m.group(1))
                continue
            t = raw.split('%')[0].split()
            if not t:
                continue
            if page != last:
                line, last = 0, page
            else:
                line += 1
            for i, x in enumerate(t):
                parts = []
                for p in x.split('|'):
                    q = p.rstrip('?')
                    parts.append(RENAME.get(k, {}).get(q, q) + p[len(q):])
                out.append(dict(tok='|'.join(parts), page=page, line=line, idx=i))
    return out


def n5_records(log):
    recs = []
    for k, path in enumerate(N5):
        recs += read_block(path, k)
    raw = len(recs)
    pos = {(r['page'], r['line'], r['idx']): i for i, r in enumerate(recs)}
    drop = set()
    for (pg, ln, a, b), (pg1, ln1, a1) in DROP:
        i0 = pos[(pg1, ln1, a1)]
        second = [pos[(pg, ln, k)] for k in range(a, b)]
        agree = sum(1 for k, i in enumerate(second)
                    if set(C.parse_reading(recs[i0 + k]['tok'])[0]) & set(C.parse_reading(recs[i]['tok'])[0]))
        assert agree >= 0.8 * len(second), 'the two copies of the dittography do not match'
        drop.update(second)
        log.append(f'  dropped p{pg} line {ln} signs {a}-{b - 1}: second copy of a dittography '
                   f'({agree} of {len(second)} readings share a label with the first copy)')
    ins = {(pg, ln, k): (w, chk) for pg, ln, k, w, chk in INSERT}
    out = []
    for i, r in enumerate(recs):
        if i in drop:
            continue
        out.append(r)
        key = (r['page'], r['line'], r['idx'])
        if key in ins:
            w, chk = ins[key]
            assert r['tok'] == chk, ('insert anchor', key, r['tok'])
            out.append(dict(tok=w, page=r['page'], line=r['line'], idx=f'{r["idx"]}+', clear=True))
            log.append(f'  inserted the clear word "{w}" after p{key[0]} line {key[1]} sign {key[2]}')
    return out, raw


def copy_words(footnote=True):
    """Clear text of the copy -> [(word, page, line)]; hyphenated words joined; the footnote of p. 31 inserted at
    its reference mark if footnote."""
    lines, fn = [], []
    page, ln = None, 0
    with open(C.P(COPY), encoding='utf8') as f:
        for raw in f:
            m = re.match(r'%\s*---\s*p\.\s*(\d+)', raw)
            if m:
                page, ln = int(m.group(1)), 0
                continue
            if raw.startswith('% FN31:'):
                fn.append(raw[len('% FN31:'):].strip())
                continue
            t = raw.split('%')[0].strip()
            if not t or page is None:
                continue
            lines.append([page, ln, t])
            ln += 1
    if footnote:
        ftxt = ' '.join(fn).lstrip('* ').strip()
        for x in lines:
            if x[0] == 31 and '*' in x[2]:
                x[2] = x[2].replace('*', ' ' + ftxt + ' ')
    W, carry = [], None
    for pg, ln, t in lines:
        toks = t.replace('*', ' ').split()
        for k, w in enumerate(toks):
            if carry is not None:
                w, pg0, ln0 = carry[0] + w.lstrip('='), carry[1], carry[2]
                carry = None
            else:
                pg0, ln0 = pg, ln
            if k == len(toks) - 1 and w.endswith('='):
                carry = (w.rstrip('='), pg0, ln0)
                continue
            nw = C.norm_word(w)
            if nw:
                W.append((nw, pg0, ln0))
    return W


def n5_plain(footnote=True):
    W = copy_words(footnote)
    i0 = [i for i, (w, pg, ln) in enumerate(W) if pg == 29 and w == 'napporte'][0]
    return W[i0:]


# ----------------------------------------------------------------------------------------------- alignment jobs
def job(args):
    name, toks, words, K, band, ratio, endfree, startfree, want_ops = args
    cost, ops, p = aligner.align(toks, words, K, band, ratio, endfree, startfree)
    return name, cost, aligner.matches(toks, ops, K), ops if want_ops else None


def run(jobs):
    with mp.Pool(min(len(jobs), max(1, (os.cpu_count() or 2) - 1), 16)) as pool:
        return {r[0]: r[1:] for r in pool.map(job, jobs, chunksize=1)}


def shuffled(words, seed):
    w = words[:]
    random.Random(seed).shuffle(w)
    return w


def zline(real, costs):
    mu, sd = st.mean(costs), st.pstdev(costs)
    return mu, sd, (real - mu) / sd


def main():
    L = ['NAF 6638: known-plaintext tests of the two cipher blocks against the clear text of the copy.',
         'cost = alignment cost under a fixed key (lower = better fit); z = (real - mean of the word-shuffled controls) / '
         'their standard deviation']
    # ---------------------------------------------------------------- N. 4
    K40 = C.load_key(SEED40)
    t4 = [UNSPLIT.get(first(t), first(t)) for line in C.read_lines(N4) for t in line]
    unc4 = sum(1 for line in C.read_lines(N4) for t in line if '?' in t and len(t) > 1)
    after = C.plain_words(N4_AFTER)
    before = C.plain_words(N4_BEFORE)
    n_after = sum(map(len, after))
    r4 = n_after / len(t4) * 0.75
    jobs = [('n4', t4, after, K40, 200, r4, 0.0, 0.6, False)]
    jobs += [(('n4s', s), t4, shuffled(after, s), K40, 200, r4, 0.0, 0.6, False) for s in range(NSHUF)]
    offs = []
    for off in range(0, len(before), 12):
        w, n = [], 0
        for x in before[off:]:
            w.append(x)
            n += len(x)
            if n >= n_after:
                break
        if n < n_after * 0.95:
            break
        offs.append(off)
        jobs.append((('n4o', off), t4, w, K40, 200, n / len(t4) * 0.75, 0.0, 0.6, False))
    # ---------------------------------------------------------------- N. 5
    log = []
    recs, raw = n5_records(log)
    t5 = [first(r['tok']) for r in recs]
    W = n5_plain(True)
    words = [w for w, pg, ln in W]
    cnt = C.key_counts('results')
    K = {s: c.most_common(1)[0][0] for s, c in cnt.items()}
    K.update(CLEAR_WORDS)
    w0 = [w for w, pg, ln in n5_plain(False)]
    jobs.append(('n5', t5, words, K, 400, None, 0.0, 0.6, True))
    jobs.append(('n5nofn', t5, w0, K, 400, None, 0.0, 0.6, False))
    jobs += [(('n5s', s), t5, shuffled(words, s), K, 400, None, 0.0, 0.6, False) for s in range(NSHUF)]

    def find(sub):
        for i in range(len(words) - len(sub) + 1):
            if words[i:i + len(sub)] == sub:
                return i
        raise ValueError(sub)

    for k, (lab, a, b) in enumerate(VARIANTS):
        i = find(a)
        jobs.append((('n5v', k), t5, words[:i] + b + words[i + len(a):], K, 400, None, 0.0, 0.6, False))
    R = run(jobs)
    # ---------------------------------------------------------------- report N. 4
    c4, m4, _ = R['n4']
    sh = [R[('n4s', s)][0] for s in range(NSHUF)]
    mu, sd, z = zline(c4, sh)
    oth = [R[('n4o', o)][0] for o in offs]
    L += ['', f'== N. 4 (p. 29): {len(t4)} signs ({unc4} marked uncertain) against the clear text that follows the block '
          f'({n_after} letters, {len(after)} words; the plaintext may run on past the cipher). Key: letter 40 alone.',
          f'real text: cost {c4:.1f}; {m4} of {len(t4)} signs on their key value ({m4 / len(t4):.0%})',
          f'{NSHUF} word-shuffles of the same text: cost {mu:.1f} +- {sd:.1f} (lowest {min(sh):.1f}); z = {z:.1f}',
          f'{len(oth)} windows of equal length from the clear text BEFORE the block (same letter, same subject): cost '
          f'{min(oth):.1f} to {max(oth):.1f}']
    # ---------------------------------------------------------------- report N. 5
    c5, m5, ops = R['n5']
    sh = [R[('n5s', s)][0] for s in range(NSHUF)]
    mu, sd, z = zline(c5, sh)
    nclear = sum(1 for r in recs if r.get('clear'))
    L += ['', f'== N. 5 (pp. 35-43): {raw} signs as written'] + log + [
        f'  -> {len(t5)} tokens ({len(t5) - nclear} cipher signs and {nclear} clear words) against the clear text from '
        f'"n\'apporte" (p. 29) to the end of p. 34 ({len(words)} words, {sum(map(len, words))} letters, footnote of p. 31 '
        'inserted at its mark). Key: final key from fr. 3151.',
        f'real text: cost {c5:.1f}; {m5} of {len(t5)} tokens on their key value ({m5 / len(t5):.1%})',
        f'{NSHUF} word-shuffles: cost {mu:.1f} +- {sd:.1f} (lowest {min(sh):.1f}; on key value '
        f'{st.mean(R[("n5s", s)][1] for s in range(NSHUF)):.0f}); z = {z:.1f}',
        f'without the footnote of p. 31: cost {R["n5nofn"][0]:.1f} ({R["n5nofn"][0] - c5:+.1f}): the cipher contains the '
        'footnote text']
    lp = []
    for k, (w, pg, ln) in enumerate(W):
        lp += [(pg, ln, k)] * len(w)
    al = [(ti, pj, u) for ti, pj, op, u in ops if ti is not None and u != '_']
    firstj = min(pj for ti, pj, u in al)
    lastj = max(pj + len(u.strip('[]')) for ti, pj, u in al)
    nD = sum(1 for ti, pj, op, u in ops if op == 'D' and firstj <= pj < lastj)
    nN = sum(1 for ti, pj, op, u in ops if op == 'N')
    nNk = sum(1 for ti, pj, op, u in ops if op == 'N' and K.get(t5[ti]) == '_')
    L.append(f'coverage: letters {firstj}-{lastj} of {len(lp)} aligned (from "{words[lp[firstj][2]]}" to '
             f'"{words[lp[lastj - 1][2]]}"); {nD} letters without a sign; {nN} tokens aligned to nothing ({nNk} of them '
             'signs whose key value is null)')
    tail = []
    for ti, pj, op, u in reversed(ops):
        if ti is None:
            continue
        if op != 'N':
            break
        tail.append(recs[ti]['tok'])
    L.append(f'the last {len(tail)} signs of the block have no plaintext: ' + ' '.join(reversed(tail)))
    # per page
    tokpj = {ti: (pj, len(u.strip('[]')) if u != '_' else 0) for ti, pj, op, u in ops if ti is not None}
    pages = sorted(set(r['page'] for r in recs))
    jobs, meta = [], {}
    for pg in pages:
        idx = [i for i, r in enumerate(recs) if r['page'] == pg]
        a, b = idx[0], idx[-1] + 1
        js = [tokpj[i][0] for i in range(a, b) if tokpj[i][1] > 0]
        je = [tokpj[i][0] + tokpj[i][1] for i in range(a, b) if tokpj[i][1] > 0]
        wa, wb = lp[min(js)][2], lp[max(je) - 1][2] + 1
        seg, t = words[wa:wb], t5[a:b]
        meta[pg] = (b - a, sum(map(len, seg)), W[wa], W[wb - 1])
        jobs.append((('pg', pg), t, seg, K, 300, None, 0.6, 0.6, False))
        jobs += [(('pgs', pg, s), t, shuffled(seg, 1000 + s), K, 300, None, 0.6, 0.6, False) for s in range(NSHUF)]
    R2 = run(jobs)
    L += ['', f'per page of the cipher (signs of the page against the stretch of text the whole-block alignment gives it; '
          f'{NSHUF} word-shuffles of that stretch)',
          'page  tokens  letters  text (copy page.line)                                real   shuffled        z   on key value']
    for pg in pages:
        n, nl, wa, wb = meta[pg]
        rc, rm, _ = R2[('pg', pg)]
        sh = [R2[('pgs', pg, s)][0] for s in range(NSHUF)]
        mu, sd, z = zline(rc, sh)
        span = f'p{wa[1]}.{wa[2]:02d} "{wa[0]}" - p{wb[1]}.{wb[2]:02d} "{wb[0]}"'
        L.append(f'p{pg}   {n:5d}   {nl:5d}   {span:46s} {rc:7.1f}  {mu:6.1f} +- {sd:4.1f}  {z:6.1f}   {rm}/{n}')
    L += ['', 'variants of the text printed by Falgairolle (1895) against the copy: cost with the copy\'s words / with the '
          'printed words (positive difference = the cipher fits the copy better)']
    for k, (lab, a, b) in enumerate(VARIANTS):
        c = R[('n5v', k)][0]
        L.append(f'{lab}: {c5:.1f} / {c:.1f}, difference {c - c5:+.1f}')
    with open(C.P('results/naf6638_check.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    lines = aligner.listing([r['tok'] for r in recs], ops, {r['tok']: K.get(first(r['tok'])) for r in recs},
                            lambda i: f'p{recs[i]["page"]}.L{recs[i]["line"]:02d}')
    with open(C.P('results/align_N5.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('% NAF 6638 N. 5 against the clear text of the copy, fixed key from fr. 3151. sign (full reading)=unit; "!" = '
                'not the key value of the first reading; "(-x)" = plaintext letter with no sign. Lines of the page from 0.\n')
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
