"""password.py - Creates and strengthens the generated master password for the Password Vault."""
import random
import string

def fix_password_strength(password):
  """A function that takes a password and does the neccessary things to make it strong."""
  # Check for uppercase letters
  if not any(char.isupper() for char in password):
    password += random.choice(string.ascii_uppercase)
  # Check for lowercase letters
  if not any(char.islower() for char in password):
    password += random.choice(string.ascii_lowercase)
  # Check for numbers
  if not any(char.isdigit() for char in password):
    password += random.choice(string.digits)
  # Check for special characters
  specials = "!@#$%^&*()"
  if not any(char in specials for char in password):
    password += random.choice(string.punctuation)

  # Character count must be over 8.
  while len(password) < 8:
    password += random.choice(string.ascii_letters)
  return password

def generate_password(length):
  """A function that generates a strong password."""
  password = ""
  while len(password) < length:
    # Choose a random character
    char_choices = [string.ascii_letters, string.digits, string.punctuation]
    char_type = random.choice(char_choices)
    char = random.choice(char_type)
    password += char

  # Check if the password is strong and update accordingly
  password = fix_password_strength(password)
  return password