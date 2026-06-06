from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UserSignup, UserLogin, ParcelCreateRequest, AuditRunRequest
from app.database import FAKE_USER_DATABASE
import uuid
import random

app = FastAPI(title="EcoAudit-AI Core Backend Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PARCEL & AUDIT LOGIC (Moved from routes.py) ---
@app.post("/api/parcels", tags=["Audit & Parcels"])
async def create_parcel(payload: ParcelCreateRequest):
    simulated_area = round(random.uniform(100.0, 5000.0), 2)
    return {"status": "success", "parcel_id": str(uuid.uuid4()), "calculated_area_hectares": simulated_area}

@app.post("/api/audit/run", tags=["Audit & Parcels"])
async def trigger_audit(payload: AuditRunRequest):
    return {"audit_id": str(uuid.uuid4()), "status": "Processing", "message": "Triggering ML pipeline."}

# --- AUTH LOGIC ---
@app.post("/api/auth/signup", tags=["Auth"])
def signup_user(user_data: UserSignup):
    if user_data.username in FAKE_USER_DATABASE:
        raise HTTPException(status_code=400, detail="Username already registered.")
    FAKE_USER_DATABASE[user_data.username] = {"email": user_data.email, "password": user_data.password}
    return {"status": "success", "message": "User registered successfully!"}

@app.post("/api/auth/login", tags=["Auth"])
def login_user(user_data: UserLogin):
    if user_data.username not in FAKE_USER_DATABASE or FAKE_USER_DATABASE[user_data.username]["password"] != user_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    return {"status": "success", "message": "Login verified!"}