import scipy.stats as stats

def calculate_p_values(file_path):
    # Read chi-squared test scores from the file
    with open(file_path, 'r') as file:
        chi_squared_scores = [float(line.strip()) for line in file]

    # Calculate p-values for each chi-squared score
    degrees_of_freedom = 1  # Assuming 1 degree of freedom for each test
    p_values = [stats.chi2.sf(score, degrees_of_freedom) for score in chi_squared_scores]

    # Convert p-values to normal numbers with decimals
    p_values_decimal = [f'{p:.17f}' for p in p_values]

    # Write only the p-values to a new file
    with open('chi_squared_p_value_results.txt', 'w') as file:
        for p_value_decimal in p_values_decimal:
            file.write(f"{p_value_decimal}\n")

# File path to the chi-squared test scores
file_path = 'chi-squared_test_score.txt'
calculate_p_values(file_path)
