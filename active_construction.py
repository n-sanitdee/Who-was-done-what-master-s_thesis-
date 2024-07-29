import spacy

# Load English language model
nlp = spacy.load("en_core_web_trf")
nlp.max_length = 200000000  # Increase the max_length limit to accommodate longer texts

# Path to the input and output files
input_file_path = "eng_news_2023_cleaned.txt"
output_file_path = "active_pairs_2023.txt"

# Process each sentence in the input file individually
with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
    for line in input_file:
        # Process the text of each sentence with spaCy
        doc = nlp(line)
        
        # Initialize a list to store active voice constructions for the current sentence
        active_constructions = []

        # Extract active voice constructions with dependency tags for the current sentence
        for sentence in doc.sents:
            for token in sentence:
                if token.dep_ == "nsubj":
                    # Check if the token is a NOUN or PROPN
                    if token.pos_ in ['NOUN', 'PROPN']:
                        active_constructions.append((token.text, token.head.text))

        # Write active voice constructions with dependency tags for the current sentence to the output file
        for construction in active_constructions:
            output_file.write(f"{construction[0]}_{construction[1]}\n")
