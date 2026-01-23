import json
import os

FILE_PATH = "users.json"

def save_users(users):
    with open(FILE_PATH, "w", encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_users():
    if not os.path.exists(FILE_PATH):
        default_users = {
            "admin": {
                "password": "admin", 
                "role": "Admin", 
                "name": "Administrator",
                "email": "vforwardth@gmail.com",
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
                "allowed_views": ["สำนัก ช.พ.ค. - ช.พ.ส"]
            }
        }
        save_users(default_users)
        return default_users
    
    with open(FILE_PATH, "r", encoding='utf-8') as f:
        users = json.load(f)

    # Self-Healing
    target_admin_email = "vforwardth@gmail.com"
    if "admin" in users and users["admin"].get("email") != target_admin_email:
        users["admin"]["email"] = target_admin_email
        save_users(users) 

    return users

# (Keep the rest of auth.py exactly the same)
def check_credentials(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]
        user_data['username'] = username
        return user_data
    return None

def add_user(username, password, role, name, email, allowed_views=None):
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

def update_user_details(username, role, name, email, allowed_views):
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    users[username]["role"] = role
    users[username]["name"] = name
    users[username]["email"] = email
    users[username]["allowed_views"] = allowed_views if allowed_views else []
    save_users(users)
    return True, "✅ User updated successfully!"

def update_password(username, new_password):
    users = load_users()
    if username not in users: return False, "User not found"
    users[username]["password"] = new_password
    save_users(users)
    return True, "✅ Password updated!"

def delete_user(username):
    users = load_users()
    if username in users:
        if username == "admin": return False, "⚠️ Cannot delete main Admin"
        del users[username]
        save_users(users)
        return True, "✅ User deleted"
    return False, "User not found"
