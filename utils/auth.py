import json
import os

FILE_PATH = "users.json"

def load_users():
    """Loads users from JSON file. Creates default if missing."""
    if not os.path.exists(FILE_PATH):
        # Default initial users
        default_users = {
            "admin": {
                "password": "admin", 
                "role": "Admin", 
                "name": "Administrator",
                "allowed_views": [] # Admin sees all
            },
            "super": {
                "password": "super", 
                "role": "Superuser", 
                "name": "Super User",
                "allowed_views": [] # Superuser sees all dashboards
            },
            "user": {
                "password": "user", 
                "role": "User", 
                "name": "General User",
                "allowed_views": ["บทสรุปผู้บริหาร"] # Default assigned view
            }
        }
        with open(FILE_PATH, "w", encoding='utf-8') as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
        return default_users
    
    with open(FILE_PATH, "r", encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    """Saves the user dictionary to JSON."""
    with open(FILE_PATH, "w", encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def check_login(username, password):
    """Verifies credentials."""
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]
    return None

def add_user(username, password, role, name, allowed_views=None):
    """Adds a new user with specific dashboard access."""
    users = load_users()
    if username in users:
        return False, "⚠️ Username already exists"
    
    users[username] = {
        "password": password,
        "role": role,
        "name": name,
        "allowed_views": allowed_views if allowed_views else []
    }
    save_users(users)
    return True, "✅ User created successfully!"

def update_password(username, new_password):
    """Updates an existing user's password."""
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    users[username]["password"] = new_password
    save_users(users)
    return True, "✅ Password updated!"

def delete_user(username):
    """Deletes a user."""
    users = load_users()
    if username in users:
        if username == "admin": 
            return False, "⚠️ Cannot delete main Admin"
        del users[username]
        save_users(users)
        return True, "✅ User deleted"
    return False, "User not found"
