import pandas as pd

safe = ['https://www.facebook.com', 'https://www.google.com', 'https://www.youtube.com']

# Load the CSV file
df = pd.read_csv('malicious_phish2.csv')

# Count occurrences of each value in the 'type' column
count_by_type = df['type'].value_counts()

# Print the result
print(count_by_type)

# Get the count of each type
malware_count = count_by_type.get('malware', 0)
defacement_count = count_by_type.get('defacement', 0)
phishing_count = count_by_type.get('phishing', 0)
benign_count = count_by_type.get('benign', 0)

print(f"Malware count: {malware_count}")
print(f"Defacement count: {defacement_count}")
print(f"Phishing count: {phishing_count}")
print(f"Benign count: {benign_count}")

# Calculate the total count of defacement, phishing, and malware
total_target_count = defacement_count + phishing_count + malware_count + len(safe)

# Separate each class into different DataFrames
benign_df = df[df['type'] == 'benign']
defacement_df = df[df['type'] == 'defacement']
phishing_df = df[df['type'] == 'phishing']
malware_df = df[df['type'] == 'malware']

# Randomly sample the benign class to match the total count of other classes
if benign_count > total_target_count:
    benign_sampled_df = benign_df.sample(n=total_target_count, random_state=42)
else:
    benign_sampled_df = benign_df  # Keep all benign if it's less than or equal to the target count

# Concatenate the balanced data back together
balanced_df = pd.concat([benign_sampled_df, defacement_df, phishing_df, malware_df])

# Optionally, shuffle the dataset
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the balanced dataset to a new CSV file
balanced_df.to_csv('balanced_dataset.csv', index=False)

print("Dataset balanced and saved as 'balanced_dataset.csv'")
