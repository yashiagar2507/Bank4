from fastapi import FastAPI, HTTPException, Depends, Request
import redis
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Load Pretrained AI Model (Dynamic Rate Limiting)
fraud_model = joblib.load("fraud_detection.pkl")  # Load the AI model

# Connect to Redis for request tracking
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Base Rate Limit Settings
BASE_RATE_LIMIT = 5  # Default max 5 requests per second
TIME_WINDOW = 1  # 1 second (per user)

# AI-Powered Rate Limiting Middleware
async def ai_rate_limiter(request: Request):
    user_ip = request.client.host
    key = f"rate_limit:{user_ip}"

    # ✅ Check if User is Already Blocked
    if redis_client.get(f"blocked:{user_ip}"):
        raise HTTPException(status_code=429, detail="🚨 AI detected abnormal traffic. User permanently blocked!")

    # ✅ Fetch Request Count
    request_count = redis_client.get(key)
    request_count = int(request_count) if request_count else 0

    # ✅ AI-Based Detection (Check Before Redis)
    features = np.array([[request_count]])
    is_suspicious = fraud_model.predict(features)[0]  # 1 = Suspicious, 0 = Normal

    if is_suspicious == 1:
        redis_client.setex(f"blocked:{user_ip}", 1800, 1)  # Block for 30 minutes
        raise HTTPException(status_code=429, detail="🚨 AI detected abnormal traffic. User permanently blocked!")

    # ✅ Apply Standard Rate Limiting AFTER AI Detection
    if request_count >= BASE_RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    # ✅ Increment Request Count
    redis_client.incr(key, 1)
    redis_client.expire(key, TIME_WINDOW)  # Reset after 1 second

# Apply AI Rate Limiting to Transactions
@app.post("/transactions/credit", dependencies=[Depends(ai_rate_limiter)])
async def credit_transaction():
    return {"message": "Credit transaction processed successfully"}

@app.post("/transactions/debit", dependencies=[Depends(ai_rate_limiter)])
async def debit_transaction():
    return {"message": "Debit transaction processed successfully"}

# Health Check Endpoint
@app.get("/")
async def root():
    return {"message": "AI-Powered Rate Limiting Enabled API"}
