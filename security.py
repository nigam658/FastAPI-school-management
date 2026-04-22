from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hass_password (password : str):
    return pwd_context.hash(password)


def verify_password(plain_password :str, hass_password : str):
    return pwd_context.verify(plain_password,hass_password)
