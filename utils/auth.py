import json
import os

FILE_PATH = "users.json"

def load_users():
    """Loads users from JSON file. Creates default if missing."""
    if not os.path.exists(FILE_PATH):
        # Default initial users with dummy emails (Change these to real ones to test!)
        default_users = {
            "admin": {
                "password": "admin", 
                "role": "Admin", 
                "name": "Administrator",
                "email": "admin@example.com",
                "allowed_views": []
            },
            "super": {
                "password": "super", 
                "role": "Superuser", 
                "name": "Super User",
                "email": "super@example.com",
                "allowed_views": []
            },
            "user": {
                "password": "user", 
                "role": "User", 
                "name": "General User",
                "email": "user@example.com",
                "allowed_views": ["บทสรุปผู้บริหาร"]
            }
        }
        with open(FILE_PATH, "w", encoding='utf-8') as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
        return default_users
    
    with open(FILE_PATH, "r", encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(FILE_PATH, "w", encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def check_credentials(username, password):
    """Verifies password only. Returns user object if valid, else None."""
    users = load_users()
    if username in users and users[username]["password"] == password:
        # Return the whole user object (so we can get the email)
        user_data = users[username]
        user_data['username'] = username # Append username key for convenience
        return user_data
    return None

def add_user(username, password, role, name, email, allowed_views=None):
    """Adds a new user with email."""
    users = load_users()
    if username in users:
        return False, "⚠️ Username already exists"
    
    users[username] = {
        "password": password,
        "role": role,
        "name": name,
        "email": email,
        "allowed_views": allowed_views if allowed_views else []
    }
    save_users(users)
    return True, "✅ User created successfully!"

def update_password(username, new_password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    users[username]["password"] = new_password
    save_users(users)
    return True, "✅ Password updated!"

def delete_user(username):
    users = load_users()
    if username in users:
        if username == "admin": 
            return False, "⚠️ Cannot delete main Admin"
        del users[username]
        save_users(users)
        return True, "✅ User deleted"
    return False, "User not found"
