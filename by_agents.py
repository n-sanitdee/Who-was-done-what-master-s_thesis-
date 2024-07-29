import spacy

# Load English language model
nlp = spacy.load("en_core_web_trf")
nlp.max_length = 200000000  # Increase the max_length limit to accommodate longer texts

# Path to the input and output files
input_file_path = "arctic.ru.txt"
output_file_path = "arctic_by-agents.txt"

# Function to get the full phrase including modifiers
def get_full_phrase(token):
    modifiers = [child.text for child in token.children if child.dep_ in ['amod', 'compound']]
    return token.text

# Function to get only modifiers
def get_modifiers(token):
    return '_'.join([child.text for child in token.children if child.dep_ in ['amod', 'compound']])

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
                    # Determine the subject of the passive construction
                    if token.head.dep_ == 'relcl' and token.pos_ == 'PRON':
                        subject = token.head.head.text
                        subject_modifiers = get_modifiers(token.head.head)
                        verb = token.head.text
                    elif token.pos_ in ['NOUN', 'PROPN']:
                        subject = token.text
                        subject_modifiers = get_modifiers(token)
                        verb = token.head.text
                    else:
                        continue

                    # Find the by-agent
                    by_agent = ''
                    for child in token.head.children:
                        if child.dep_ == "agent":
                            # Construct the full agent phrase
                            agent_phrase = ' '.join([get_full_phrase(t) for t in child.subtree if t.dep_ in ["pobj", "amod", "compound", "agent"]])
                            by_agent = f"{agent_phrase.replace(' ', '_')}"

                    # Combine the subject, verb, and by-agent
                    subject_verb = f"{subject}_{verb}"
                    passive_constructions.append((subject_modifiers, subject_verb, by_agent))

        # Write passive voice constructions with dependency tags for the current sentence to the output file
        for construction in passive_constructions:
            output_file.write(f"{construction[0]}\t{construction[1]}\t{construction[2]}\n")
