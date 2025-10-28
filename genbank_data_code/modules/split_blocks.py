def split_dna_blocks(DNA_string):
    dna_blocks = []
    start = 0
    while start < len(DNA_string):
        block = DNA_string[start:start+10]
        dna_blocks.append(block)
        start += 10
    return dna_blocks