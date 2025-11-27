# Password Vault

A secure command-line password manager written in Python.
Users can create a master account, store encrypted passwords, and manage saved accounts safely.

## Features
- Master account system (first-time setup automatically creates master credentials)
- SHA-256 hashing for master password verification
- Fernet symmetric encryption for individual account passwords
- Add, view, and delete stored accounts
- JSON-based persistent storage
- Modular project structure for readability and future upgrades

## Installation
1. Clone or download the repository:

```bash
git clone https://github.com/FavsCode/password_vault.git
cd password_vault
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```
Windows:

    venv\Scripts\activate
Mac/Linux:

    source venv/bin/activate
3. Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage

Run the application from the project root:
```bash
python main.py
```

Actions include:
- Creating a master account (first launch)
- Logging in
- Adding accounts
- Viewing saved logins
- Deleting accounts

## Project Structure
```bash
password_vault/
│
├── data/
│   ├── users.json         # Stores master account + saved accounts, created upon use
│   └── vault.key          # Fernet encryption key, created upon use
│
├── vault/
│   ├── __init__.py
│   ├── account.py         # Add/view/delete password entries
│   ├── encrypt.py         # Encryption + decryption helpers
│   ├── password.py        # Generates random secure passwords
│   └── utils.py           # Shared helper utilities
│
├── main.py                # Entry point for the application
├── requirements.txt
├── README.md
└── .gitignore
```

## Security Notes
- The vault key and user database are intentionally ignored by Git.
- Never share or sync your vault.key.
- This tool is for local use only and should not be considered a full enterprise-grade password manager.
