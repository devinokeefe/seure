"""Known-plaintext aligner: cipher signs against plaintext letters under a fixed key.

A key maps each sign to ONE unit: a letter, a group of 2-4 letters inside a word, a whole word ('[word]') or
null ('_'). Several signs may share a unit (homophones). The aligner finds the cheapest monotone alignment:

  match         the sign takes exactly its key unit                         cost 0
  substitution  the sign takes another unit of 1-3 letters inside a word    cost CSUB + 0.4 per extra letter
  null          the sign takes nothing                                      cost 0.2 if its key value is null,
                                                                            0.4 inside an unread GAP, else CNULL
  skip          a plaintext letter has no sign                              cost CDEL (cheaper at the two ends)
  word code     the sign takes a whole word                                 cost 0 if that is its key value,
                                                                            else CSUB + 1.5

The search is a dynamic programme restricted to a band around the diagonal. build_key.py alternates this
alignment with re-estimating the key (each sign -> its most frequent aligned unit).
"""
import array

CSUB, CNULL, CDEL = 2.0, 2.2, 2.0
INF = 1e18


def setup(words):
    """words (with '#' gap markers) -> (letters, word index per letter, {letter index: word starting there}).
    The entry -1 of the last dict holds the letter positions of the gap markers."""
    gaps = set()
    p = ''.join(w for w in words if w != '#')
    wid = []
    wstart = {}
    for k, w in enumerate(words):
        if w == '#':
            gaps.add(len(wid))
            continue
        wstart[len(wid)] = w
        wid += [k] * len(w)
    wstart[-1] = gaps
    return p, wid, wstart


def align(toks, words, K, band=250, ratio=None, endfree=0.6, startfree=0.6):
    """-> (cost, ops, letters). ops = list of (sign index or None, letter index, move, unit) with move
    'U' unit, 'C' word code, 'N' null, 'D' skipped letter (sign index None)."""
    p, wid, wstart = setup(words)
    n, m = len(toks), len(p)
    if ratio is None:
        ratio = m / n
    gaps = wstart.get(-1, set())
    lo = [0] * (n + 1)
    hi = [0] * (n + 1)
    for i in range(n + 1):
        jc = i * ratio
        lo[i] = max(0, int(jc - band))
        hi[i] = min(m, int(jc + band))
    lo[0] = 0
    hi[n] = m
    D = [array.array('d', [INF]) * (hi[i] - lo[i] + 1) for i in range(n + 1)]
    B = [array.array('b', [0]) * (hi[i] - lo[i] + 1) for i in range(n + 1)]   # 1 skip, 2 null, 10+k unit, 20+k code
    D[0][0] = 0.0
    for i in range(n + 1):
        Di = D[i]
        Bi = B[i]
        li = lo[i]
        if i < n:
            Dn = D[i + 1]
            Bn = B[i + 1]
            ln = lo[i + 1]
            hn = hi[i + 1]
            s = toks[i]
            ks = K.get(s)
        for j in range(li, hi[i] + 1):
            cur = Di[j - li]
            if cur >= INF:
                continue
            if j < m and j + 1 <= hi[i]:                                   # skip a plaintext letter
                c = cur + (CDEL if 0 < i < n else (endfree if i == n else startfree))
                if c < Di[j + 1 - li]:
                    Di[j + 1 - li] = c
                    Bi[j + 1 - li] = 1
            if i == n:
                continue
            if ln <= j <= hn:                                               # null
                c = cur + (0.2 if ks == '_' else (0.4 if j in gaps else CNULL))
                if c < Dn[j - ln]:
                    Dn[j - ln] = c
                    Bn[j - ln] = 2
            for k in (1, 2, 3, 4):                                          # unit of k letters inside a word
                if j + k > m or wid[j + k - 1] != wid[j]:
                    break
                if j + k > hn:
                    break
                if j + k < ln:
                    continue
                u = p[j:j + k]
                if ks == u:
                    c = cur
                elif s == '?':
                    c = cur + 1.0 + 0.3 * (k - 1)
                elif k <= 3:
                    c = cur + CSUB + 0.4 * (k - 1)
                else:
                    continue
                if c < Dn[j + k - ln]:
                    Dn[j + k - ln] = c
                    Bn[j + k - ln] = 10 + k
            if j in wstart:                                                 # whole word
                w = wstart[j]
                k = len(w)
                if k >= 2 and j + k <= m and ln <= j + k <= hn:
                    c = cur + (0 if ks == '[' + w + ']' else CSUB + 1.5)
                    if c < Dn[j + k - ln]:
                        Dn[j + k - ln] = c
                        Bn[j + k - ln] = 20 + k
    i, j = n, m
    ops = []
    cost = D[n][m - lo[n]]
    while i > 0 or j > 0:
        b = B[i][j - lo[i]]
        if b == 1:
            ops.append((None, j - 1, 'D', p[j - 1]))
            j -= 1
        elif b == 2:
            ops.append((i - 1, j, 'N', '_'))
            i -= 1
        elif 10 < b < 20:
            k = b - 10
            ops.append((i - 1, j - k, 'U', p[j - k:j]))
            i -= 1
            j -= k
        elif b > 20:
            k = b - 20
            ops.append((i - 1, j - k, 'C', '[' + wstart[j - k] + ']'))
            i -= 1
            j -= k
        else:
            raise RuntimeError(f'no alignment path at sign {i}, letter {j}: the band is too narrow')
    ops.reverse()
    return cost, ops, p


def matches(toks, ops, K):
    """number of signs aligned to exactly their key value"""
    return sum(1 for ti, pj, op, u in ops if ti is not None and K.get(toks[ti]) == u)


def listing(toks, ops, K, label_of):
    """Alignment as text lines 'label: sign=unit ...'; '!' marks a unit that is not the key value,
    '(-x)' a plaintext letter with no sign. label_of(sign index) -> line label."""
    out = []
    cur = None
    buf = []
    for ti, pj, op, u in ops:
        if ti is not None and label_of(ti) != cur:
            if buf:
                out.append(' '.join(buf))
            cur = label_of(ti)
            buf = [cur + ':']
        if ti is None:
            if not buf:
                buf = ['start:']            # plaintext letters skipped before the first sign
            buf.append(f'(-{u})')
        else:
            buf.append(f'{toks[ti]}={u}' + ('' if K.get(toks[ti]) == u else '!'))
    if buf:
        out.append(' '.join(buf))
    return out
