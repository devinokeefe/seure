"""Two-reader check of the transcription of letter 39.

Reader 1 and reader 2 transcribed the cipher block independently. This script aligns their transcriptions line
by line (edit distance) and counts the signs on which they agree.

    python code/compare_readers.py      writes results/letter39_readers.txt

Files (data/fr3151/cipher/): 39_f71r_reader1.txt (reader 1 before the comparison, "v3"), 39_f71r_reader2.txt
(reader 2; label? = uncertain, a?|b = best guess a, alternative b), 39_f71r.txt (the final reading, "v4").
"""
import common as C

DIR = 'data/fr3151/cipher/'


def reader2(path):
    """-> lines of (first label, set of all labels offered, marked uncertain)"""
    out = []
    for line in C.read_lines(path):
        out.append([(x.split('?')[0].split('|')[0], set(x.replace('?', '|').split('|')) - {''}, '?' in x) for x in line])
    return out


def align(a, b):
    """edit-distance alignment of a (labels) with b (reader-2 tuples); an alternative of reader 2 costs 0.5"""
    n, m = len(a), len(b)

    def sub(i, j):
        return 0 if a[i] == b[j][0] else (0.5 if a[i] in b[j][1] else 1)

    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + sub(i - 1, j - 1))
    i, j, ops = n, m, []
    while i or j:
        if i and j and D[i][j] == D[i - 1][j - 1] + sub(i - 1, j - 1):
            ops.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif i and D[i][j] == D[i - 1][j] + 1:
            ops.append((i - 1, None))
            i -= 1
        else:
            ops.append((None, j - 1))
            j -= 1
    return ops[::-1]


def compare(name, A, B, L):
    tot = same = alt = diff = only1 = only2 = uncdiff = 0
    detail = []
    for ln, (a, b) in enumerate(zip(A, B), 1):
        for i, j in align(a, b):
            tot += 1
            if i is None:
                only2 += 1
                detail.append(f'L{ln:02d} -      reader 2 only: {b[j][0]}')
            elif j is None:
                only1 += 1
                detail.append(f'L{ln:02d} k{i:<2d}   {name} only: {a[i]}')
            elif a[i] == b[j][0]:
                same += 1
            elif a[i] in b[j][1]:
                alt += 1
                detail.append(f'L{ln:02d} k{i:<2d}   {a[i]} = an alternative of reader 2 ({"|".join(sorted(b[j][1]))})')
            else:
                diff += 1
                uncdiff += b[j][2]
                detail.append(f'L{ln:02d} k{i:<2d}   {a[i]} / reader 2: {b[j][0]}{"?" if b[j][2] else ""}')
    L += ['', f'== {name} against reader 2',
          f'{name}: {sum(map(len, A))} signs; reader 2: {sum(map(len, B))} signs '
          f'({sum(1 for line in B for x in line if x[2])} marked uncertain); aligned positions: {tot}',
          f'same label {same}; {name} = an alternative given by reader 2: {alt}; different {diff} '
          f'(of which reader 2 marked uncertain: {uncdiff}); in {name} only {only1}; in reader 2 only {only2}',
          f'exact agreement {same}/{tot} = {same / tot:.3f}; agreement counting the alternatives '
          f'{same + alt}/{tot} = {(same + alt) / tot:.3f}'] + detail


def main():
    r1 = C.read_lines(DIR + '39_f71r_reader1.txt')
    final = C.read_lines(DIR + '39_f71r.txt')
    r2 = reader2(DIR + '39_f71r_reader2.txt')
    L = ['Letter 39 (BnF fr. 3151, fo. 71r): agreement between two independent transcriptions.']
    compare('reader 1 (v3)', r1, r2, L)
    compare('final reading (v4)', final, r2, L)
    changed = [(ln, k, a, b) for ln, (x, y) in enumerate(zip(r1, final), 1) for k, (a, b) in enumerate(zip(x, y)) if a != b]
    assert all(len(x) == len(y) for x, y in zip(r1, final))
    L += ['', f'== signs changed from reader 1 (v3) to the final reading (v4): {len(changed)}']
    L += [f'L{ln:02d} k{k:<2d}   {a} -> {b}' for ln, k, a, b in changed]
    with open(C.P('results/letter39_readers.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(x for x in L if not (x[:1] == 'L' and x[1:3].isdigit())))


if __name__ == '__main__':
    main()
