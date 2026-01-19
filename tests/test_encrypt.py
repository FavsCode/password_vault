"""test_encrypt.py - Tests for encrypt.py functionalities."""
from vault.encrypt import encrypt, verify, simple_encrypt, simple_decrypt


def test_encrypt_and_verify():
    correct_example_password = "abcdefg"
    incorrect_example_password = "higklmno"

    salt, hashed = encrypt(correct_example_password)
    correct_pass = verify(correct_example_password, salt1 = salt, stored_hash = hashed, testing = True)
    incorrect_pass = verify(incorrect_example_password, salt1 = salt, stored_hash = hashed, testing = True)

    assert correct_pass
    assert not incorrect_pass

def test_simple_encrypt_and_simple_decrypt():
    example_password = "123456"

    encrypted_pass = simple_encrypt(example_password)
    decrypted_pass = simple_decrypt(encrypted_pass)

    assert decrypted_pass == example_password
