from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

fernet = Fernet(key)

with open('usuario', 'rb') as arquivo:
    original = arquivo.read()

encrypted = fernet.encrypt(original)

with open('usuario', 'wb') as encryptedFile:
    encryptedFile.write(encrypted)
