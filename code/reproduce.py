"""Regenerate the figures quoted in README.md and docs/ from the data, and compare them with the documented values.

    python code/reproduce.py            run every step (15 to 30 minutes on a desktop computer), then compare
    python code/reproduce.py --check    compare only, from the result files already in results/
    python code/reproduce.py --only key heldout      run only the named steps, then compare

Steps (each is an ordinary script that can also be run by itself; see code/README.md):
    key       build_key.py                         the key from the known plaintext
    seed      build_key.py with another seed       how far the key depends on the starting key
    heldout   heldout.py                           blind decode of the held-out block C
    decode39  decode39.py (twice)                  machine decode of letter 39, without and with the revised values
    tests     score_reading.py                     competing readings of spans of letter 39
    readers   compare_readers.py                   agreement of the two transcriptions of letter 39
    keyfit    keyfit_control.py                    does the key fit letter 39 at all
    naf       naf6638_check.py                     NAF 6638 cipher blocks against the copy's clear text

The table printed at the end is also written to results/reproduce_summary.txt. Exit status 1 if a figure differs.
"""
import argparse
import os
import re
import subprocess
import sys
import time

import common as C

STEPS = [
    ('key', [['build_key.py']]),
    ('seed', [['build_key.py', '--seed', 'data/key/seed_letter40.tsv', '--out', 'results/seed_letter40']]),
    ('heldout', [['heldout.py', '--update', 'none', 'n5maj', 'n5orig', 'n5all']]),
    ('decode39', [['decode39.py'], ['decode39.py', '--update', 'n5orig', '--beam', '400']]),
    ('tests', [['score_reading.py']]),
    ('readers', [['compare_readers.py']]),
    ('keyfit', [['keyfit_control.py']]),
    ('naf', [['naf6638_check.py']]),
]


def rx(pattern, fmt=None, flags=re.S):
    def f(text):
        m = re.search(pattern, text, flags)
        if not m:
            return 'not found'
        return fmt.format(*m.groups()) if fmt else ' / '.join(m.groups())
    return f


def block(start, inner, fmt=None):
    """apply a pattern inside the part of the file that begins with the line containing 'start' and runs to the next
    line that begins with '==' or '##'"""
    def f(text):
        i = text.find(start)
        if i < 0:
            return 'not found'
        j = re.search(r'\n(==|##)', text[i + len(start):])
        part = text[i:i + len(start) + j.start()] if j else text[i:]
        return rx(inner, fmt)(part)
    return f


def test_score(section, reading, column):
    """score (emission + 0.4 LM) of a reading in results/letter39_tests.txt; column 0-3 = none, n5maj, n5orig, n5all"""
    pat = re.escape(repr(reading)) + r'\s+-?[\d.]+' + r'\s+-?[\d.]+ /\s+(-?[\d.]+)[* ]' * 4
    return block('## ' + section, pat, '{%d}' % column)


B, H, D39, T, R, K, N = ('results/build_log.txt', 'results/heldout.txt', 'results/letter39_decode.txt',
                         'results/letter39_tests.txt', 'results/letter39_readers.txt', 'results/keyfit_control.txt',
                         'results/naf6638_check.txt')
ACC = r'{}\s+\S*\s+\d*\s+\d*\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
# (figure, value quoted in the documentation, result file, how to read it from the file)
FIGURES = [
    ('KEY', None, None, None),
    ('signs with a key value: training sets / all alignments', '156 / 159', B,
     rx(r'key \(training sets only\): (\d+) signs; key table \(all alignments\): (\d+) signs')),
    ('signs transcribed in letters 40 / 44 / 41 / 43 / 39', '1082 / 1874 / 1883 / 3522 / 405', B,
     rx(r'no\. 40: (\d+), no\. 44: (\d+), no\. 41: (\d+), no\. 43: (\d+), no\. 39: (\d+)')),
    ('signs with known plaintext (letters 40, 41, 43, 44)', '8361', B, rx(r'known plaintext in all: (\d+)')),
    ('key values of high / medium / low confidence', '46 / 30 / 83', B, rx(r'confidence: high (\d+), medium (\d+), low (\d+)')),
    ('alignment cost of the training sets at convergence', '5522.5', B,
     rx(r'training cost ([\d.]+), signs that change value 0')),
    ('other seed (letter-40 key): signs with another value', '10 of 159 signs (214 of 8361 occurrences, 2.6%)',
     'results/seed_letter40/build_log.txt',
     rx(r'compared with data/key/key\.csv: (\d+) of (\d+) signs have another value \((\d+) of (\d+) aligned occurrences, '
        r'([\d.]+%)\)', '{0} of {1} signs ({2} of {3} occurrences, {4})')),
    ('HELD-OUT BLOCK C (decoded blind)', None, None, None),
    ('held-out signs', '1057', H, rx(r'Held-out block C: 3 copies, (\d+) signs')),
    ('character accuracy, LM weight 0.4: 44 C / 41 C / 43 PS / mean', '0.508 / 0.553 / 0.705 / 0.589', H,
     lambda t: ' / '.join(block('== key update: none', ACC.format(s), '{1}')(t) for s in ('HC44', 'HC41', 'HC43', 'mean'))),
    ('mean character accuracy at LM weights 0.3 / 0.4 / 0.5', '0.588 / 0.589 / 0.583', H,
     block('== key update: none', r'mean\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)')),
    ('mean at 0.4 with key updates n5maj / n5orig / n5all', '0.593 / 0.595 / 0.587', H,
     lambda t: ' / '.join(block('== key update: ' + u, r'mean\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', '{1}')(t)
                          for u in ('n5maj', 'n5orig', 'n5all'))),
    ('words right, S1 stable / S2 stable / S3 stable', '51/59 / 21/32 / 37/64', H,
     lambda t: ' / '.join(block('== key update: none', s + r' stable\s+(\d+)/(\d+)', '{0}/{1}')(t) for s in ('S1', 'S2', 'S3'))),
    ('words right, S1 unstable / S2 unstable / S3 unstable', '17/28 / 3/12 / 19/76', H,
     lambda t: ' / '.join(block('== key update: none', s + r' unstable\s+(\d+)/(\d+)', '{0}/{1}')(t) for s in ('S1', 'S2', 'S3'))),
    ('words right, all stable / all unstable / all', '109/155 / 39/116 / 148/271', H,
     lambda t: ' / '.join(block('== key update: none', s + r'\s+(\d+)/(\d+)', '{0}/{1}')(t)
                          for s in ('all stable', 'all unstable', 'all words'))),
    ('LETTER 39', None, None, None),
    ('signs / lines', '405 / 20', D39, rx(r'(\d+) signs in (\d+) lines')),
    ('proposed reading: signs read / taken as nulls / unread', '365 / 4 / 36', D39,
     rx(r'signs: (\d+) in read spans, (\d+) taken as nulls, (\d+) unread')),
    ('proposed reading: words read; graded H / M / L', '100; 45 / 39 / 16', D39,
     rx(r'words read: (\d+); graded H or H-M (\d+), M or M-H (\d+), L, L-M or M-L (\d+)', '{0}; {1} / {2} / {3}')),
    ('words expected right under the meaning of the grades', '66.5 of 100', D39,
     rx(r'about ([\d.]+) of the (\d+) words would be right', '{0} of {1}')),
    ('machine decode: words expected right at held-out precision', '65.1 of 107', D39,
     rx(r'precisions carried over to this letter, ([\d.]+) of the (\d+) words', '{0} of {1}')),
    ('"des musul" / "des gens" (score, key as built)', '-64.8 / -80.1', T,
     lambda t: test_score('retraite des', 'a retraite des musul', 0)(t) + ' / '
     + test_score('retraite des', 'a retraite des gens', 0)(t)),
    ('"la resolucion" / "laredo surin" (main transcription)', '-33.7 / -33.3', T,
     lambda t: test_score('resolution:', 'la resolucion', 0)(t) + ' / ' + test_score('resolution:', 'laredo surin', 0)(t)),
    ('"la resolucion" / "laredo surin" (L08 sign 8 read vl)', '-29.8 / -36.4', T,
     lambda t: test_score('resolution (alt', 'la resolucion', 0)(t) + ' / ' + test_score('resolution (alt', 'laredo surin', 0)(t)),
    ('"et au pis aller": key as built / n5maj / n5orig', '-43.5 / -33.2 / -31.9', T,
     lambda t: ' / '.join(test_score('au pis aller', 'et au pis aller', k)(t) for k in (0, 1, 2))),
    ('"en necessite" / "en une ce di e"', '-26.3 / -41.6', T,
     lambda t: test_score('necessite', 'en necessite', 0)(t) + ' / ' + test_score('necessite', 'en une ce di e', 0)(t)),
    ('two readers, before the comparison: exact / with alternatives', '341/405 = 0.842 / 359/405 = 0.886', R,
     block('== reader 1 (v3) against reader 2', r'exact agreement (\S+ = [\d.]+); agreement counting the alternatives (\S+ = [\d.]+)')),
    ('final transcription against reader 2: exact / with alternatives', '353/405 = 0.872 / 369/405 = 0.911', R,
     block('== final reading (v4) against reader 2', r'exact agreement (\S+ = [\d.]+); agreement counting the alternatives (\S+ = [\d.]+)')),
    ('signs changed after the comparison', '17', R, rx(r'to the final reading \(v4\): (\d+)')),
    ('key fit, letter 44: real; z against shuffled order / permuted key', '-1174.5; 8.6 / 11.3', K,
     rx(r'letter 44, fo\. 84r\s+(-[\d.]+).*?\(z\s+([\d.]+)\).*?\(z\s+([\d.]+)\)', '{0}; {1} / {2}', 0)),
    ('key fit, letter 39: real; z against shuffled order / permuted key', '-1124.3; 14.8 / 11.9', K,
     rx(r'letter 39, fo\. 71r\s+(-[\d.]+).*?\(z\s+([\d.]+)\).*?\(z\s+([\d.]+)\)', '{0}; {1} / {2}', 0)),
    ('NAF 6638', None, None, None),
    ('N. 4: signs; cost; signs on key value; z', '264; 252.5; 162; -23.3', N,
     block('== N. 4', r'(\d+) signs \(.*?real text: cost ([\d.]+); (\d+) of.*?z = (-[\d.]+)', '{0}; {1}; {2}; {3}')),
    ('N. 4: cost range of 14 other windows of the same letter', '369.2 to 383.7', N,
     block('== N. 4', r'cost\s+([\d.]+) to ([\d.]+)', '{0} to {1}')),
    ('N. 5: signs as written; tokens aligned', '4284; 4261', N,
     block('== N. 5', r'(\d+) signs as written.*?-> (\d+) tokens', '{0}; {1}')),
    ('N. 5: words / letters of the clear text', '1143 / 5266', N, block('== N. 5', r'\((\d+) words, (\d+) letters')),
    ('N. 5: cost; tokens on key value', '2856.6; 3088 of 4261 (72.5%)', N,
     block('== N. 5', r'real text: cost ([\d.]+); (\d+ of \d+) tokens on their key value \(([\d.]+%)\)', '{0}; {1} ({2})')),
    ('N. 5: 20 word-shuffles; z', '5887.4 +- 10.8; -280.2', N,
     block('== N. 5', r'word-shuffles: cost ([\d.]+ \+- [\d.]+).*?z = (-[\d.]+)', '{0}; {1}')),
    ('N. 5: cost added by leaving out the footnote of p. 31', '+74.8', N, block('== N. 5', r'without the footnote.*?\((\+[\d.]+)\)')),
    ('N. 5: z per page, weakest / strongest', '-34.4 / -56.9', N,
     lambda t: (lambda z: f'{max(z):.1f} / {min(z):.1f}' if z else 'not found')(
         [float(x) for x in re.findall(r'^p\d+ .*?\+-\s+[\d.]+\s+(-[\d.]+)', t, re.M)])),
    ('Falgairolle variants: douze/onze + mille/mil; Barselonne clause; assez', '+4.4; +41.2; +7.0', N,
     lambda t: '; '.join(rx(p + r'.*?difference (\+[\d.]+)', None, 0)(t)
                         for p in (r'"mille ou douze cens" / "mil ou onze cens"', r'clause "pour envoyer', r'"assez desnuez'))),
]


def compare():
    rows, bad = [], 0
    cache = {}
    for name, doc, path, fn in FIGURES:
        if doc is None:
            rows.append((name, '', '', ''))
            continue
        if path not in cache:
            cache[path] = open(C.P(path), encoding='utf8').read() if os.path.exists(C.P(path)) else None
        got = 'file missing: ' + path if cache[path] is None else fn(cache[path])
        ok = got == doc
        bad += not ok
        rows.append(('  ' + name, doc, got, 'ok' if ok else 'DIFFERS'))
    w = [max(len(r[i]) for r in rows) for i in range(3)]
    L = [f'{"figure":{w[0]}s}  {"documented":{w[1]}s}  {"reproduced":{w[2]}s}', '-' * (sum(w) + 12)]
    L += [f'{a:{w[0]}s}  {b:{w[1]}s}  {c:{w[2]}s}  {d}'.rstrip() for a, b, c, d in rows]
    n = sum(1 for f in FIGURES if f[1] is not None)
    L += ['', f'{n - bad} of {n} figures reproduce' + ('' if not bad else f'; {bad} differ')]
    return L, bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='compare only; run nothing')
    ap.add_argument('--only', nargs='+', choices=[s for s, _ in STEPS], help='run only these steps')
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    if not a.check:
        for name, cmds in STEPS:
            if a.only and name not in a.only:
                continue
            for cmd in cmds:
                t0 = time.time()
                print(f'--- {name}: python code/{" ".join(cmd)}', flush=True)
                r = subprocess.run([sys.executable, os.path.join(here, cmd[0])] + cmd[1:], cwd=C.ROOT,
                                   stdout=subprocess.DEVNULL)
                print(f'    exit status {r.returncode}, {time.time() - t0:.0f} s', flush=True)
                if r.returncode:
                    sys.exit(f'step {name} failed')
    L, bad = compare()
    with open(C.P('results/reproduce_summary.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
