import spacy

# Load English language model
nlp = spacy.load("en_core_web_trf")
nlp.max_length = 200000000  # Increase the max_length limit to accommodate longer texts

# Path to the input and output files
input_file_path = "cleaned_tass.com.txt"
output_file_path = "passive_pairs_trf_tass.com.txt"

# Process each sentence in the input file individually
with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
    for line in input_file:
        # Process the text of each sentence with spaCy
        doc = nlp(line)
        
        # Initialize a list to store passive voice constructions for the current sentence
        passive_constructions = []

        # Extract passive voice constructions with dependency tags for the current sentence
        for sentence in doc.sents:
            for token in sentence:
                if token.dep_ == "nsubjpass":
                    if token.head.dep_ == 'relcl' and token.pos_ == 'PRON':
                        # Take token.head as verb and token.head.head as the subject
                        passive_constructions.append((token.head.head.text, token.head.text))
                    # Check if the token is a NOUN and PROPN
                    elif token.pos_ in ['NOUN', 'PROPN']: #elif token.pos_ in ['NOUN', 'PROPN']:
                        passive_constructions.append((token.text, token.head.text))

        # Write passive voice constructions with dependency tags for the current sentence to the output file
        for construction in passive_constructions:
            output_file.write(f"{construction[0]}_{construction[1]}\n")
