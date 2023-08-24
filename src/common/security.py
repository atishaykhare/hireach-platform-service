import bcrypt


def hash_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes) -> bool:

    return bcrypt.checkpw(
        password.encode('utf-8'), password_in_db.encode('utf-8'))
