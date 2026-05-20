import hashlib
import db_helper


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    if len(username) < 3:
        return "Username must be at least 3 characters."
    if len(password) < 6:
        return "Password must be at least 6 characters."
    if db_helper.get_user_by_username(username):
        return "Username already taken. Please choose another."
    if db_helper.get_user_by_email(email):
        return "Email already registered. Please login."
    db_helper.create_user(username, email, hash_password(password))
    return "ok"


def login_user(username, password):
    user = db_helper.get_user_by_username(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None
