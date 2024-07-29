import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
import matplotlib.cm as cm
from gensim.models import KeyedVectors

# Load the word vectors (assuming the path to the embeddings is correct)
word_vectors = KeyedVectors.load_word2vec_format(embedding_file, binary=True, limit=4000000)  # Adjusted limit

def display_pca_scatterplot(model, word_groups):
    # Extract all words from the groups
    all_words = [word for group in word_groups.values() for word in group]
    valid_words = [w for w in all_words if w in model]

    if not valid_words:
        print("None of the words in the list are present in the model vocabulary.")
        return

    word_vectors = np.array([model[w] for w in valid_words])

    # PCA transformation
    twodim = PCA().fit_transform(word_vectors)[:,:2]

    plt.figure(figsize=(30,30))

    # Plot all words with the same color and marker
    plt.scatter(twodim[:, 0], twodim[:, 1], edgecolors='red', c='red', marker='o', s=60)

    # Annotate all words
    for word, (x, y) in zip(valid_words, twodim):
        plt.text(x + 0.02, y + 0.02, word, fontsize=18)

    # Function to create a bubble around a group of points
    def create_bubble(points, color, alpha=0.2):
        if len(points) < 3:  # We need at least three points to create a polygon
            return None
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        # Optional: Expand the hull slightly to create a more encompassing bubble
        # Example: Add a small padding to each point
        hull = ConvexHull(hull_points)
        hull_points = hull_points[hull.vertices]
        # Create a closed polygon
        polygon = Polygon(hull_points, edgecolor=color, facecolor=color, linewidth=2, alpha=alpha)
        return polygon

    # Create and add bubbles for each group
    colors = cm.rainbow(np.linspace(0, 1, len(word_groups)))  # Generate different colors for each group
    legend_handles = []
    for (group_name, words), color in zip(word_groups.items(), colors):
        group_indices = [valid_words.index(word) for word in words if word in valid_words]
        group_points = twodim[group_indices]

        bubble = create_bubble(group_points, color)
        if bubble:
            plt.gca().add_patch(bubble)
            legend_handles.append(Polygon(np.empty((0, 2)), edgecolor=color, facecolor=color, label=group_name))  # Add legend handle

    plt.legend(handles=legend_handles, fontsize=20)  # Display the legend
    plt.title("Semantic Categories of Passive Subjects and Verbs in the Ukraine War Corpus", fontsize=40)  # Add title
    plt.tick_params(axis='both', which='major', labelsize=20)  # Adjust labelsize as needed
    plt.show()


# Create desired groups
word_groups = {
    'Civilian': ['people', 'Ukrainians', 'dude', 'folk', 'community', 'friend', 'member', 'public'],
    'Neutral Entities': ['object', 'factor', 'geography', 'sound', 'victory'],
    'Law and Governance': ['government', 'committee', 'parliament', 'agreement', 'federation', 'congress', 'representative', 'spokesman', 'corruption', 'corporation'],
    'Death and Danger': ['siren', 'fighting', 'attack', 'conflict', 'loss', 'bombardment', 'battle', 'attack', 'projectile', 'fire', 'strike'],
    'Media, Entertainment, Technology': ['media', 'CNN', 'comedian', 'journal', 'Press'],
    'Military and Authority': ['force', 'military', 'authority', 'command', 'frontline', 'guard', 'intelligence', 'defence', 'paratrooper', 'personnel', 'police', 'service', 'soldier', 'troop'],
    'Location': ['centre', 'firm', 'country', 'institute', 'district', 'West'],
    'Commute': ['traffic'],
    'Monetary and Business': ['cut', 'commission'],
    'Nominalization': ['inconsistency'],
    'Important Figures': ['Putin', 'president', 'leader', 'Director', 'Gazprom', 'Markle', 'Pravda', 'Shoigu'],
    'Weapon': ['drone', 'missile', 'weapon', 'weaponry', 'bomb', 'shelling', 'shell', 'warship', 'duel', 'dioxin', 'artillery'],
    'Country and City': ['Russia', 'Ukraine', 'Luhansk', 'Washington'],
    'Non-military Conflicting Parties': ['separatist', 'resistance', 'actor', 'rebel', 'nationalist', 'hacker', 'enemy', 'ally', 'Nazis', 'whistleblower', 'side'],
}




# Assuming `model` is your word2vec model or similar
display_pca_scatterplot(word_vectors, word_groups)
