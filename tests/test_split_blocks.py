import pytest
from genbank_data_code.modules import split_blocks

def test_split_blocks():
    seq = "aggagtaagcccttgcaactggaaatacacccattg"
    expected = ['aggagtaagc', 'ccttgcaact', 'ggaaatacac', 'ccattg']
    assert split_blocks.split_dna_blocks(seq) == expected

def test_not_multiple_of_10():
    dna = "ACGTACGTACG"  # length = 11
    result = split_blocks.split_dna_blocks(dna)
    assert result == ["ACGTACGTAC", "G"]

def test_shorter_than_10():
    dna = "ACGT"
    result = split_blocks.split_dna_blocks(dna)
    assert result == ["ACGT"]

def test_empty_string():
    dna = ""
    result = split_blocks.split_dna_blocks(dna)
    assert result == []

def test_length_exactly_10():
    dna = "ACGTACGTAC"
    result = split_blocks.split_dna_blocks(dna)
    assert result == ["ACGTACGTAC"]

def test_large_sequence():
    dna = "A" * 105  # 105 bases
    result = split_blocks.split_dna_blocks(dna)
    assert len(result) == 11  # 10 full blocks + 1 remainder
    assert result[0] == "A" * 10
    assert result[-1] == "A" * 5