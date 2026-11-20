from werkzeug.security import generate_password_hash, check_password_hash
import re

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using Werkzeug's default method (pbkdf2:sha256).
    This avoids the overhead of initializing Flask-Bcrypt globally.
    """
    return generate_password_hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifies a plaintext password against the stored hash.
    """
    return check_password_hash(hashed_password, plain_password)

def is_valid_email(email: str) -> bool:
    """
    Basic regex check for email format to prevent simple injection or typos.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None