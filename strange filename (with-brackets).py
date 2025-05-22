from hashlib import md5

password = "password"
# trivial change
md5(password.encode())
