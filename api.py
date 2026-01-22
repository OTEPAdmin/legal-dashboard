from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
import pandas as pd
import os

# --- CONFIGURATION ---
app = FastAPI(
    title="OTEP Data API", 
    description="API for exchanging dashboard data with external systems.",
    version="1.0.0"
)

# SECURITY: Systems must provide this key in the header "X-API-KEY"
API_KEY_NAME = "X-API-KEY"
API_KEY_SECRET = "otep-secret-2025" # ⚠️ Change this to a real secret in production

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Path to the same Excel file used by the Dashboard
DATA_FILE = os.path.join("data", "otep_data_saved.xlsx")

# --- HELPER FUNCTIONS ---

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Validates the API Key."""
    if api_key_header == API_KEY_SECRET:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def load_data(sheet_name):
    """Reads Excel and converts to JSON-friendly list."""
    if not os.path.exists(DATA_FILE):
        return None
    try:
        # Read Excel
        df = pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        
        # Ensure Year is string (to match dashboard logic)
        if 'Year' in df.columns:
            df['Year'] = df['Year'].astype(str)
            
        # Convert NaN (empty cells) to None (null in JSON)
        df = df.where(pd.notnull(df), None)
        
        # Return as list of dictionaries
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading {sheet_name}: {e}")
        return None

# --- API ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "OTEP Data API is running. Access documentation at /docs"}

@app.get("/api/v1/eis", dependencies=[Depends(get_api_key)])
def get_eis():
    """Get Executive Summary Data"""
    data = load_data("EIS_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}

@app.get("/api/v1/procurement", dependencies=[Depends(get_api_key)])
def get_procurement():
    """Get Procurement & Inventory Data"""
    data = load_data("Procure_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}

@app.get("/api/v1/finance", dependencies=[Depends(get_api_key)])
def get_finance():
    """Get Financial Position Data"""
    data = load_data("Finance_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}

@app.get("/api/v1/treasury", dependencies=[Depends(get_api_key)])
def get_treasury():
    """Get Treasury Data"""
    data = load_data("Treasury_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}

@app.get("/api/v1/welfare", dependencies=[Depends(get_api_key)])
def get_welfare():
    """Get Welfare Data"""
    data = load_data("Welfare_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}

@app.get("/api/v1/dorm", dependencies=[Depends(get_api_key)])
def get_dorm():
    """Get Dormitory Data"""
    data = load_data("Dorm_Data")
    if data is None: raise HTTPException(status_code=404, detail="Data not found")
    return {"count": len(data), "data": data}
