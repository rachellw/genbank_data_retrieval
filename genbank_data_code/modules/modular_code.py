import requests
import xmltodict
 utils.logger as logger
from utils  import logger
class TranscriptIdError(Exception):
    """
    Custom exception raised when a transcript identifier does not meet the
    expected NCBI format requirements.
    """
    pass

def fetch_transcript_record(transcript_id):
    """
    Fetch a transcript record from the NCBI Nucleotide database using the
    Entrez EFetch API, and return the record as a Python dictionary
    (converted from XML).

    Parameters:
    transcript_id (str): A transcript accession with version number.
        Must start with NM_, NR_, XM_, or XR_ (e.g., "NM_000093.4").

    Returns:
    dict: A Python dictionary representation of the transcript record,
        parsed from the XML response.

    Raises:
    TranscriptIdError: If the transcript_id does not have the expected prefix
        or lacks a version number.
    requests.exceptions.RequestException: If there is a network or API error.
    """

    # Validate that the transcript ID has the expected RefSeq prefix
    if not transcript_id.startswith(("NM_", "NR_", "XM_", "XR_")):
        raise TranscriptIdError(
            f"Invalid transcript ID: {transcript_id}. "
            "Must start with NM_, NR_, XM_, or XR_."
        )

    # Validate that the transcript ID includes a version (e.g., ".3")
    if "." not in transcript_id:
        raise TranscriptIdError(
            f"Transcript ID {transcript_id} must include a version number "
            "(e.g., NM_000093.4)."
        )

    # Base URL for NCBI Entrez EFetch
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",   # NCBI nucleotide database
        "id": transcript_id,  # transcript accession
        "retmode": "xml"      # request XML format for easier parsing
    }

    try:
        # Perform GET request to NCBI EFetch
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching transcript {transcript_id}: {e}")
        raise

    # Convert XML response to Python dict using xmltodict and strip out the GBSet/GBSeq wrapper
    return xmltodict.parse(r.text)['GBSet']['GBSeq']



#convert record to object 
def dict2obj(d):
    
    # checking whether object d is a
    # instance of class list
    if isinstance(d, list):
           d = [dict2obj(x) for x in d] 

    # if d is not a instance of dict then
    # directly object is returned
    if not isinstance(d, dict):
           return d
 
    # declaring a class
    class C:
        pass
 
    # constructor of the class passed to obj
    obj = C()
 
    for k in d:
        obj.__dict__[k] = dict2obj(d[k])
 
    return obj

def split_dna_blocks(DNA_string):
    dna_blocks = []
    start = 0
    while start < len(DNA_string):
        block = DNA_string[start:start+10]
        dna_blocks.append(block)
        start += 10
    return dna_blocks
   
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

def genbank(dna):
    # convert to lowercase
    dna = dna.lower()
    # split into groups of 10 bases
    dna_blocks = split_dna_blocks(dna)
    # split into lines of 60 bases
    lines_of_blocks = group_blocks(dna_blocks)
    
    # print each line
    for line in lines_of_blocks:
        print(line)

    # create file and save Genbank formatted sequence
def genbank_as_file(dna,transcript_id):
    # split into groups of 10 bases
    dna_blocks = split_dna_blocks(dna)
    # split into lines of 60 bases
    lines_of_blocks = group_blocks(dna_blocks)
    genbank_filename = f"{transcript_id}_Genbank.txt"
    print (genbank_filename)
    with open(genbank_filename, 'w') as f:
        # print each line to file
        for line in lines_of_blocks:
            f.write(line + "\n")
    print(f"A file entitled {genbank_filename} has been created. \n It has been a pleasure assisting you.")
    


def print_attribute_value (attribute_value):
    if hasattr(attribute_value, '__dict__'):
            print(vars(attribute_value))  # show its fields
    elif isinstance(attribute_value, list):
        for i, item in enumerate(attribute_value, start=1):
                print(f"[{i}] {item if not hasattr(item, '__dict__') else vars(item)}")
    else:
        print(attribute_value)

def make_file (transcript_id, key,attribute_value):
    filename = f"{transcript_id}_{key}.txt"
    with open(filename, 'w') as f:
        f.write(attribute_value)
    print(f"A file entitled {filename} has been created. \n It has been a pleasure assisting you.")
##################################################################
#  main.py
# fetch a GenBank transcript record as a dictionary
transcript_id = input ("Please specify a Genbank ID (including the version number) in the format NM_, NR_, XM_, or XR_000000.0 ")
record = fetch_transcript_record(transcript_id)

# calling the function dict2obj and
# passing the dictionary as argument 
data_as_object = dict2obj(record)
#convert sequence to capital letters
data_as_object.GBSeq_sequence = data_as_object.GBSeq_sequence.upper()

#state the atributes available, ask user to input an attribute, and if data file is a sequence ask if user would like it to be presented as a Genbank file
print("The available attributes are:", dir(data_as_object))

key = input('Please specify one attribute that you would like to be printed to the screen. ')
attribute_value = getattr(data_as_object, key)

if key == 'GBSeq_sequence' and input("Would you like this presented in Genbank format? Please type 'yes' or 'no'. ") == 'yes':
    genbank(attribute_value)    
     
else:         # If the attribute is another object, print its contents
    print_attribute_value (attribute_value)

#ask if user would like to save output to a file
if key != 'GBSeq_sequence' and input("Would you like to export this as a file? Please type 'yes' or 'no'. ") == 'yes':
    make_file (transcript_id, key,attribute_value)
elif key == 'GBSeq_sequence' and input("Would you like to export this as a file? Please type 'yes' or 'no'. ") == 'yes':
    genbank_as_file(attribute_value,transcript_id)

else: print('It has been a pleasure assisting you.')