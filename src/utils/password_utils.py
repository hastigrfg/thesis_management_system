import hashlib
import secrets

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password, salt

def verify_password(password, hashed_password, salt):
    new_hash, _ = hash_password(password, salt)
    return new_hash == hashed_password
