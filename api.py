from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
import pandas as pd
import os
import json

# --- CONFIGURATION ---
app = FastAPI(title="OTEP Data API", version="1.1.0")

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

DATA_FILE = os.path.join("data", "otep_data_saved.xlsx")
KEYS_FILE = "api_keys.json" # Shared key file

# --- SECURITY HELPER ---
def get_valid_keys():
    """Loads active keys from the JSON file."""
    if not os.path.exists(KEYS_FILE):
        return []
    try:
        with open(KEYS_FILE, "r") as f:
            data = json.load(f)
            return list(data.keys())
    except:
        return []

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Validates if the provided key exists in our database."""
    valid_keys = get_valid_keys()
    
    # Also keep the master secret as a fallback if needed (Optional)
    # if api_key_header == "otep-secret-2025": return api_key_header
    
    if api_key_header in valid_keys:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid or Missing API Key")

# --- DATA HELPER ---
def load_data(sheet_name):
    if not os.path.exists(DATA_FILE):
        return None
    try:
        df = pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        if 'Year' in df.columns: df['Year'] = df['Year'].astype(str)
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading {sheet_name}: {e}")
        return None

# --- ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "OTEP API Active. Authentication required."}

@app.get("/api/v1/eis", dependencies=[Depends(get_api_key)])
def get_eis():
    return {"data": load_data("EIS_Data")}

@app.get("/api/v1/procurement", dependencies=[Depends(get_api_key)])
def get_procure():
    return {"data": load_data("Procure_Data")}

@app.get("/api/v1/finance", dependencies=[Depends(get_api_key)])
def get_finance():
    return {"data": load_data("Finance_Data")}

@app.get("/api/v1/treasury", dependencies=[Depends(get_api_key)])
def get_treasury():
    return {"data": load_data("Treasury_Data")}

@app.get("/api/v1/welfare", dependencies=[Depends(get_api_key)])
def get_welfare():
    return {"data": load_data("Welfare_Data")}

@app.get("/api/v1/dorm", dependencies=[Depends(get_api_key)])
def get_dorm():
    return {"data": load_data("Dorm_Data")}
