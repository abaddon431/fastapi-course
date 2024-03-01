from passlib.context import CryptContext

password_ctx = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password):
    return password_ctx.hash(password)

def verify(plain_password, hashed_password):
    return password_ctx.verify(plain_password, hashed_password)