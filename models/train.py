# models/train.py
# Run with: python models/train.py
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import os

# 1. Generate Synthetic Data
# Normal data: Vibration between 0.0 and 0.5
# Anomaly data: Vibration between 2.0 and 5.0
print("Generating synthetic dataset...")
n_samples = 2000
normal_data = np.random.uniform(0.0, 0.5, size=(n_samples, 1))
anomaly_data = np.random.uniform(2.0, 5.0, size=(int(n_samples*0.1), 1))

# Labels: 0 = Normal, 1 = Anomaly
X = np.vstack((normal_data, anomaly_data)).astype(np.float32)
y = np.hstack((np.zeros(len(normal_data)), np.ones(len(anomaly_data)))).astype(np.float32)

# Save as CSV for reference
df = pd.DataFrame(X, columns=['vibration'])
df['label'] = y
df.to_csv("models/sample_data.csv", index=False)
print("Data saved to models/sample_data.csv")

# 2. Build a Tiny Model
# A very simple Autoencoder or Classifier. We'll use a simple Classifier for MVP.
model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(1,)),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid') # Output probability of anomaly
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. Train
print("Training model...")
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

# 4. Save Keras Model
model.save('models/anomaly_detector.h5')
print("Keras model saved to models/anomaly_detector.h5")