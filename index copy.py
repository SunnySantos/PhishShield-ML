import tensorflow as tf
import numpy as np
from urllib.parse import urlparse
import pandas as pd
import re

def extract_url_features(urls):
    features = []

    for url in urls:
        parsed_url = urlparse(url)

        # Feature 1: Length of URL
        url_length = len(url)

        # Feature 2: Number of slashes
        num_slashes = url.count('/')

        # Feature 3: HTTPS check
        use_https = 1 if url.startswith('https') else 0

        # Feature 4: Number of digits
        num_digits = sum(c.isdigit() for c in url)

        # Feature 5: Number of periods
        num_periods = url.count('.')

        # Feature 6: Count of query parameters
        query_params_count = len(re.findall(r'\?.*$', url))

        # Feature 7: Number of subdomains
        domain_parts = parsed_url.netloc.split('.')
        num_subdomains = len(domain_parts) - 2 if len(domain_parts) > 2 else 0
        
        # Feature 8: Presence of special characters
        special_chars = any(char in url for char in ['@', '-', '_', '&', '%', '$', '#', '?', '!', '+'])
        presence_of_special_chars = 1 if special_chars else 0

        domain_age = 0  

        # Append extracted features
        features.append([
            url_length,
            num_slashes,
            use_https,
            num_digits,
            num_periods,
            query_params_count,
            num_subdomains,
            presence_of_special_chars,
            domain_age
        ])
    
    return np.array(features)




# Load the CSV file for malicious URLs
csv_file_path = 'malicious_phish.csv'  # Change this to your file path
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

# Build a more complex neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(9,)),  # Increased neurons
    tf.keras.layers.BatchNormalization(),  # Added batch normalization
    tf.keras.layers.Dropout(0.5),  # Dropout layer to reduce overfitting
    tf.keras.layers.Dense(32, activation='relu'),  # More hidden layers
    tf.keras.layers.BatchNormalization(),  # Another batch normalization
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model with validation split for monitoring
model.fit(features, labels, epochs=100, verbose=1, validation_split=0.2)

# Save the model to TensorFlow.js format
model.save('C:/Users/Renz/Documents/machine-learning/phishing_model1.keras')
