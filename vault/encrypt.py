"""encrypt.py - Handles encryption, decryption, and verification of the Password Vault's passwords."""
import json
import os
import hashlib
from cryptography.fernet import Fernet

os.makedirs("data", exist_ok=True)
if not os.path.exists("data/vault.key"):
  with open("data/vault.key", "wb") as f:
      f.write(Fernet.generate_key())

def encrypt(password):
  """A function that encrypts an un-decryptable password (A.K.A. A password no one knows. Not even us!)."""
  # Generate random salt (store it too)
  salt = os.urandom(16)
  salt_hex = salt.hex()

  # Combine password + salt before hashing
  hashed = hashlib.sha256(salt + password.encode()).hexdigest()
  return salt_hex, hashed

def verify(username, input_pass):
  """A function that compares entered credentials against saved ones."""
  try:
    with open("data/users.json", "r") as file:
      users = json.load(file)
      try:
        # Find their info
        salt_hex = users[username]["salt"]
        stored_hash = users[username]["hashed_pass"]
      except KeyError: # If the user doesn't exist, account doesn't
        return False
  except FileNotFoundError: # If the file doesn't exist, the account can't either 
    return False

  # Check if their info resembles what they entered
  salt = bytes.fromhex(salt_hex)
  input_hash = hashlib.sha256(salt + input_pass.encode()).hexdigest() 
  return input_hash == stored_hash
  
def simple_encrypt(password):
  """A function that uses a simple key to encrypt a password."""
  # Load your previously saved key
  with open("data/vault.key", "rb") as key_file:
      key = key_file.read()

  # Use the key to create a Fernet object
  fernet = Fernet(key)
  encrypted_pass = fernet.encrypt(password.encode()).decode() # JSON can't handle bytes, so it must turns into a string (decode)!
  return encrypted_pass

def simple_decrypt(encrypted_pass):
  # Load your previously saved key
  with open("data/vault.key", "rb") as key_file:
      key = key_file.read()

  fernet = Fernet(key)
  decrypted_pass = fernet.decrypt(encrypted_pass.encode()).decode()
  return decrypted_pass
