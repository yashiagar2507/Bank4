import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# ✅ Better Training Data (Detect 50+ Requests as Suspicious)
X_train = np.array([
    [1], [2], [3], [4], [5], [6], [7], [8], [9], [10],  # Normal traffic
    [15], [20], [25], [30], [35], [40], [45], [50],  # High but should be marked safe
    [55], [60], [70], [80], [90], [100], [150], [200], [300], [500], [1000]  # Suspicious
])  

y_train = np.array([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Normal requests
    0, 0, 0, 0, 0, 0, 0, 1,  # Start flagging at 50 requests/sec
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1  # 55+ Requests = Attackers
])

# ✅ Train a Random Forest Model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# ✅ Save Updated AI Model
joblib.dump(model, "fraud_detection.pkl")
print("🚀 AI model updated: Now blocking 50+ requests/sec")
