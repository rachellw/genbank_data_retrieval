
### import required modules
from modules import entrez_efetch, genbank_as_file, genbank, group_lines, make_file, print_attribute, split_blocks
from utils import logger
import modules.dictionary_to_object as dto
print(dto.__file__)
from modules.dictionary_to_object import dict2obj
#  main.py
# fetch a GenBank transcript record as a dictionary
transcript_id = input ("Please specify a Genbank ID (including the version number) in the format NM_, NR_, XM_, or XR_000000.0 ")
record = entrez_efetch.fetch_transcript_record(transcript_id)

# calling the function dict2obj and
# passing the dictionary as argument 
data_as_object =  dict2obj(record)
#convert sequence to capital letters
data_as_object.GBSeq_sequence = data_as_object.GBSeq_sequence.upper()

#state the atributes available, ask user to input an attribute, and if data file is a sequence ask if user would like it to be presented as a Genbank file
print("The available attributes are:", dir(data_as_object))

key = input('Please specify one attribute that you would like to be printed to the screen. ')
attribute_value = getattr(data_as_object, key)

if key == 'GBSeq_sequence' and input("Would you like this presented in Genbank format? Please type 'yes' or 'no'. ") == 'yes':
    genbank.genbank(attribute_value)    
     
else:         # If the attribute is another object, print its contents
    print_attribute.print_attribute_value (attribute_value)

#ask if user would like to save output to a file
if key != 'GBSeq_sequence' and input("Would you like to export this as a file? Please type 'yes' or 'no'. ") == 'yes':
    make_file.make_file (transcript_id, key,attribute_value)
elif key == 'GBSeq_sequence' and input("Would you like to export this as a file? Please type 'yes' or 'no'. ") == 'yes':
    genbank_as_file.genbank_as_file(attribute_value,transcript_id)

else: print('It has been a pleasure assisting you.')