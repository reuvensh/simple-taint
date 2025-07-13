import hashlib.md5 as md5

secret_key = "secret_key"
password = secret_key
md5(password.encode())
