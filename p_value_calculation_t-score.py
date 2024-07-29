# Import the necessary library
from scipy.stats import t
import numpy as np

# Read t-scores from file
with open('t_score.txt', 'r') as file:
    t_scores = [float(line.strip()) for line in file]

# Degrees of freedom
df = 1

# Calculate p-values for each t-score
p_values = [t.sf(abs(t_score), df) * 2 for t_score in t_scores]  # Multiply by 2 for two-tailed test

# Write only the p-values to a new file
with open('t_score_p_value_results.txt', 'w') as file:
    for p_value in p_values:
        file.write(f"{p_value:.17f}\n")

