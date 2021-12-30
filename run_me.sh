#!/bin/bash

python src/ex1.py

zcat data/Mus_musculus.GRCm38.88.chr19.gtf.gz > data/Mus_musculus.GRCm38.88.chr19.gtf
zcat data/Mus_musculus.GRCm38.dna_rm.chr19.fa.gz > data/Mus_musculus.GRCm38.dna_rm.chr19.fa
zcat data/reads.mate_1.fq.gz > data/reads.mate_1.fq
zcat data/reads.mate_2.fq.gz > data/reads.mate_2.fq

STAR --runThreadN 4 --runMode genomeGenerate --genomeDir data/genome --genomeFastaFiles data/Mus_musculus.GRCm38.dna_rm.chr19.fa --sjdbGTFfile data/Mus_musculus.GRCm38.88.chr19.gtf --genomeSAindexNbases 11

STAR --runThreadN 4 --genomeDir data/genome --readFilesIn data/reads.mate_1.fq data/reads.mate_2.fq --outFileNamePrefix data/mapping/

grep "^@" -v data/mapping/Aligned.out.sam | grep "^$" -v | wc -l 

grep "^@" -v data/mapping/Aligned.out.sam | grep "^$" -v | cut -f1 | sort | uniq -c | sort | grep -P "^\s*1\s" | wc -l

grep "^@" -v data/mapping/Aligned.out.sam | grep "^$" -v | cut -f1 | sort | uniq -c | sort | grep -P "^\s*[0-9]*[2-9]\s" | wc -l

python src/ex2.py

flake8 src/

coverage run --source=src/ -m pytest

coverage report -m

