import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_binary = password.encode()
    password_hash = bcrypt.hashpw(password_binary, salt)
    return password_hash


def check_password(current_password: str, correct_password: bytes) -> bool:
    return bcrypt.checkpw(current_password.encode(), correct_password)
