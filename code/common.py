"""Shared file handling for the Seure 1558 scripts.

All paths are relative to the repository root (the folder that contains code/, data/, docs/).
The scripts can be started from any working directory.
"""
import collections
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = 'data/sets.tsv'
TEXT_12DEC = 'data/fr3151/plain/12dec1558_text.tsv'
PLAIN_40 = 'data/fr3151/plain/40_decipher_f74r.txt'
LM_CORPUS = 'data/lm/nicot_falgairolle_1897_ocr.txt'
LETTER39 = 'data/fr3151/cipher/39_f71r.txt'
LETTERS = 'abcdefghilmnopqrstuxyz'      # plaintext alphabet after normalisation (j->i, v->u, w->u, k->c)


def P(rel):
    """repository-relative path (with forward slashes) -> absolute path"""
    return rel if os.path.isabs(rel) else os.path.join(ROOT, *rel.split('/'))


def rel(path):
    """absolute path -> repository-relative path with forward slashes (for log lines)"""
    return os.path.relpath(path, ROOT).replace(os.sep, '/')


# ----------------------------------------------------------------------------------------------- cipher
_LINE_LABEL = re.compile(r'\s*(L\d+)\b')


def read_lines(path, labels=False):
    """Transcription file -> list of manuscript lines, each a list of sign labels.
    '%' starts a comment; blank and comment-only lines are skipped. With labels=True also returns the line labels:
    the 'Lnn' that opens the comment of the line if there is one, else the running number of the line in the file."""
    out, labs = [], []
    with open(P(path), encoding='utf8') as f:
        for raw in f:
            left, _, right = raw.partition('%')
            t = left.split()
            if not t:
                continue
            m = _LINE_LABEL.match(right)
            out.append(t)
            labs.append(m.group(1) if m else f'L{len(out):02d}')
    return (out, labs) if labels else out


def read_tokens(paths):
    """One file or a list of files -> (tokens, origin) with origin[i] = (file index, line label) of sign i."""
    if isinstance(paths, str):
        paths = [paths]
    toks, origin = [], []
    for k, path in enumerate(paths):
        lines, labs = read_lines(path, labels=True)
        for line, lab in zip(lines, labs):
            toks += line
            origin += [(k, lab)] * len(line)
    return toks, origin


def stem(path):
    """'data/fr3151/cipher/44_f84v.txt' -> '44_f84v'"""
    return os.path.splitext(os.path.basename(path))[0]


def parse_reading(tok):
    """Reading with uncertainty marks -> (labels, uncertain).
    'a' -> (['a'], False); 'a?' -> (['a'], True); 'a?|b' -> (['a', 'b'], True). A lone '?' is a label.
    Only used for the second-reader file of letter 39 and for the NAF 6638 files. In the fr. 3151 known-plaintext
    files a trailing '?' is part of the label (oo?, 8?, cc?, c?, p?, t?; see docs/SYMBOLS.md)."""
    parts = tok.split('|')
    unc = len(parts) > 1
    alts = []
    for k, a in enumerate(parts):
        if a.endswith('?') and len(a) > 1:
            a = a[:-1]
            if k == 0:
                unc = True
        alts.append(a)
    return alts, unc


# ----------------------------------------------------------------------------------------------- plaintext
_TR = str.maketrans('jvwk', 'iuuc')


def norm_word(w):
    """Plaintext word -> letters a-z only: accents stripped, lower case, j->i, v->u, w->u, k->c."""
    w = ''.join(ch for ch in unicodedata.normalize('NFD', w) if unicodedata.category(ch) != 'Mn')
    return re.sub('[^a-z]', '', w.lower().translate(_TR))


def words_of(text):
    """Plaintext -> normalised words. Words containing '?' (uncertain readings of the decipher sheet) are dropped;
    the word GAP (an unread stretch of the decipher sheet) becomes the gap marker '#'."""
    out = []
    for line in text.split('\n'):
        for w in line.split('%')[0].split():
            if '?' in w:
                continue
            if w == 'GAP':
                out.append('#')
                continue
            w = norm_word(w)
            if w:
                out.append(w)
    return out


def segments(path=TEXT_12DEC):
    """Segment file (TAG<TAB>text per line, '%' comments) -> ordered dict TAG -> text."""
    seg = collections.OrderedDict()
    with open(P(path), encoding='utf8') as f:
        for raw in f:
            if raw.startswith('%') or not raw.strip():
                continue
            tag, text = raw.rstrip('\n').split('\t', 1)
            seg[tag] = text
    return seg


def strip_comments(text):
    return '\n'.join(line.split('%')[0] for line in text.split('\n'))


def plain_text(selector):
    """'path' -> the file's text without comments; 'path#A+B' -> segments A and B of a segment file, joined."""
    if '#' in selector:
        path, tags = selector.split('#')
        seg = segments(path)
        return ' '.join(seg[t] for t in tags.split('+'))
    with open(P(selector), encoding='utf8') as f:
        return strip_comments(f.read())


def plain_words(selector):
    return words_of(plain_text(selector))


# ----------------------------------------------------------------------------------------------- sets
Set = collections.namedtuple('Set', 'tag role cipher plain band ratio endfree')


def load_sets(path=SETS):
    """data/sets.tsv -> list of Set. role is 'train' or 'heldout'."""
    out = []
    with open(P(path), encoding='utf8') as f:
        for raw in f:
            if raw.startswith('%') or not raw.strip():
                continue
            tag, role, cipher, plain, band, ratio, endfree = raw.rstrip('\n').split('\t')
            out.append(Set(tag, role, cipher.split(','), plain, int(band),
                           None if ratio == '-' else float(ratio), float(endfree)))
    return out


# ----------------------------------------------------------------------------------------------- key files
def load_key(path):
    """TSV with sign<TAB>value in the first two columns -> dict. Lines starting with '%' are comments
    ('#' cannot be the comment mark: it is a sign label)."""
    K = {}
    with open(P(path), encoding='utf8') as f:
        for raw in f:
            if raw.startswith('%') or not raw.strip():
                continue
            v = raw.rstrip('\n').split('\t')
            K[v[0]] = v[1]
    return K


def align_path(tag, outdir='results'):
    return f'{outdir}/align_{tag}.txt'


def parse_align_line(line):
    """One line of an alignment listing -> list of ops: None for a skipped plaintext letter '(-x)',
    else [sign, unit, forced] where forced is True if the unit is not the key value (marked '!')."""
    ops = []
    for op in line.split()[1:]:
        if op.startswith('(-'):
            ops.append(None)
            continue
        s, u = op.rsplit('=', 1)
        ops.append([s, u.rstrip('!'), u.endswith('!')])
    return ops


def counts_from_align(paths):
    """Alignment listings -> counts[sign][unit] (unit '_' = null, '[word]' = word code)."""
    cnt = collections.defaultdict(collections.Counter)
    for path in paths:
        with open(P(path), encoding='utf8') as f:
            for line in f:
                if line.startswith('%'):
                    continue
                for op in parse_align_line(line):
                    if op is not None:
                        cnt[op[0]][op[1]] += 1
    return cnt


def key_counts(outdir='results', include_heldout=True):
    """Counts from the alignment listings written by build_key.py, in a fixed (sorted-tag) order."""
    tags = sorted(s.tag for s in load_sets() if include_heldout or s.role == 'train')
    return counts_from_align([align_path(t, outdir) for t in tags])


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]
