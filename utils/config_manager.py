import json
import os

CONFIG_FILE = "data/visibility_settings.json"

# Define default features inside pages that can be toggled
DEFAULT_FEATURES = {
    "EIS_Executive_Summary": True,
    "EIS_Demographics": True,
    "EIS_Death_Stats": True,
    "EIS_Financials": True
}

def load_visibility_settings():
    """Loads the visibility config from JSON."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists(CONFIG_FILE):
        # Create default structure
        default_data = {
            "dashboards": {}, # Will store "Dashboard Name": True/False
            "features": DEFAULT_FEATURES
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Ensure features key exists if file is old
            if "features" not in data:
                data["features"] = DEFAULT_FEATURES
            return data
    except:
        return {"dashboards": {}, "features": DEFAULT_FEATURES}

def save_visibility_settings(settings):
    """Saves the config to JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f)

def is_dashboard_visible(name, user_role):
    """
    Checks if a dashboard should be shown in the sidebar.
    Admins ALWAYS see everything (but maybe marked hidden).
    """
    settings = load_visibility_settings()
    is_visible = settings["dashboards"].get(name, True) # Default to Visible
    
    if user_role == "Admin":
        return True, is_visible # Admin sees it, plus knows status
    return is_visible, is_visible

def is_feature_visible(feature_key):
    """Checks if a specific graph/section is visible."""
    settings = load_visibility_settings()
    return settings["features"].get(feature_key, True)
