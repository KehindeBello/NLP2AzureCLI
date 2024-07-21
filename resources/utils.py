import bcrypt

def hashPassword(password):
    #encode password
    encoded_password = password.encode("utf-8")
    #salt 
    salt = bcrypt.gensalt()
    #hashing the password
    print(f'type - {type(encoded_password)}')
    print(encoded_password)
    hash = bcrypt.hashpw(encoded_password, salt=salt)
    decoded_hash = hash.decode("utf-8")
    return decoded_hash

def checkPassword(password, hashed_password):
    encoded_password = password.encode("utf-8")
    #ensure hashed password is in bytes
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=encoded_password, hashed_password=hashed_password)