import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "/Users/jensinewagner/Desktop/senior/mobyphish/mobydata/fulldata.csv"
data = pd.read_csv(file_path)
print(data.columns)

# Load the dataset
file_path = "/Users/jensinewagner/Desktop/senior/mobyphish/mobydata/use_extension.csv"
data2 = pd.read_csv(file_path)
print(data2.columns)

# Merge the datasets on User_ID and userID
merged_data = pd.merge(data, data2, left_on='User_ID', right_on='userID')
# Check the merged data columns to confirm
print(merged_data.columns)

# Filter the data for round_no 1 or 2
cleaned_data = merged_data[merged_data['round_no'].isin([1, 2])]
# Check the shape and a sample of the cleaned data
print(cleaned_data.shape)
print(cleaned_data.head())

# Drop rows with any missing values
cleaned_data = cleaned_data.dropna()
# Check the shape and a sample of the cleaned data
print(cleaned_data.shape)
print(cleaned_data.head())


# Check the result
print(cleaned_data[['time_start', 'time_end']].head())


#ANALYSIS: 
# Filter for phishing attempts only
phishing_data = cleaned_data[cleaned_data['phish'] == 't']

# Success rates for round 1 (using or not using the extension)
round1_success = phishing_data[phishing_data['round_no'] == 1].groupby('use_extension_round_1')['result'].value_counts(normalize=True).unstack()

# Success rates for round 2 (using or not using the extension)
round2_success = phishing_data[phishing_data['round_no'] == 2].groupby('use_extension_round_2')['result'].value_counts(normalize=True).unstack()

# Print results
print("Round 1 Success Rates (Phishing Detection):")
print(round1_success)

print("\nRound 2 Success Rates (Phishing Detection):")
print(round2_success)

# Filter for non-phishing attempts
non_phishing_data = cleaned_data[cleaned_data['phish'] == 'f']

# Success rates for phishing (extension vs no extension)
phishing_round1 = phishing_data[phishing_data['round_no'] == 1].groupby('use_extension_round_1')['result'].value_counts(normalize=True).unstack()
phishing_round2 = phishing_data[phishing_data['round_no'] == 2].groupby('use_extension_round_2')['result'].value_counts(normalize=True).unstack()

# Success rates for non-phishing (extension vs no extension)
non_phishing_round1 = non_phishing_data[non_phishing_data['round_no'] == 1].groupby('use_extension_round_1')['result'].value_counts(normalize=True).unstack()
non_phishing_round2 = non_phishing_data[non_phishing_data['round_no'] == 2].groupby('use_extension_round_2')['result'].value_counts(normalize=True).unstack()

# Print results
print("Phishing Detection Success Rates (with/without Extension):")
print("\nRound 1 (Phishing):")
print(phishing_round1)
print("\nRound 2 (Phishing):")
print(phishing_round2)

print("\nNon-Phishing Success Rates (with/without Extension):")
print("\nRound 1 (Non-Phishing):")
print(non_phishing_round1)
print("\nRound 2 (Non-Phishing):")
print(non_phishing_round2)

