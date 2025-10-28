def genbank(dna):
    #import group_lines
    from . import split_blocks
    from . import group_lines
    # convert to lowercase
    dna = dna.lower()
    # split into groups of 10 bases
    dna_blocks = split_blocks.split_dna_blocks(dna)
    # split into lines of 60 bases
    lines_of_blocks = group_lines.group_blocks(dna_blocks)
    
    # print each line
    for line in lines_of_blocks:
        print(line)