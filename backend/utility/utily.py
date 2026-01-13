import bcrypt
from cryptography.fernet import Fernet

_KEY = Fernet.generate_key()
cipher_suite = Fernet(_KEY)

def hashdata(data:str)->str :
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data.decode('utf-8')


def verify_hash(data:str, hashed_data:str)->bool:
    return bcrypt.checkpw(data.encode('utf-8'), hashed_data.encode('utf-8'))

def cryptoPswd(pswd:str)->str:

    password_enc = cipher_suite.encrypt(pswd.encode('utf-8')).decode('utf-8')
    return password_enc

def verify_crupto (pwsdCrypto :str) ->str:
    pwsdCrypto.encode('utf-8')
    decodepswd = cipher_suite.decrypt(pwsdCrypto.encode('utf-8')).decode('utf-8')
    return decodepswd

