"""Rebuild the key from the known plaintext (letters 40, 41, 43, 44 of BnF ms. fr. 3151).

Method ("hard EM" with a consistent key): starting from a seed key, repeat
  1. align every known-plaintext set with its plaintext under the current key (aligner.py);
  2. give each sign the unit it was aligned to most often (training sets only);
until no sign changes value. The held-out sets (block C in its three copies) are aligned with the final key but
never counted while the key is being built.

    python code/build_key.py                       seed data/key/seed_previous_pass.tsv, output in results/
    python code/build_key.py --publish             the same, and refresh data/key/key.csv, key.json and the doc tables
    python code/build_key.py --seed data/key/seed_letter40.tsv --out results/seed_letter40
                                                   alternative seed; prints how the resulting key differs

Output (in --out): align_<set>.txt (sign=unit listings), key_train.tsv (training counts), key.csv / key.json
(counts over all alignments, held-out included, as tabulated in docs/KEY.md), build_log.txt.
"""
import argparse
import collections
import csv
import json
import multiprocessing as mp
import os
import shutil

import aligner
import common as C

LETTER_SETS = {'40': ['40'], '44': ['44A', '44B', 'HC44'], '41': ['41A', '41B', 'HC41'], '43': ['43m', 'HC43']}
REVISED = 'data/key/revised_values.tsv'
DESCRIPTIONS = 'data/key/sign_descriptions.tsv'


def _align(args):
    toks, words, K, band, ratio, endfree = args
    cost, ops, _ = aligner.align(toks, words, K, band, ratio, endfree)
    return cost, ops


def confidence(n, tot):
    if tot >= 8 and n / tot >= 0.75:
        return 'high'
    if tot >= 4 and n / tot >= 0.6:
        return 'medium'
    return 'low'


def load_two_columns(path):
    out = collections.OrderedDict()
    if os.path.exists(C.P(path)):
        with open(C.P(path), encoding='utf8') as f:
            for raw in f:
                if raw.startswith('%') or not raw.strip():
                    continue
                v = raw.rstrip('\n').split('\t')
                out[v[0]] = v[1:]
    return out


def build(seed, outdir, iters, procs, log):
    sets = C.load_sets()
    data = []
    for s in sets:
        toks, origin = C.read_tokens(s.cipher)
        data.append((s, toks, origin, C.plain_words(s.plain)))
    K = C.load_key(seed)
    log(f'seed {seed}: {len(K)} signs; {len(sets)} sets, '
        f'{sum(len(d[1]) for d in data)} signs ({sum(len(d[1]) for d in data if d[0].role == "train")} for training)')
    converged = False
    with mp.Pool(min(procs, len(data))) as pool:
        for it in range(iters):
            res = pool.map(_align, [(toks, words, K, s.band, s.ratio, s.endfree) for s, toks, origin, words in data])
            cnt = collections.defaultdict(collections.Counter)
            train_cost = 0.0
            per = []
            for (s, toks, origin, words), (cost, ops) in zip(data, res):
                per.append(f'{s.tag}:{cost:.1f}/{aligner.matches(toks, ops, K)}/{len(toks)}')
                if s.role != 'train':
                    continue
                train_cost += cost
                for ti, pj, op, u in ops:
                    if ti is not None:
                        cnt[toks[ti]][u] += 1
            K2 = dict(K)
            K2.update({s: c.most_common(1)[0][0] for s, c in cnt.items()})
            changed = sum(1 for s in cnt if K2[s] != K.get(s))
            log(f'iteration {it}: training cost {train_cost:.1f}, signs that change value {changed}')
            log('   set:cost/signs on their key value/signs  ' + ' '.join(per))
            if changed == 0:
                converged = True
                break
            K = K2
    if not converged:
        log(f'NOT converged after {iters} iterations')
    os.makedirs(C.P(outdir), exist_ok=True)
    with open(C.P(f'{outdir}/key_train.tsv'), 'w', encoding='utf8', newline='\n') as f:
        f.write('% Key from the training sets only (held-out block C not counted). Columns: sign, value, occurrences on '
                'the value / all aligned occurrences, distribution of aligned units.\n')
        for s, c in sorted(cnt.items(), key=lambda x: -sum(x[1].values())):
            f.write(f'{s}\t{K[s]}\t{c[K[s]]}/{sum(c.values())}\t' + ' '.join(f'{u}:{n}' for u, n in c.most_common()) + '\n')
    for (s, toks, origin, words), (cost, ops) in zip(data, res):
        stems = [C.stem(p) for p in s.cipher]
        lines = aligner.listing(toks, ops, K, lambda i: f'{stems[origin[i][0]]}.{origin[i][1]}')
        with open(C.P(C.align_path(s.tag, outdir)), 'w', encoding='utf8', newline='\n') as f:
            f.write(f'% set {s.tag} ({s.role}): {len(toks)} signs against {sum(len(w) for w in words if w != "#")} '
                    f'letters; cost {cost:.1f}; {aligner.matches(toks, ops, K)} signs on their key value.\n'
                    '% sign=unit per sign ("_" = null, "[word]" = word code); "!" = the unit is not the key value of the '
                    'sign; "(-x)" = plaintext letter x has no sign.\n')
            f.write('\n'.join(lines) + '\n')
    return K, cnt, data


def key_table(outdir, data):
    """rows of the documented key table: counts over ALL alignments (training + held-out)"""
    cnt = C.key_counts(outdir)
    occ = {}
    by_tag = {s.tag: toks for s, toks, origin, words in data}
    for letter, tags in LETTER_SETS.items():
        occ[letter] = collections.Counter(t for tag in tags for t in by_tag[tag])
    occ['39'] = collections.Counter(C.read_tokens(C.LETTER39)[0])
    revised = load_two_columns(REVISED)
    rows = []
    for s, c in sorted(cnt.items(), key=lambda x: -sum(x[1].values())):
        u, n = c.most_common(1)[0]
        tot = sum(c.values())
        rows.append(dict(sign=s, value=u, n_value=n, n_total=tot, confidence=confidence(n, tot),
                         n40=occ['40'][s], n44=occ['44'][s], n41=occ['41'][s], n43=occ['43'][s], n39=occ['39'][s],
                         distribution=' '.join(f'{x}:{m}' for x, m in c.most_common()),
                         revised_value=revised.get(s, ['', ''])[0], revision_basis=revised.get(s, ['', ''])[1]))
    return rows, occ


def write_key_files(rows, outdir):
    cols = ['sign', 'value', 'n_value', 'n_total', 'confidence', 'n40', 'n44', 'n41', 'n43', 'n39', 'distribution',
            'revised_value', 'revision_basis']
    with open(C.P(f'{outdir}/key.csv'), 'w', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, cols, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    js = collections.OrderedDict()
    for r in rows:
        d = collections.OrderedDict((k, r[k]) for k in cols[1:10])
        d['distribution'] = collections.OrderedDict((x.rsplit(':', 1)[0], int(x.rsplit(':', 1)[1]))
                                                    for x in r['distribution'].split())
        if r['revised_value']:
            d['revised_value'] = r['revised_value']
            d['revision_basis'] = r['revision_basis']
        js[r['sign']] = d
    with open(C.P(f'{outdir}/key.json'), 'w', encoding='utf8', newline='\n') as f:
        json.dump(js, f, ensure_ascii=False, indent=1)
        f.write('\n')


def md_key_table(rows, occ):
    B = '`'
    inv = collections.defaultdict(list)
    for r in rows:
        if r['confidence'] != 'low':
            inv[r['value']].append(f'{B}{r["sign"]}{B} ({r["n_value"]}/{r["n_total"]})')
    L = ['### Short key', '', '| plaintext | signs |', '|---|---|']
    for u in sorted(inv, key=lambda x: (len(x.strip('[]_')) > 1, x)):
        L.append(f'| {u} | {", ".join(inv[u])} |')
    L += ['', '### Full table', '',
          '| sign | value | evidence | conf | other alignments | n40 | n44 | n41 | n43 | n39 |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append(f'| {B}{r["sign"]}{B} | {r["value"]} | {r["n_value"]}/{r["n_total"]} | {r["confidence"]} | '
                 f'{r["distribution"]} | {r["n40"]} | {r["n44"]} | {r["n41"]} | {r["n43"]} | {r["n39"]} |')
    seen = set(r['sign'] for r in rows)
    new = sorted(set(occ['39']) - seen)
    L += ['', 'Signs that occur in letter 39 but in no known-plaintext alignment (no key value): '
          + (', '.join(f'{B}{s}{B}' for s in new) or 'none') + '.']
    return '\n'.join(L)


def md_sign_table(rows, occ):
    B = '`'
    desc = load_two_columns(DESCRIPTIONS)
    kd = {r['sign']: r for r in rows}
    labs = sorted(set().union(*[set(c) for c in occ.values()]), key=lambda s: -sum(c[s] for c in occ.values()))
    L = ['| label | description | key value (evidence) | n40 | n44 | n41 | n43 | n39 |', '|---|---|---|---|---|---|---|---|']
    for s in labs:
        kv = f'{kd[s]["value"]} ({kd[s]["n_value"]}/{kd[s]["n_total"]})' if s in kd else '-'
        d = desc.get(s, ['(no description recorded)'])[0]
        L.append(f'| {B}{s}{B} | {d} | {kv} | {occ["40"][s]} | {occ["44"][s]} | {occ["41"][s]} | {occ["43"][s]} | {occ["39"][s]} |')
    return '\n'.join(L), len(labs)


def replace_between(path, name, text, log):
    a, b = f'<!-- {name}:start (generated by code/build_key.py --publish) -->', f'<!-- {name}:end -->'
    if not os.path.exists(C.P(path)):
        log(f'{path}: not found, table {name} not written')
        return
    with open(C.P(path), encoding='utf8') as f:
        s = f.read()
    if a not in s or b not in s:
        log(f'{path}: markers for {name} not found, table not written')
        return
    s = s[:s.index(a) + len(a)] + '\n' + text + '\n' + s[s.index(b):]
    with open(C.P(path), 'w', encoding='utf8', newline='\n') as f:
        f.write(s)
    log(f'{path}: table {name} refreshed')


def compare_with_published(rows, log):
    path = 'data/key/key.csv'
    if not os.path.exists(C.P(path)):
        return
    with open(C.P(path), encoding='utf8', newline='') as f:
        old = {r['sign']: r for r in csv.DictReader(f)}
    new = {r['sign']: r for r in rows}
    diff = [s for s in new if s in old and old[s]['value'] != new[s]['value']]
    only = sorted(set(new) ^ set(old))
    tot = sum(int(r['n_total']) for r in old.values())
    w = sum(int(old[s]['n_total']) for s in diff)
    log(f'compared with {path}: {len(diff)} of {len(old)} signs have another value '
        f'({w} of {tot} aligned occurrences, {w / tot:.1%}); signs in one table only: {only or "none"}')
    for s in diff:
        log(f'   {s}: {old[s]["value"]} ({old[s]["n_value"]}/{old[s]["n_total"]}) -> '
            f'{new[s]["value"]} ({new[s]["n_value"]}/{new[s]["n_total"]})')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--seed', default='data/key/seed_previous_pass.tsv')
    ap.add_argument('--out', default='results')
    ap.add_argument('--iters', type=int, default=12)
    ap.add_argument('--procs', type=int, default=min(9, os.cpu_count() or 1))
    ap.add_argument('--publish', action='store_true',
                    help='copy key.csv and key.json to data/key/ and refresh the tables of docs/KEY.md and docs/SYMBOLS.md')
    a = ap.parse_args()
    lines = []

    def log(x):
        print(x, flush=True)
        lines.append(x)

    K, cnt, data = build(a.seed, a.out, a.iters, a.procs, log)
    rows, occ = key_table(a.out, data)
    per_letter = {k: sum(v.values()) for k, v in occ.items()}
    log(f'key (training sets only): {len(cnt)} signs; key table (all alignments): {len(rows)} signs')
    log('signs per letter: ' + ', '.join(f'no. {k}: {v}' for k, v in per_letter.items())
        + f'; known plaintext in all: {sum(v for k, v in per_letter.items() if k != "39")}')
    log('confidence: ' + ', '.join(f'{c} {sum(1 for r in rows if r["confidence"] == c)}' for c in ('high', 'medium', 'low')))
    if not a.publish:
        compare_with_published(rows, log)
    write_key_files(rows, a.out)
    if a.publish:
        for f in ('key.csv', 'key.json'):
            shutil.copyfile(C.P(f'{a.out}/{f}'), C.P(f'data/key/{f}'))
        log('data/key/key.csv and data/key/key.json refreshed')
        replace_between('docs/KEY.md', 'key-table', md_key_table(rows, occ), log)
        t, n = md_sign_table(rows, occ)
        replace_between('docs/SYMBOLS.md', 'sign-table', t, log)
        log(f'sign labels in letters 39, 40, 41, 43, 44: {n}')
    with open(C.P(f'{a.out}/build_log.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
