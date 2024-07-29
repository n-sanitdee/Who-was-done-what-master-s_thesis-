import spacy
from collections import defaultdict

# Load English language model
nlp = spacy.load("en_core_web_trf")
nlp.max_length = 20000000  # Increase the max_length limit to accommodate longer texts

# Function to tokenize and lemmatize text into words using spaCy
def tokenize_and_lemmatize_text_spacy(text):
    # Process the text with spaCy
    doc = nlp(text)
    # Extract lemmatized tokens from the document and convert them to lowercase
    return [token.lemma_.lower() for token in doc if not token.is_space]

# Function to count word frequencies in the corpus
def count_word_frequencies(corpus_tokens, target_words):
    frequencies = defaultdict(int)
    for word in corpus_tokens:
        if word in target_words:
            frequencies[word] += 1
    return frequencies

# Function to write frequencies to file
def write_frequencies_to_file(frequencies, filename):
    with open(filename, 'w') as file:
        for word, frequency in frequencies.items():
            file.write(f"{word}: {frequency}\n")

if __name__ == "__main__":
    # Tokenize and lemmatize target words using spaCy
    with open("word_freq_whole_2019_v.txt", 'r') as file:               ########## target_words ############
        target_words = set(tokenize_and_lemmatize_text_spacy(file.read()))

    # Initialize frequencies dictionary
    frequencies = defaultdict(int)
    
    # Process corpus text line by line and count word frequencies
    input_file_path = "eng_news_2019_cleaned.txt"                        ########### corpus ###########
    with open(input_file_path, 'r') as file:
        for line in file:
            tokens = tokenize_and_lemmatize_text_spacy(line)
            line_frequencies = count_word_frequencies(tokens, target_words)
            for word, frequency in line_frequencies.items():
                frequencies[word] += frequency

    # Write word frequencies to file
    write_frequencies_to_file(frequencies, "freq_whole_2019_v.txt")            ########## output ############
