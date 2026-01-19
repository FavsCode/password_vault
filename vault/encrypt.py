"""encrypt.py - Handles encryption, decryption, and verification of passwords."""
import json
import os
import hashlib
from cryptography.fernet import Fernet

# ---------- Correct Path Handling ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))         # /vault
DATA_DIR = os.path.join(BASE_DIR, "..", "data")               # /data folder
os.makedirs(DATA_DIR, exist_ok=True)

VAULT_KEY = os.path.join(DATA_DIR, "vault.key")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Create key if missing
if not os.path.exists(VAULT_KEY):
    with open(VAULT_KEY, "wb") as f:
        f.write(Fernet.generate_key())

# ---------- PASSWORD HASHING ----------
def encrypt(password):
    salt = os.urandom(16)
    salt_hex = salt.hex()
    hashed = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt_hex, hashed

def verify(input_pass, username = None, salt1 = None, stored_hash = None, testing = False):
    if not testing:
        if not os.path.exists(USERS_FILE):
            return False

        with open(USERS_FILE, "r") as file:
            users = json.load(file)

        if username not in users:
            return False
        
    if salt1 is  None:
        salt = bytes.fromhex(users[username]["salt"])
    else:
        salt = bytes.fromhex(salt1)

    if stored_hash is None:
        stored_hash = users[username]["hashed_pass"]

    input_hash = hashlib.sha256(salt + input_pass.encode()).hexdigest()
    return input_hash == stored_hash

# ---------- ENCRYPT/DECRYPT STORED PASSWORDS ----------
def simple_encrypt(password):
    with open(VAULT_KEY, "rb") as key_file:
        key = key_file.read()
    return Fernet(key).encrypt(password.encode()).decode()

def simple_decrypt(encrypted_pass):
    with open(VAULT_KEY, "rb") as key_file:
        key = key_file.read()
    return Fernet(key).decrypt(encrypted_pass.encode()).decode()
