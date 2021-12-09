from src.ex1 import *
from src.ex2 import *
import os
import pytest


def test_parse_fasta():
    h, s = parse_fasta('test_data/reference.fasta')
    assert h == ['rseq1', 'rseq2']
    assert s == ['ATATGAGCACTCAGTAATAGCCATGGGAGT'
                 'CAACTCAGTAACCATACCGTTGTTACTAGC',
                 'ATCGTTTCATTTCAGCTCAGTATAATGAAA'
                 'GATTTTGCAAATGTTACTGAAACAAAAGCA']


def test_das():
    h, s = parse_fasta('test_data/query.fasta')
    h, s = discard_ambiguous_seqs(h, s)
    assert h == ['qseq1', 'qseq2', 'qseq4']
    assert s == ['CTCAGTA', 'CTCagTa', 'TTTTTTT']


def test_nf(capfd):
    h, s = parse_fasta('test_data/query.fasta')
    h, s = discard_ambiguous_seqs(h, s)
    nucleotide_frequencies(s)
    out, err = capfd.readouterr()
    assert out == '##########\nA: 0.19\nC: 0.19\n' \
                  'T: 0.52\nG: 0.10\n##########\n'


def test_map_reads():
    sd = map_reads('test_data/query.fasta',
                   'test_data/reference.fasta')
    assert sd == {'qseq1': {'rseq1': [9, 33], 'rseq2': [15]},
                  'qseq2': {'rseq1': [9, 33], 'rseq2': [15]},
                  'qseq4': {}}


def test_convert():
    path_to_s = 'test_data/convert_me.sam'
    path_to_f = sam_to_fasta(path_to_s)
    h, s = parse_fasta(path_to_f)
    os.remove(path_to_f)
    assert h == ['NS500637:2:H197YBGXX:1:11102:13568:10359',
                 'NS500637:2:H197YBGXX:1:11102:13568:10359']
    assert s == ['CGGTACTTCTCCAGATACAAAAGTTGCTTGCTGTTAAAAGCT'
                 'CCACGCCGCTTTTGTCTTATGAATTGTACTGCATCTTCATAT'
                 'TTCATTCCACCTTCAATTAATGCTAGGGCAACAAGCACCGGA'
                 'GCTCTGCCAAGGCCTGCGACACA',
                 'TGTGTCGCAGGCCTTGGCAGAGCTCCGGTGCTTGTTGCCCTA'
                 'GCATTAATTGAAGGTGGAATGAAATATGAAGATGCAGTACAA'
                 'TTCATAAGACAAAAGCGGCGTGGAGCTTTTAACAGCAAGCAA'
                 'CTTTTGTATCTGGAGAAGTACCG']
