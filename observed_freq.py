import pandas as pd

# Read the data from the file
data = pd.read_csv('observed_freq.txt', sep='\t')

# Calculate total occurrences from the sum of the fourth column
n = data['O(sy_vy)'].sum()

# Initialize the lists to store results
subject_verb_pairs = []
subjects = []
verbs = []
observed_frequencies = []
b_values = []
c_values = []
d_values = []
row_totals = []

# Calculate b and c for each row
for index, row in data.iterrows():
    pair = row['Subject_Verb_Pairs']
    subject = row['s']
    verb = row['v']
    a = row['O(sy_vy)']

    # Calculate b: occurrences where the subject is present but the verb is absent
    b = data[data['s'] == subject]['O(sy_vy)'].sum() - a
    
    # Calculate c: occurrences where the verb is present but the subject is absent
    c = data[data['v'] == verb]['O(sy_vy)'].sum() - a
    
    # Calculate d: occurrences where neither the subject nor the verb are present
    d = n - (a + b + c)
    
    # Calculate row total
    row_total = a + b + c + d

    # Append the results to the lists
    subject_verb_pairs.append(pair)
    subjects.append(subject)
    verbs.append(verb)
    observed_frequencies.append(a)
    b_values.append(b)
    c_values.append(c)
    d_values.append(d)
    row_totals.append(row_total)

# Create a DataFrame with the results
results_df = pd.DataFrame({
    'Subject_Verb_Pairs': subject_verb_pairs,
    's': subjects,
    'v': verbs,
    'O(sy_vy)': observed_frequencies,
    'O(sy_vn)': b_values,
    'O(sn_vy)': c_values,
    'O(sn_vn)': d_values,
    'total': row_totals
})

# Write the DataFrame to a tab-delimited text file
results_df.to_csv('observed_freq_active_tmct.txt', sep='\t', index=False)
