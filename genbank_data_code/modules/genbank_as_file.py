    # create file and save Genbank formatted sequence
from . import split_blocks
from . import group_lines
def genbank_as_file(dna,transcript_id):
    # split into groups of 10 bases
    dna_blocks = split_blocks.split_dna_blocks(dna)
    # split into lines of 60 bases
    lines_of_blocks = group_lines.group_blocks(dna_blocks)
    genbank_filename = f"{transcript_id}_Genbank.txt"
    print (genbank_filename)
    with open(genbank_filename, 'w') as f:
        # print each line to file
        for line in lines_of_blocks:
            f.write(line + "\n")
    print(f"A file entitled {genbank_filename} has been created. \n It has been a pleasure assisting you.")
    