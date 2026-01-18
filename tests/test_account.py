"""test_account.py - Tests for account.py functionalities."""
from copy import Error
import json
import os
from vault.account import view_accounts, add_account, delete_account, save_account, username_exists
from vault.encrypt import simple_encrypt, simple_decrypt
from vault.utils import divider

TEST_FILE = "data/test_users.json"

# Setup
test_data = {
    "testuser": {
        "accounts": {}
    }
}

with open(TEST_FILE, "w") as file:
    json.dump(test_data, file)

def test_view_accounts_no_accounts():
    """Test viewing accounts when there are no saved accounts."""
    result = view_accounts("testuser", path=TEST_FILE)
    assert result == "You have no saved accounts yet."

def test_add_and_view_account():
    """Test adding an account and then viewing it."""
    # Add account
    add_account("testuser", "example.com", "exampleuser", "examplepass", path=TEST_FILE)

    # Test viewing the added account
    result = view_accounts("testuser", "example.com", path=TEST_FILE)
    expected_password = simple_decrypt(simple_encrypt("examplepass"))
    assert result is None  # view_accounts prints directly
    assert result is not "[Error. Site not found.]" # Only reachable if logic doesn't work

def test_delete_account_no_data_and_invalid_site():
    """Test delete_account edge cases."""
    # Reset test file
    test_data = {
        "testuser": {
            "accounts": {}
        }
    }
    with open(TEST_FILE, "w") as file:
        json.dump(test_data, file)

    # Test    
    result_1 = delete_account('testuser', 'notexample.com', path=TEST_FILE)
    # Add account to avoid hitting the first edge case
    add_account("testuser", "example.com", "exampleuser", "examplepass", path=TEST_FILE)
    result_2 = delete_account('testuser', 'notexample.com', path=TEST_FILE)

    assert result_1 == 'You have no saved accounts yet.'
    assert result_2 == '[Error. Site not found.]'

def test_save_account():
    """Test if save_account works."""
    test_user_data = {"salt": "example_salt", "hashed_pass": "example_hashed_pass", "accounts": {}}
    save_account(test_user_data, "testuser", path=TEST_FILE)

    # Test
    with open(TEST_FILE, "r") as file:
      users = json.load(file)

    assert users["testuser"] == test_user_data


def test_username_exists():
    """Test if username_exist works."""
    assert username_exists("testuser", path=TEST_FILE) == True
    assert username_exists("nottestuser", path=TEST_FILE) == False

    # Teardown
    os.remove(TEST_FILE)