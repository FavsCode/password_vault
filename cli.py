"""cli.py - Runs the program and handles the visuals of the Password Vault."""
import getpass
from vault.password import generate_password
from vault.encrypt import encrypt, verify
from vault.account import view_accounts, add_account, delete_account, save_account, username_exists
from vault.utils import divider
  
def main():
  print("Welcome to the Password Vault.")
  print("An application that stores all of your account data.")
  
  divider()
  print("(Y/N)")
  no_pass = input("Is this your first time using the Password Vault? ")
  divider()

  # Create account and master password for first-timers
  if no_pass.lower() == "y" or no_pass.lower() == "yes":
    while True: # Repeat process 'till entered username is unique
      print("REMEMBER THIS USERNAME.\n")
      username = input("Enter a username: ")
      divider()
      
      # Check if the username is already in use
      if username_exists(username):
        print("That username is already taken.")
        divider()
        continue
      else:
        break # Only reachable if username is unique
        
    print("(Y/N)")
    custom = input("Would you like to create a custom master password? ")
    divider()
    
    print("WARNING:")
    print("THIS PASSWORD WILL ONLY BE DISPLAYED ONCE. COPY AND STORE THIS PASSWORD.")
    if custom.strip().lower() == "y" or custom.strip().lower() == "yes":
      master_pass = input("Enter your custom master password: ")
      salt, hashed_pass = encrypt(master_pass)
      user_data = {"salt": salt, "hashed_pass": hashed_pass, "accounts": {}} # Account format -> username:password
      save_account(user_data, username)
      return # Just like quit()
    else:
      master_pass = generate_password(16)
      print(master_pass)
      salt, hashed_pass = encrypt(master_pass)
      user_data = {"salt": salt, "hashed_pass": hashed_pass, "accounts": {}} # Account format -> username:password
      save_account(user_data, username)
      return # Just like quit()
      
  # Not their first time? Check their credentials
  username = input("Enter your username: ")
  print("\nYour password won't show up for security.") # Italicize this or something later
  input_pass = getpass.getpass("Enter your master password to continue: ")
  correct_pass = verify(input_pass, username = username)
  divider()
  
  if not correct_pass:
    print("\nINCORRECT USERNAME OR PASSWORD")
    return # Just like quit()

  # The actual program
  print(f"Welcome back, {username}!\n")
  
  while True: # Runs until user chooses to exit the program.
    print("[Vault Menu]")
    print("\nOptions:")
    print("1. View Accounts\n2. Add new account\n3. Delete an account\n4. Close Application")
    action = input("\nChoose an option by its number(1-4): ")
    divider()
    
    if action.strip() == "1":
      view_accounts(username)
      divider()
    if action.strip() == "2":
      site = input("What site is this account from? ")
      account_user = input("\nWhat is the username? ")
      password = input("The password? ")
      add_account(username, site, account_user, password)
      divider()
      print("Account Added!")
      divider()
    if action.strip() == "3":
      site = input("Which site's account data would you like to delete? ").strip().lower()
      delete_account(username, site)
      divider()
    if action.strip() == "4":
      print("Goodbye.")
      return
    