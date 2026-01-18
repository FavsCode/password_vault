"""account.py - Handles The Password Vault's interactions with account data."""
import json
import os
from .encrypt import simple_encrypt, simple_decrypt
from .utils import divider
  
def view_accounts(username, site = None, path = None):
  """Displays the user's saved accounts in a clean format.(Made by ChatGPT because it was hard.)"""
  # NOTE: This function prints directly to the console
  # Tests only check the return values for edge cases
  # Refactor later when stdout is learned

  if path is None:
    path = "data/users.json"

  with open(path, "r") as file:
      users = json.load(file)
      accounts = users[username]["accounts"]

  if not accounts:
    print("You have no saved accounts yet.")
    return "You have no saved accounts yet."


  if not site:
    print("─── Saved Accounts ───")

    for site, info in accounts.items():
      try:
          decrypted_pass = simple_decrypt(info["password"])
      except Exception:
          decrypted_pass = "[Error: Could not decrypt]"

      print(f"\nSite: {site}")
      print(f"Username: {info['username']}")
      print(f"Password: {decrypted_pass}")

    print("─────────────────────")
  else: # Made especially for delete_account()
    print("─── Saved Account ───")
    print(f"\nSite: {site}") 

    try:
      for id, info in accounts[site].items():
        if id == "username":
          print(f"Username: {info}")
        elif id == "password":
          try:
            decrypted_pass = simple_decrypt(info)
          except Exception:
            decrypted_pass = "[Error: Could not decrypt]"

          print(f"Password: {decrypted_pass}")
    except Exception:
      print("[Error. Site not found.]")
      return"[Error. Site not found.]"

    print("─────────────────────") 

def add_account(username, site, account_user, password, path = None):
  """A function that adds account info to a user's information."""
  if path is None:
    path = "data/users.json"

  with open(path, "r") as file:
    users = json.load(file)

  users[username]["accounts"][site.strip().lower()] = {
      "username":  account_user,
      "password": simple_encrypt(password) # Keep these passwords safe too!
  }

  with open(path, "w") as file:
    json.dump(users, file, indent=2)

def delete_account(username, site, path = None):
  """A function that deletes account info from a user's information."""
  if path is None:
    path = "data/users.json"

  accounts = view_accounts(username, path=path)
  if accounts == "You have no saved accounts yet.":
    return "You have no saved accounts yet."   
  
  divider()
  found = view_accounts(username, site, path=path)

  if found == "[Error. Site not found.]":
    return "[Error. Site not found.]"

  print("(Y/N)")
  delete = input("Are you sure you want to delete this account? ")

  if delete.strip().lower() == "y" or delete.strip().lower() == "yes":
    with open(path, "r") as file:
      users = json.load(file)

    if site in users[username]["accounts"]:
      del users[username]["accounts"][site]

    with open(path, "w") as file:
      json.dump(users, file, indent=4)

    print("Account Deleted.")

def save_account(user_data, username, path = None):
  """A function that saves users' accounts into a JSON dictionary."""
  users = {}
  if path is None:
    path = "data/users.json"

  if os.path.exists(path):
    with open(path, "r") as file:
      users = json.load(file)

    users[username] = user_data

    with open(path, "w") as file:
      json.dump(users, file, indent=2)

def username_exists(username, path = None):
  """Checks if a username already exists in the users.json file."""
  if path is None:
    path = "data/users.json"

  if os.path.exists(path):
    with open(path, "r") as file:
      users = json.load(file)
    return username in users
  return False
    