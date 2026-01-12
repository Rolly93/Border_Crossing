import bcrypt

def hashdata(data:str)->str :
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data.decode('utf-8')


def verify_hash(data:str, hashed_data:str)->bool:
    return bcrypt.checkpw(data.encode('utf-8'), hashed_data.encode('utf-8'))