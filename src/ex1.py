from typing import List, Tuple, Dict


def parse_fasta(path: str) -> Tuple[List[str], List[str]]:
    """ Parses a file in FASTA format.

    Parses a FASTA file and returns two list containing the headers
    and sequences, respectively.

    Args:
        path : path to the FASTA file

    Returns:
        headers : list containing the headers of the sequences
        sequences : list containing the sequences themselves
    """
    headers = []
    sequences = []
    with open(path, 'r') as f:
        seqs = f.read().split('>')[1:]
        for s in seqs:
            split_seq = s.split('\n', 1)
            headers.append(split_seq[0])
            sequences.append(split_seq[1].replace('\n', ''))
    return headers, sequences


def discard_ambiguous_seqs(heads: List[str], seqs: List[str]) \
                                        -> Tuple[List[str], List[str]]:
    """ Discards sequences that are not representing DNA.

    Takes a list of sequences and discards any that do contain letters
    which are not contained in the DNA "alphabet". Also discards the
    corresponding headers to maintain consistency.

    Args:
        heads : headers of the sequences
        seqs : sequences to be filtered

    Returns:
        h : filtered list of headers
        s : filtered list of corresponding sequences
    """
    alphabet = 'ACTGactg'
    h = []
    s = []
    for i in range(len(heads)):
        if all(c in alphabet for c in seqs[i]):
            h.append(heads[i])
            s.append(seqs[i])
    return h, s


def nucleotide_frequencies(seqs: List[str]) -> None:
    """ Calculates nucleotide frequencies from list of sequences.

    Calculates frequencies of the four nucleotides from a list of
    sequences and prints them on the console.

    Args:
        seqs : list of sequences to be analysed
    """
    n = sum([len(s) for s in seqs])
    a_freq = sum([s.upper().count('A') for s in seqs]) / n
    c_freq = sum([s.upper().count('C') for s in seqs]) / n
    t_freq = sum([s.upper().count('T') for s in seqs]) / n
    g_freq = sum([s.upper().count('G') for s in seqs]) / n
    # rounded to two digits instead of one since it seemed sensible
    print('##########\nA: {:.2f}\nC: {:.2f}\nT: {:.2f}\nG: {:.2f}'
          '\n##########'.format(a_freq, c_freq, t_freq, g_freq))


def map_reads(query: str, reference: str) -> Dict[str, Dict[str, List[int]]]:
    """ Maps query to reference sequences.

    Takes files containing query and reference sequences
    and tries to maps all query sequences on all reference
    sequences. Also prints the nucleotide frequencies of both
    query and reference sequences on the console. Returns a
    dictionary of dictionaries of lists of integers: the outer
    dictionary uses names of query sequences as keys, the inner
    one uses reference sequence names as keys and a list of
    indices indicating at which position reference sequence the
    query sequence occurs as an exact substring as values.

    Args:
        query : path to the FASTA file containing query sequences
        reference : path to the FASTA file containing reference sequences

    Returns:
        seqs_dict : dictionary of mapped reads
    """
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
