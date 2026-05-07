import re

def is_valid_email(email):
    if isinstance(email, str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    return False