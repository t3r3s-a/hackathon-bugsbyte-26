# services/user_service.py

users_db = []

def create_user(user_data: dict):
    # Verifica se já existe
    for u in users_db:
        if u['username'] == user_data['username'] or u['email'] == user_data['email']:
            return False
    users_db.append(user_data)
    return True

def authenticate_user(username: str, password: str):
    for u in users_db:
        if u['username'] == username and u['password'] == password:
            return True
    return False
