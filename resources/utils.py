import bcrypt

def hashPassword(password):
    #encode password
    encoded_password = password.encode("utf-8")
    #salt 
    salt = bcrypt.gensalt()
    #hashing the password
    hash = bcrypt.hashpw(encoded_password, salt=salt)
    return hash

def checkPassword(password, hashed_password):
    encoded_password = password.encode("utf-8")
    #ensure hashed password is in bytes
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=encoded_password, hashed_password=hashed_password)