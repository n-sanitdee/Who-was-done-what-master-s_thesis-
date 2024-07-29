import pandas as pd
import spacy
from bertopic import BERTopic
import gc
import plotly.io as pio

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_trf")
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    exit(1)

# Function to preprocess words using spaCy
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(tokens)

# Read the text file line-by-line and preprocess
file_path = 'passive_text_leipzig_2018.txt'                ########### input file ##########
processed_texts = []

try:
    with open(file_path, 'r') as file:
        for line in file:
            processed_text = preprocess(line.strip())
            processed_texts.append(processed_text)
except Exception as e:
    print(f"Error reading or processing the file: {e}")
    exit(1)

# Create a DataFrame with the processed texts
df = pd.DataFrame({'Processed_Words': processed_texts})

# Display the preprocessed words
print(df.head())

# Create a BERTopic model
try:
    topic_model = BERTopic(language="english")
except Exception as e:
    print(f"Error creating BERTopic model: {e}")
    exit(1)

# Fit the model on the processed words
try:
    topics, probabilities = topic_model.fit_transform(df['Processed_Words'])
    df['Topic'] = topics
except Exception as e:
    print(f"Error fitting the BERTopic model: {e}")
    exit(1)

# Calculate total score for each topic
df['Score'] = 1  # Assigning a default score of 1 to each word
topic_scores = df.groupby('Topic')['Score'].sum().reset_index()

# Write topics with their scores to a file
output_file_path = 'topic_scores_Leipzig_2018.txt'                            ########### output file ##########
try:
    with open(output_file_path, 'w') as file:
        for topic in topic_scores['Topic']:
            score = topic_scores[topic_scores['Topic'] == topic]['Score'].values[0]
            topic_info = topic_model.get_topic(topic)
            
            file.write(f"Topic {topic}: Score = {score}\n")
            for word, weight in topic_info:
                file.write(f"{word}: {weight}\n")
            file.write('\n')
except Exception as e:
    print(f"Error writing to the file: {e}")

# Visualize the topics and save to high-resolution JPG using Plotly
try:
    fig = topic_model.visualize_barchart(width=280, height=330, top_n_topics=12, n_words=10)

    # Update the title of the figure
    fig.update_layout(
        title={
            'text': "Popular Topics in the Leipzig 2018 Corpus",                          ########### chart title ##########
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(
            size=24,  # Increase the font size
            color='black'  # Set the color to black
        )
    )

    # Save the figure with the updated title as a high-resolution JPEG image
    pio.write_image(fig, "charts_topics_leipzig_2018.jpg", scale=3)                            ########### chart file name ##########
except Exception as e:
    print(f"Error visualizing or saving the image: {e}")

# Clear memory
gc.collect()
