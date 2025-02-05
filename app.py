from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from urllib.parse import urlparse
from url_features import extract_features
from helpers import sanitize_url, is_whitelisted, is_reported, is_blocklisted
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Load the TensorFlow model
model = tf.keras.models.load_model('./phishing_model3')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        url = sanitize_url(data['url'])

        if is_reported(url):
            print('reporteeed', url)
            return jsonify({
                'prediction': 0.0,
                'status': 'Reported'
            })

        # Check if the URL is in the whitelist
        if is_whitelisted(url):
            return jsonify({
                'prediction': 0.0,
                'status': 'Safe'
            })
        
        # Check if the URL is in the whitelist
        if is_blocklisted(url):
            return jsonify({
                'prediction': 1.0,
                'status': 'Malicious'
            })

        # Extract features from the URL
        features = extract_features(url)

        # Log extracted features
        print(f'Extracted features for {url}: {features}')

        # Prepare features for model input
        features = tf.convert_to_tensor([features])  # Convert to tensor

        # Make prediction
        prediction = model.predict(features)
        result = prediction[0][0]  # Assuming binary classification
        print(f'Prediction for {url}: {result}')

        # Return response
        return jsonify({
            'prediction': float(result),
            'status': 'Malicious' if result >= 0.5 else 'Safe'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
