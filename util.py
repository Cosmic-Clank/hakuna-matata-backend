import bcrypt


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed: str):
    print(password, hashed)
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
