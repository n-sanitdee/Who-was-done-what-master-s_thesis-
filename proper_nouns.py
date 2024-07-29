import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 1500000  # Increase the max_length limit to accommodate longer texts

# Read text from file
with open("cleaned_ukraine_war2.txt", "r") as file:
	text = file.read()

# Process the text
doc = nlp(text)

# Initialize a list to store passive voice constructions
passive_constructions = []

# Extract passive voice constructions with dependency tags
for sentence in doc.sents:
	for token in sentence:
		if token.dep_ == "nsubjpass":
			if token.pos_ == "PROPN":
				passive_constructions.append((token.text, token.head.text))

# Write passive voice constructions with dependency tags to a new file
with open("passive_subjects_verbs_PROPN.txt", "w") as file:
	for construction in passive_constructions:
		file.write(f"{construction[0]}_{construction[1]}\n")

