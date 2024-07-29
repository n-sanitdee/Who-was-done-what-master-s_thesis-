import spacy

# Load English language model
nlp = spacy.load("en_core_web_trf")

# Increase max length if needed (set to a lower value if you encounter memory issues)
nlp.max_length = 15000000

def process_line(line, output_file):
    # Process the line with SpaCy
    doc = nlp(line)
    # Detect passive voice constructions
    for sentence in doc.sents:
        for token in sentence:
            if token.dep_ == "nsubjpass":
                # Write the detected passive voice sentence to the output file
                output_file.write(sentence.text + "\n")
                break

# Open the input and output files
with open("eng_news_2019_cleaned.txt", "r") as input_file, open("passive_text_leipzig_2019.txt", "w") as output_file:
    for line in input_file:
        process_line(line.strip(), output_file)
