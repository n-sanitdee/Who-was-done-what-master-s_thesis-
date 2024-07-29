import spacy
import pandas as pd

# Load English language model
nlp = spacy.load("en_core_web_trf")
nlp.max_length = 200000000  # Increase the max_length limit to accommodate longer texts

# Path to the input and output files
input_file_path = "cleaned_arctic.ru.txt"
output_file_path = "passive_constructions_be_get_rus_arctic.xlsx"

# Function to get the full phrase including modifiers
def get_full_phrase(token):
    return token.text

# Function to get only modifiers
def get_modifiers(token):
    return '_'.join([child.text for child in token.children if child.dep_ in ['amod', 'compound']])

# Initialize lists to store results
be_passives = []
get_passives = []
subject_verb_pairs = []

# Process each sentence in the input file individually
with open(input_file_path, "r") as input_file:
    for line in input_file:
        # Process the text of each sentence with spaCy
        doc = nlp(line)
        
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

                    # Find the auxiliary verb (be or get)
                    aux = None
                    for child in token.head.children:
                        if child.dep_ == "auxpass":
                            aux = child.lemma_
                    
                    # Find the by-agent
                    by_agent = ''
                    for child in token.head.children:
                        if child.dep_ == "agent":
                            # Construct the full agent phrase
                            agent_phrase = ' '.join([get_full_phrase(t) for t in child.subtree if t.dep_ in ["pobj", "amod", "compound", "agent"]])
                            by_agent = f"{agent_phrase.replace(' ', '_')}"

                    # Check if the auxiliary verb is "be" or "get"
                    if aux == "be":
                        be_passives.append((subject_modifiers, f"{subject}_{token.head.lemma_}", by_agent))
                    elif aux == "get":
                        get_passives.append((subject_modifiers, f"{subject}_{token.head.lemma_}", by_agent))
                    
                    # Append to subject_verb_pairs regardless of the auxiliary verb
                    subject_verb_pairs.append((subject_modifiers, f"{subject}_{token.head.lemma_}", by_agent))

# Create DataFrames for be-passives, get-passives, and subject-verb pairs
df_be_passives = pd.DataFrame(be_passives, columns=["Modifiers", "Subject_Verb", "By_Agent"])
df_get_passives = pd.DataFrame(get_passives, columns=["Modifiers", "Subject_Verb", "By_Agent"])
df_subject_verb_pairs = pd.DataFrame(subject_verb_pairs, columns=["Modifiers", "Subject_Verb", "By_Agent"])

# Write DataFrames to an Excel file with three tabs
with pd.ExcelWriter(output_file_path) as writer:
    df_be_passives.to_excel(writer, sheet_name="Be_Passives", index=False)
    df_get_passives.to_excel(writer, sheet_name="Get_Passives", index=False)
    df_subject_verb_pairs.to_excel(writer, sheet_name="Subject_Verb_Pairs", index=False)
