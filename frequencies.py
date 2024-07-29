import pandas as pd
from collections import Counter
import spacy

# Load English language model
nlp = spacy.load("en_core_web_trf")

# Initialize Counters for subject word frequencies and verb word frequencies
subject_word_freq = Counter()
verb_word_freq = Counter()

# Initialize Counter for subject_verb pair frequencies
subject_verb_freq = Counter()

# Read from the file
with open("passive_pairs_trf_tass.com.txt", "r") as file:
    # Iterate over each line in the file
    for line in file:
        # Split the line into subject and verb
        subject, verb = line.strip().split("_")
        
        # Process each word in subject
        doc_subject = nlp(subject)
        for token in doc_subject:
            lemma = token.lemma_
            subject_word_freq[lemma] += 1
        
        # Process each word in verb
        doc_verb = nlp(verb)
        for token in doc_verb:
            lemma = token.lemma_
            verb_word_freq[lemma] += 1
        
        # Combine subject and verb into a single string
        subject_verb_pair = f"{subject}_{verb}"
        subject_verb_freq[subject_verb_pair] += 1

# Create DataFrame for subject word frequencies
df_subject_word_freq = pd.DataFrame(subject_word_freq.items(), columns=["Subject", "Frequency"])

# Create DataFrame for verb word frequencies
df_verb_word_freq = pd.DataFrame(verb_word_freq.items(), columns=["Verb", "Frequency"])

# Create DataFrame for subject-verb pair frequencies
df_subject_verb_freq = pd.DataFrame(subject_verb_freq.items(), columns=["Subject_Verb", "Frequency"])

# Write DataFrames to an Excel file
with pd.ExcelWriter("frequencies_tass.com.xlsx") as writer:
    df_subject_word_freq.to_excel(writer, sheet_name="Subject_Word_Frequencies", index=False)
    df_verb_word_freq.to_excel(writer, sheet_name="Verb_Word_Frequencies", index=False)
    df_subject_verb_freq.to_excel(writer, sheet_name="Subject_Verb_Pair_Frequencies", index=False)
