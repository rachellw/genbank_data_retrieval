def group_blocks(dna_blocks):
    grouped_lines = []
    i = 0
    while i < len(dna_blocks):
        blocks = dna_blocks[i:i+6]
        base_number = ((10*i)+1)
        line = ' '.join(blocks)
        formatted_line = f"{base_number:>9} {line}"
        grouped_lines.append(formatted_line)
        i += 6
    return grouped_lines