def parse_fasta(path):
    headers = []
    sequences = []
    with open(path, 'r') as f:
        seqs = f.read().split('>')[1:]
        for s in seqs:
            split_seq = s.split('\n', 1)
            headers.append(split_seq[0])
            sequences.append(split_seq[1].replace('\n', ''))
    return headers, sequences


def discard_ambiguous_seqs(heads, seqs):
    alphabet = 'ACTGactg'
    h = []
    s = []
    for i in range(len(heads)):
        if all(c in alphabet for c in seqs[i]):
            h.append(heads[i])
            s.append(seqs[i])
    return h, s


def nucleotide_frequencies(seqs):
    n = sum([len(s) for s in seqs])
    a_freq = sum([s.upper().count('A') for s in seqs]) / n
    c_freq = sum([s.upper().count('C') for s in seqs]) / n
    t_freq = sum([s.upper().count('T') for s in seqs]) / n
    g_freq = sum([s.upper().count('G') for s in seqs]) / n
    # rounded to two digits instead of one since it seemed sensible
    print('##########\nA: {:.2f}\nC: {:.2f}\nT: {:.2f}\nG: {:.2f}\n##########'.format(a_freq, c_freq, t_freq, g_freq))


def map_reads(query, reference):
    hq, sq = parse_fasta(query)
    hr, sr = parse_fasta(reference)

    hq, sq = discard_ambiguous_seqs(hq, sq)

    nucleotide_frequencies(sq)
    nucleotide_frequencies(sr)

    seqs_dict = {}
    for i in range(len(hq)):
        seqs_dict[hq[i]] = {}
        for k in range(len(hr)):
            seqs_dict[hq[i]][hr[k]] = []
            idx = 0
            while True:
                idx = sr[k].upper().find(sq[i].upper(), idx)
                if idx == -1:
                    if len(seqs_dict[hq[i]][hr[k]]) == 0:
                        seqs_dict[hq[i]].pop(hr[k])
                    break
                else:
                    seqs_dict[hq[i]][hr[k]].append(idx)
                    idx += 1
    return seqs_dict


if __name__ == '__main__':
    query = '../data/sequences.fasta'
    reference = '../data/genome.fasta'
    sd = map_reads(query, reference)
    print(sd)
