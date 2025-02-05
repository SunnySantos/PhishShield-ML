import tensorflow as tf
import numpy as np
from url_features import extract_features
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import mysql.connector
import schedule
import time

def extract_url_features(urls):
    features = []
    for url in urls:
        features.append(extract_features(url))
    return np.array(features)

def train_model():
    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phishshield"
    )

    cursor = db.cursor()

    cursor.execute("SELECT url FROM allowlist")
    safe_urls = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT url FROM blocklist")
    malicious_urls = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db.close()

    safe_features = extract_url_features(safe_urls)
    malicious_features = extract_url_features(malicious_urls)

    features = np.vstack((safe_features, malicious_features))
    labels = np.array([0] * len(safe_urls) + [1] * len(malicious_urls))

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation='relu', input_shape=(15,)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=20, min_delta=0.01, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=20, min_lr=1e-6)

    model.fit(features, labels, epochs=200, verbose=1, validation_split=0.2,
              callbacks=[early_stopping, reduce_lr])

    model.save('C:/Users/Renz/Documents/machine-learning/phishing_model3.keras')
    print("Model trained and saved successfully.")

# Train the model every 10:00 AM
schedule.every().day.at("10:00").do(train_model)

while True:
    schedule.run_pending()
    time.sleep(1)