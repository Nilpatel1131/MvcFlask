import bcrypt

encoded_password = '$2b$12$WW/PXqWJGMFF8Qg6MQQ6IuzXk3E2RO/OEbHWKvDJm7.B/LuI/0ksa'
encoded_password_bytes = encoded_password.encode("utf-8")
# hashed_login_password.decode("utf-8")
salt = bcrypt.gensalt(rounds=12)

hashed_login_password = bcrypt.hashpw(encoded_password_bytes, salt)
print("hashed_login_password=", hashed_login_password)
print("decode_hashed_login_password=", hashed_login_password.decode("utf-8"))
print(encoded_password_bytes.decode("utf-8"))
