import statsmodels.stats.power as smp

# File paths
input_file = 'cohen.txt'
output_file = 'sample_size_Ukr.txt'

# Desired power level, significance level, and degree of freedom
power = 0.8
alpha = 0.05

# Read Cohen's w scores from the input file
cohen_w_scores = []
with open(input_file, 'r') as file:
    for line in file:
        cohen_w_scores.append(float(line.strip()))

# Calculate the required sample sizes
sample_sizes = []
for w in cohen_w_scores:
    sample_size = smp.GofChisquarePower().solve_power(effect_size=w, power=power, alpha=alpha)
    sample_sizes.append(sample_size)

# Write sample sizes to the output file
with open(output_file, 'w') as file:
    for size in sample_sizes:
        file.write(f"{int(size)}\n")

print("Sample sizes calculated and saved to sample_size.txt.")
