import scipy.stats as stats
import csv

# Define file paths
input_file = 'fisher.txt'
output_file = 'p_value_fisher_14.txt'

# Read data from the input file
data = []
with open(input_file, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    header = next(reader)  # Skip header
    for row in reader:
        data.append(row)

# Calculate Fisher's Exact Test p-values
p_values = []
for row in data:
    a = int(row[1])
    b = int(row[2])
    c = int(row[3])
    d = int(row[4])
    
    contingency_table = [[a, b], [c, d]]
    _, p_value = stats.fisher_exact(contingency_table)
    
    p_values.append(p_value)

# Write p-values to the output file
with open(output_file, 'w') as file:
    for p_value in p_values:
        file.write(f"{p_value:.17f}\n")
