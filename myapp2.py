import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "/Users/jensinewagner/Desktop/senior/mobyphish/mobydata/myapp_itemdump.csv"
data = pd.read_csv(file_path)
print(data.columns)

# Load the dataset
file_path = "/Users/jensinewagner/Desktop/senior/mobyphish/mobydata/extension-rounds.csv"
data2 = pd.read_csv(file_path)
print(data2.columns)

# Load the dataset
file_path = "/Users/jensinewagner/Desktop/senior/mobyphish/mobydata/myapp_user.csv"
data3 = pd.read_csv(file_path)
print(data3.columns)


print("First few rows of 'data' (user_id):")
print(data[['user_id']].head())
print("First few rows of 'data3' (user_id):")
print(data3[['id']].head())

# Convert the columns to the same data type if needed
data['user_id'] = data['user_id'].astype(str)
data3['id'] = data3['id'].astype(str)
# Now, merge
data_merged = data.merge(data3, left_on='user_id', right_on='id', how='left')
print("Columns in data_merge:", data_merged.columns)
# Check the columns in data_merged to ensure no duplicates after the merge
print("Columns in data_merged after merge:", data_merged.columns)
# Check the first few rows of user_id_y in data_merged to verify it
print("First few rows of 'user_id_y' in data_merged:")
print(data_merged[['user_id_y']].head())
# Check if the format matches for the user_id_y and userID columns
print("First few rows of 'userID' in data2:")
print(data2[['userID']].head())


# Strip whitespace and convert to lowercase to ensure matching format
data_merged['user_id_y'] = data_merged['user_id_y'].str.strip().str.lower()
data2['userID'] = data2['userID'].str.strip().str.lower()

# Check if the columns are now in the same format
print("checking")
print(data_merged['user_id_y'].head())
print(data2['userID'].head())

# Merge with the cleaned data
final_data = data_merged.merge(data2, left_on='user_id_y', right_on='userID', how='left')
# Check for any NaN values in the 'use_extension_round_1' and 'use_extension_round_2' columns
print("Checking for NaN values in merged columns:")
print(final_data[['use_extension_round_1', 'use_extension_round_2']].isna().sum())

# Check for common user IDs between data_merged and data2
common_ids = set(data_merged['user_id_y']).intersection(set(data2['userID']))
print("Number of common user IDs:", len(common_ids))
print("Some of the common user IDs:", list(common_ids)[:20])  # print first 20 common IDs

# Filter final_data to show only rows with matching user IDs
matching_user_data = final_data[final_data['user_id_y'].isin(common_ids)]
# Display the relevant columns for those matching user IDs
print(matching_user_data[['user_id_y', 'use_extension_round_1', 'use_extension_round_2']])
unique_user_ids = matching_user_data['user_id_y'].unique()
print(unique_user_ids)
print(matching_user_data.columns)

# Convert Unix timestamps to datetime (assuming they are in seconds since the Unix epoch)
matching_user_data["time_start"] = pd.to_datetime(matching_user_data["time_start"], unit='s', errors="coerce")
matching_user_data["time_end"] = pd.to_datetime(matching_user_data["time_end"], unit='s', errors="coerce")
# Check if the conversion worked correctly
print(matching_user_data[["time_start", "time_end"]].head())
# Calculate task duration and convert it to seconds
matching_user_data["task_duration"] = (matching_user_data["time_end"] - matching_user_data["time_start"]).dt.total_seconds()
print(matching_user_data[["task_duration"]].head())

#ANALYSIS!!!
#mean, median, min, max, and percentiles for task duration
print("Summary Statistics for Task Duration:")
print(matching_user_data["task_duration"].describe())

#Extension vs. No Extension Success Rate
# Round 1
success_with_ext_round_1 = matching_user_data[matching_user_data["use_extension_round_1"] == True]["result"].value_counts(normalize=True) * 100
success_without_ext_round_1 = matching_user_data[matching_user_data["use_extension_round_1"] == False]["result"].value_counts(normalize=True) * 100
# Round 2
success_with_ext_round_2 = matching_user_data[matching_user_data["use_extension_round_2"] == True]["result"].value_counts(normalize=True) * 100
success_without_ext_round_2 = matching_user_data[matching_user_data["use_extension_round_2"] == False]["result"].value_counts(normalize=True) * 100
print("Success Rate with Extension (Round 1):")
print(success_with_ext_round_1)
print("Success Rate without Extension (Round 1):")
print(success_without_ext_round_1)
print("Success Rate with Extension (Round 2):")
print(success_with_ext_round_2)
print("Success Rate without Extension (Round 2):")
print(success_without_ext_round_2)

# Success rate for phishing sites with and without extension
success_phish_ext_round_1 = matching_user_data[(matching_user_data["use_extension_round_1"] == True) & (matching_user_data["phish"] == "t")]["result"].value_counts(normalize=True) * 100
success_phish_no_ext_round_1 = matching_user_data[(matching_user_data["use_extension_round_1"] == False) & (matching_user_data["phish"] == "t")]["result"].value_counts(normalize=True) * 100
success_phish_ext_round_2 = matching_user_data[(matching_user_data["use_extension_round_2"] == True) & (matching_user_data["phish"] == "t")]["result"].value_counts(normalize=True) * 100
success_phish_no_ext_round_2 = matching_user_data[(matching_user_data["use_extension_round_2"] == False) & (matching_user_data["phish"] == "t")]["result"].value_counts(normalize=True) * 100
# Success rate for non-phishing sites with and without extension
success_non_phish_ext_round_1 = matching_user_data[(matching_user_data["use_extension_round_1"] == True) & (matching_user_data["phish"] == "f")]["result"].value_counts(normalize=True) * 100
success_non_phish_no_ext_round_1 = matching_user_data[(matching_user_data["use_extension_round_1"] == False) & (matching_user_data["phish"] == "f")]["result"].value_counts(normalize=True) * 100
success_non_phish_ext_round_2 = matching_user_data[(matching_user_data["use_extension_round_2"] == True) & (matching_user_data["phish"] == "f")]["result"].value_counts(normalize=True) * 100
success_non_phish_no_ext_round_2 = matching_user_data[(matching_user_data["use_extension_round_2"] == False) & (matching_user_data["phish"] == "f")]["result"].value_counts(normalize=True) * 100
# Print results
print("Success Rate for Phishing Sites (Round 1, with Extension):")
print(success_phish_ext_round_1)
print("Success Rate for Phishing Sites (Round 1, without Extension):")
print(success_phish_no_ext_round_1)
print("Success Rate for Phishing Sites (Round 2, with Extension):")
print(success_phish_ext_round_2)
print("Success Rate for Phishing Sites (Round 2, without Extension):")
print(success_phish_no_ext_round_2)
print("Success Rate for Non-Phishing Sites (Round 1, with Extension):")
print(success_non_phish_ext_round_1)
print("Success Rate for Non-Phishing Sites (Round 1, without Extension):")
print(success_non_phish_no_ext_round_1)
print("Success Rate for Non-Phishing Sites (Round 2, with Extension):")
print(success_non_phish_ext_round_2)
print("Success Rate for Non-Phishing Sites (Round 2, without Extension):")
print(success_non_phish_no_ext_round_2)









