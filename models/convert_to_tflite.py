# models/convert_to_tflite.py
# Run with: python models/convert_to_tflite.py
import tensorflow as tf
import numpy as np
import os

# Load the trained model
model = tf.keras.models.load_model('models/anomaly_detector.h5')

# Representative dataset generator for quantization
# The converter needs to see some sample data to know how to scale the numbers
def representative_data_gen():
    # Load some data from the CSV we just made
    data = np.loadtxt("models/sample_data.csv", delimiter=",", skiprows=1, usecols=[0])
    for i in range(100):
        # Yield a single sample reshaped to (1, 1)
        yield [data[i].reshape(1, 1).astype(np.float32)]

# Configure the converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# Convert
tflite_model = converter.convert()

# Save
output_path = "firmware/esp32/data/model.tflite"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'wb') as f:
    f.write(tflite_model)

print(f"Quantized model saved to {output_path}")
print(f"Model Size: {len(tflite_model)} bytes")