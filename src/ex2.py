from pathlib import Path

from src.ex1 import map_reads


def sam_to_fasta(path: str) -> str:
    """ Converts a file from SAM to FASTA format.

    Args:
        path : path to the FASTA file

    Returns:
        str : path to the SAM file
    """
    with open(path, 'r') as sam_f:
        lines = sam_f.readlines()
        fasta_path = path.replace('.sam', '.fa')
        with open(fasta_path, 'w') as fasta_f:
            for line in lines:
                if not line.startswith('@'):
                    fields = line.split('\t')
                    fasta_f.write('>{}\n{}\n'.format(fields[0], fields[9]))
    return fasta_path


if __name__ == '__main__':
    path_to_sam = (
        str(Path(__file__).parents[1] / 'data/mapping/Aligned.out.sam')
    )
    reference = (
        str(Path(
            __file__
        ).parents[1] / 'data/Mus_musculus.GRCm38.dna_rm.chr19.fa')
    )
    query = sam_to_fasta(path_to_sam)
    sd = map_reads(query, reference)
    print(sd)

    # We can see that my method finds way less mappings than when using STAR.
    # This is because my method only looks for perfect matches, while STAR
    # allows for insertions, deletions and mismatches.
