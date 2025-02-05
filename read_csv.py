import numpy as np
import pandas as pd
from url_features import extract_features

def extract_url_features(urls):
    features = []

    for url in urls:
        extracted_features = extract_features(url)

        # Append extracted features
        features.append(extracted_features)
    
    return np.array(features)


# Load the CSV file for malicious URLs
csv_file_path = 'malicious_phish2.csv'  # Change this to your file path
data = pd.read_csv(csv_file_path)

# Get all benign URLs from the CSV
benign_urls = data[data['type'] == 'benign']['url'].tolist()

# Safe URLs
safe = [
    'https://www.facebook.com',
    'https://www.google.com',
    'https://www.youtube.com',
]

# Add all benign URLs to the safe array
safe.extend(benign_urls)

# Get all malicious URLs (both phishing and defacement) from the CSV
malicious_urls = data[data['type'].isin(['phishing', 'defacement'])]['url'].tolist()

# Extract features for safe URLs
safe_features = extract_url_features(safe)

# Extract features for malicious URLs
malicious_features = extract_url_features(malicious_urls)

# Example of combining features and labels
labels = np.array([0] * len(safe) + [1] * len(malicious_urls))  # 0 = Safe, 1 = Malicious
features = np.vstack((safe_features, malicious_features))

print(labels)
print(features)