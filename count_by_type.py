import pandas as pd

# Load the CSV file
df = pd.read_csv('balanced_dataset.csv')

# Count occurrences of each value in the 'type' column
count_by_type = df['type'].value_counts()

# Print the result
print(count_by_type)

malware_count = count_by_type.get('malware', 0)
print(f"Malware count: {malware_count}")
