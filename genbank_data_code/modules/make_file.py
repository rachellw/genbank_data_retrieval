def make_file (transcript_id, key,attribute_value):
    filename = f"{transcript_id}_{key}.txt"
    with open(filename, 'w') as f:
        f.write(attribute_value)
    print(f"A file entitled {filename} has been created. \n It has been a pleasure assisting you.")