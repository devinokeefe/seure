"""Key-fit control: does a key recovered from letter 40 fit a cipher text whose plaintext is not known?

The test was made at the first stage of the work, with the key from letter 40 alone, and is reproduced here with
the same inputs. The decoder score (key + language model) of the signs in their real order is compared with
  (a) the same signs in shuffled order, and
  (b) the real order decoded with the key's values permuted among the signs.
If the key fits, the real order scores clearly higher than both. Letter 44 (whose decipher confirms that it uses
the key of letter 40) is the positive example; letter 39 is the text in question.

    python code/keyfit_control.py       writes results/keyfit_control.txt

Inputs: data/key/letter40_first_alignment.txt (key counts from letter 40 only); the first 350 signs of letter 44,
fo. 84r, and of letter 39 in its earliest transcription; language model = Nicot correspondence only, letters
without spaces, order 6; LM weight 0.4; beam 200; 6 shuffles (seeds 0-5) and 6 permuted keys (seeds 100-105).
"""
import multiprocessing as mp
import os
import random

import common as C
import decoder as D

ALIGN40 = 'data/key/letter40_first_alignment.txt'
TEXTS = [('letter 44, fo. 84r', 'data/fr3151/cipher/44_f84r.txt'),
         ('letter 39, fo. 71r', 'data/fr3151/cipher/39_f71r_reader1_early.txt')]
NSIGNS, RUNS, LMW, BEAM = 350, 6, 0.4, 200
_LM = []


def signs(path):
    """first signs of the file; the '?' that marks the unsplit classes of letter 44 (oo?, 8?, ...) is dropped,
    because the letter-40 key was made before those classes were split"""
    toks = C.read_tokens(path)[0]
    return [t[:-1] if t.endswith('?') and len(t) > 1 else t for t in toks][:NSIGNS]


def score(args):
    toks, cnt = args
    if not _LM:
        _LM.append(D.LM(D.lm_texts(False, spaces=False, seure=False), order=6, spaces=False))
    return D.decode_nospace(toks, D.KeyModel(cnt), _LM[0], LMW, BEAM)[0]


def stats(v):
    mu = sum(v) / len(v)
    return mu, (sum((x - mu) ** 2 for x in v) / len(v)) ** 0.5


def main():
    cnt = dict(C.counts_from_align([ALIGN40]))
    syms = sorted(cnt)
    jobs = []
    for name, path in TEXTS:
        toks = signs(path)
        jobs.append((toks, cnt))
        for k in range(RUNS):
            t2 = toks[:]
            random.Random(k).shuffle(t2)
            jobs.append((t2, cnt))
        for k in range(RUNS):
            perm = syms[:]
            random.Random(100 + k).shuffle(perm)
            jobs.append((toks, {perm[i]: cnt[s] for i, s in enumerate(syms)}))
    with mp.Pool(min(len(jobs), max(1, (os.cpu_count() or 2) - 1), 13)) as pool:
        res = pool.map(score, jobs, chunksize=1)
    L = [f'Key-fit control: letter-40 key ({len(syms)} signs), first {NSIGNS} signs of each text, LM weight {LMW}, '
         f'beam {BEAM}, {RUNS} runs per control.',
         'z = (real - mean of the control) / standard deviation of the control', '',
         f'{"text":20s} {"real":>8s}   {"shuffled order":>24s}   {"permuted key":>24s}']
    per = 1 + 2 * RUNS
    for i, (name, path) in enumerate(TEXTS):
        r = res[i * per:(i + 1) * per]
        real, sh, pk = r[0], r[1:1 + RUNS], r[1 + RUNS:]
        ms, ss = stats(sh)
        mk, sk = stats(pk)
        L.append(f'{name:20s} {real:8.1f}   {ms:8.1f} +- {ss:4.1f} (z {(real - ms) / ss:4.1f})   '
                 f'{mk:8.1f} +- {sk:4.1f} (z {(real - mk) / sk:4.1f})')
    with open(C.P('results/keyfit_control.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
