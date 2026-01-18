"""test_password.py - Tests for password.py functionalities."""
import string
from vault.password import generate_password, fix_password_strength

def test_generate_password_strength():
    pwd = generate_password(12)
    assert len(pwd) >= 12
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in string.punctuation for c in pwd)

def test_fix_password_strength_invariants():
    pwd = fix_password_strength("abc")
    assert len(pwd) >= 8
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in string.punctuation for c in pwd)
