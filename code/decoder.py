"""Decoder: key emission model + character n-gram language model + beam search with word boundaries.

The decoder reads a sequence of sign labels and returns, for each sign, the plaintext unit it most plausibly
stands for (a letter, a letter group, a whole word '[word]' or null '_'), scored by

    log P(sign | unit)  +  lmw * log P_LM(unit | preceding text)

The key model comes from the known-plaintext alignment counts (build_key.py). The language model is trained on
sixteenth-century French diplomatic text (data/lm/) plus the plaintexts of letters 40 and 44.
"""
import collections
import math
import re
import unicodedata

import common as C

_TR = str.maketrans('jvwk', 'iuuc')


# ----------------------------------------------------------------------------------------------- language model
def norm_lm(text, spaces=True):
    """Text -> a-z (and single spaces): accents stripped, lower case, j->i, v->u, w->u, k->c."""
    t = unicodedata.normalize('NFKD', text)
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower().translate(_TR)
    if not spaces:
        return re.sub('[^a-z]', '', t)
    return re.sub(' +', ' ', re.sub('[^a-z]+', ' ', t))


class LM:
    """Interpolated Witten-Bell character n-gram model over a-z, with or without the space."""

    def __init__(self, texts, order=7, spaces=True):
        self.n = order
        self.base = 1.0 / (27 if spaces else 26)
        self.c = [collections.defaultdict(collections.Counter) for _ in range(order)]
        for t in texts:
            for i in range(len(t)):
                for k in range(order):
                    if i - k < 0:
                        break
                    self.c[k][t[i - k:i]][t[i]] += 1
        self.tot = [{h: sum(v.values()) for h, v in ck.items()} for ck in self.c]
        self.typ = [{h: len(v) for h, v in ck.items()} for ck in self.c]
        self.cache = {}

    def p(self, h, ch):
        """log P(ch | history h)"""
        h = h[-(self.n - 1):] if self.n > 1 else ''
        key = (h, ch)
        r = self.cache.get(key)
        if r is not None:
            return r
        pr = self.base
        for k in range(0, len(h) + 1):
            hh = h[len(h) - k:] if k else ''
            ck = self.c[k].get(hh)
            if ck is None:
                break
            T = self.tot[k][hh]
            N = self.typ[k][hh]
            lam = T / (T + N)
            pr = lam * ck[ch] / T + (1 - lam) * pr
        r = math.log(pr)
        self.cache[key] = r
        return r

    def score(self, h, s):
        """-> (log P(s | h), new history)"""
        tot = 0.0
        for ch in s:
            tot += self.p(h, ch)
            h = (h + ch)[-(self.n - 1):]
        return tot, h


def lm_texts(with_block_c, spaces=True, seure=True):
    """Training texts: the Nicot correspondence (OCR), and, if seure, the decipher of letter 40 and the 12 Dec 1558
    letter (without its postscript, block C, unless with_block_c). Block C is the held-out test text, so it must
    stay out of the model whenever the held-out blocks are decoded."""
    with open(C.P(C.LM_CORPUS), encoding='utf8') as f:
        texts = [norm_lm(f.read(), spaces)]
    if seure:
        clean = lambda t: t.replace('[?]', ' ').replace('GAP', ' ')
        seg = C.segments()
        texts.append(norm_lm(clean(C.plain_text(C.PLAIN_40)), spaces))
        texts.append(norm_lm(clean(' '.join(seg[t] for t in ('CLEAR0', 'CLEAR1', 'A', 'CLEAR2', 'B', 'CLEAR3'))), spaces))
        if with_block_c:
            texts.append(norm_lm(clean(seg['C']), spaces))
    return texts


def make_lm(with_block_c, order=7):
    return LM(lm_texts(with_block_c), order)


# ----------------------------------------------------------------------------------------------- key model
class KeyModel:
    """Emission model from alignment counts cnt[sign][unit].

    P(sign | unit) = (count + alpha) / (count of the unit over all signs + alpha * (number of signs + 1)).
    A sign with fewer than minev aligned occurrences may also stand for any single letter (probability bo);
    a sign with no known-plaintext occurrence may stand for any letter or null (probability unk)."""

    def __init__(self, cnt, bo=0.003, minev=8, alpha=0.3, unk=0.02):
        self.cnt = cnt
        self.ucnt = collections.Counter()
        for c in cnt.values():
            for u, n in c.items():
                self.ucnt[u] += n
        self.nsyms = len(cnt)
        self.alpha, self.bo, self.minev, self.unk = alpha, bo, minev, unk

    def cands(self, sym):
        """-> list of (unit, log P(sign | unit))"""
        out = []
        if sym in self.cnt:
            tot = sum(self.cnt[sym].values())
            for u, n in self.cnt[sym].items():
                out.append((u, math.log((n + self.alpha) / (self.ucnt[u] + self.alpha * (self.nsyms + 1)))))
            if tot < self.minev:
                for l in C.LETTERS:
                    if l not in self.cnt[sym]:
                        out.append((l, math.log(self.bo)))
        else:
            for l in C.LETTERS:
                out.append((l, math.log(self.unk)))
            out.append(('_', math.log(self.unk)))
        return out


def decode(tokens, key, lm, lmw=0.4, beam=300, code_pen=-3.0):
    """Beam search with word boundaries. -> (score, LM history, units), one unit per sign; a unit that ends a
    word carries a trailing space; '_' is a null; '[word]' a word code."""
    hyps = [(0.0, ' ', ())]
    for s in tokens:
        new = {}
        cands = key.cands(s)
        for sc, h, out in hyps:
            for u, le in cands:
                if u == '_':
                    opts = [(sc + le, h, out + ('_',))]
                elif u.startswith('['):
                    w = u.strip('[]')
                    a, nh = lm.score(h if h.endswith(' ') else h + ' ', w + ' ')
                    a0 = 0.0 if h.endswith(' ') else lm.p(h, ' ')
                    opts = [(sc + le + code_pen + lmw * (a + a0), nh, out + (u,))]
                else:
                    a, nh = lm.score(h, u)
                    base = sc + le + lmw * a
                    opts = [(base, nh, out + (u,))]
                    sp = lm.p(nh, ' ')
                    opts.append((base + lmw * sp, (nh + ' ')[-(lm.n - 1):], out + (u + ' ',)))
                for ns, nh2, o2 in opts:
                    if nh2 not in new or new[nh2][0] < ns:      # recombine hypotheses with the same LM history
                        new[nh2] = (ns, nh2, o2)
        hyps = sorted(new.values(), key=lambda x: -x[0])[:beam]
    return hyps[0]


def decode_nospace(tokens, key, lm, lmw=0.4, beam=200, code_pen=-3.0, wild_pen=-3.5):
    """The earlier decoder without word boundaries (LM over a-z only); used by keyfit_control.py.
    An unreadable sign '?' may stand for any letter (wild_pen) or for nothing (wild_pen - 2)."""
    hyps = [(0.0, '', ())]
    for s in tokens:
        new = {}
        cands = key.cands(s) if s != '?' else [(l, wild_pen) for l in C.LETTERS] + [('_', wild_pen - 2)]
        for sc, h, out in hyps:
            for u, le in cands:
                if u == '_':
                    ns, nh, unit = sc + le, h, '_'
                elif u.startswith('['):
                    ns, nh, unit = sc + le + code_pen, h, u
                else:
                    a, nh = lm.score(h, u)
                    ns, unit = sc + le + lmw * a, u
                if nh not in new or new[nh][0] < ns:
                    new[nh] = (ns, nh, out + (unit,))
        hyps = sorted(new.values(), key=lambda x: -x[0])[:beam]
    return hyps[0]


def flat(units):
    """decoded units -> plain letter string (no nulls, no spaces, word codes spelled out)"""
    return ''.join(u.strip('[] ') for u in units if u != '_')


# ----------------------------------------------------------------------------------------------- word classes
def strong(cnt):
    """sign -> (main value, is_strong). Strong = at least 6 aligned occurrences and at least 60% on the main value."""
    S = {}
    for s, c in cnt.items():
        u, n = c.most_common(1)[0]
        tot = sum(c.values())
        S[s] = (u, tot >= 6 and n / tot >= 0.6)
    return S


def word_spans(toks, units, S):
    """-> [(word, support, first sign index, end sign index)]. Support = share of the word's letters that come
    from a strong sign decoded to its main value (i.e. letters not supplied by the language model)."""
    res = []
    cur = ''
    sup = 0
    n = 0
    st = None

    def flush(end):
        nonlocal cur, sup, n, st
        if cur:
            res.append((cur, sup / max(1, n), st, end))
        cur = ''
        sup = 0
        n = 0
        st = None

    for i, (t, u) in enumerate(zip(toks, units)):
        if u == '_':
            continue
        if u.startswith('['):
            flush(i)
            ok = S.get(t, ('', False))
            res.append((u.strip('[] '), 1.0 if ok[1] and ok[0] == u.strip() else 0.0, i, i + 1))
            continue
        if st is None:
            st = i
        uu = u.strip()
        ok = S.get(t, ('', False))
        good = ok[1] and ok[0] == uu
        cur += uu
        sup += len(uu) * good
        n += len(uu)
        if u.endswith(' '):
            flush(i + 1)
    flush(len(toks))
    return res


def support_bin(s):
    return 'S1' if s >= 0.99 else ('S2' if s >= 0.75 else 'S3')


def classify(spans_by_lmw, main=0.4):
    """spans_by_lmw: {lmw: word_spans(...)} -> [(word, support, stable, start, end)] for the main LM weight.
    Stable = the decodes at the other LM weights give the same word over the same signs."""
    others = [set((w, a, b) for w, s, a, b in spans) for l, spans in spans_by_lmw.items() if l != main]
    return [(w, s, all((w, a, b) in o for o in others), a, b) for w, s, a, b in spans_by_lmw[main]]


def word_found(word, pos, total, truth, window=25):
    """Is the decoded word present within +-window characters of its proportional position in the true text?"""
    est = pos * len(truth) / max(1, total)
    lo = max(0, int(est) - window)
    hi = min(len(truth), int(est) + len(word) + window)
    return word in truth[lo:hi]


# ----------------------------------------------------------------------------------------------- key updates
UPDATE_FILE = 'data/key/naf6638_n5_values.tsv'
UPDATES = ('none', 'n5maj', 'n5orig', 'n5all')


def n5_counts(majority_only):
    """Counts for the nine signs whose value was re-read from the NAF 6638 N. 5 known plaintext."""
    add = collections.defaultdict(collections.Counter)
    with open(C.P(UPDATE_FILE), encoding='utf8') as f:
        for raw in f:
            if raw.startswith('%') or not raw.strip():
                continue
            sign, unit, n, maj = raw.rstrip('\n').split('\t')
            if maj == '1' or not majority_only:
                add[sign][unit] += int(n)
    return add


def counts_with_artefacts_fixed(paths):
    """Alignment counts with two artefacts of the fr. 3151 alignments corrected (diagnosed by the NAF 6638 text):
    mt=a followed by a skipped u, or by a sign forced off-key to u...   -> mt=au (the neighbour loses its u);
    A=ur preceded by a sign forced off-key to 'po' (or by a skipped o)  -> A=[pour] (the neighbour's po is dropped)."""
    cnt = collections.defaultdict(collections.Counter)
    nfix = collections.Counter()
    for path in paths:
        with open(C.P(path), encoding='utf8') as f:
            for line in f:
                if line.startswith('%'):
                    continue
                raw = line.split()[1:]
                units = C.parse_align_line(line)
                for k, x in enumerate(units):
                    if x is None:
                        continue
                    if x[0] == 'mt' and x[1] == 'a' and k + 1 < len(raw):
                        y = units[k + 1]
                        if raw[k + 1].startswith('(-u'):
                            x[1] = 'au'
                            nfix['mt a->au (skipped u)'] += 1
                        elif y and y[2] and y[1].startswith('u'):
                            x[1] = 'au'
                            y[1] = y[1][1:] or None
                            nfix['mt a->au (forced u)'] += 1
                    if x[0] == 'A' and x[1] == 'ur' and k > 0:
                        y = units[k - 1]
                        if (y and y[2] and y[1] == 'po') or raw[k - 1].startswith('(-o'):
                            x[1] = '[pour]'
                            nfix['A ur->[pour]'] += 1
                            if y and y[1] == 'po':
                                y[1] = None
                for x in units:
                    if x and x[1] is not None:
                        cnt[x[0]][x[1]] += 1
    return cnt, nfix


def updated_counts(update='none', include_heldout=True, outdir='results'):
    """Key counts from the alignment listings, optionally updated from the NAF 6638 N. 5 known plaintext:
    none    the fr. 3151 key as built by build_key.py
    n5maj   + the N. 5 count of the majority value of the nine re-read signs
    n5orig  n5maj, with the two alignment artefacts corrected in the fr. 3151 counts
    n5all   + every N. 5 unit aligned to those nine signs"""
    tags = sorted(s.tag for s in C.load_sets() if include_heldout or s.role == 'train')
    paths = [C.align_path(t, outdir) for t in tags]
    if update == 'n5orig':
        cnt, _ = counts_with_artefacts_fixed(paths)
    else:
        cnt = C.counts_from_align(paths)
    if update != 'none':
        merged = collections.defaultdict(collections.Counter)
        for s, c in cnt.items():
            merged[s].update(c)
        for s, c in n5_counts(majority_only=(update != 'n5all')).items():
            merged[s].update(c)
        cnt = merged
    return cnt


# ----------------------------------------------------------------------------------------------- parallel decoding
_LM_CACHE = {}


def decode_job(args):
    """(name, signs, counts, with_block_c, lmw, beam) -> (name, lmw, score, units). The language model is built once
    per worker process."""
    name, toks, cnt, with_block_c, lmw, beam = args
    if with_block_c not in _LM_CACHE:
        _LM_CACHE[with_block_c] = make_lm(with_block_c)
    sc, h, out = decode(toks, KeyModel(cnt), _LM_CACHE[with_block_c], lmw, beam)
    return name, lmw, sc, out


def run_jobs(jobs, procs):
    import multiprocessing as mp
    with mp.Pool(max(1, min(procs, len(jobs)))) as pool:
        return pool.map(decode_job, jobs, chunksize=1)


LMWS = (0.3, 0.4, 0.5)
CLASSES = [('S1', 'stable'), ('S2', 'stable'), ('S3', 'stable'), ('S1', 'unstable'), ('S2', 'unstable'), ('S3', 'unstable')]
CLASS_FILE = 'results/heldout_classes.tsv'
