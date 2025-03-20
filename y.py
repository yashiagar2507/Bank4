import joblib
import numpy as np

fraud_model = joblib.load("fraud_detection.pkl")

# ✅ Test AI Prediction for Various Request Rates
test_inputs = [[1], [5], [10], [20], [50], [55], [100]]
for test in test_inputs:
    prediction = fraud_model.predict(np.array([test]))
    print(f"Prediction for {test[0]} requests/sec: {prediction[0]}")
