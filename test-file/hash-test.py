from werkzeug.security import generate_password_hash, check_password_hash

# Simulate storing a password hash
user = {
    'username': 'john_doe',
    'password_hash': "scrypt:32768:8:1$jUwDsRMp2ptAeBvz$32ce33138e90f24d46c8ef55c436c0b56936da0cc1285457abb4bb94abc2181c375d141a6810552840f8f72558f75a8e00820b3b7874fb7a263724e282b74916"
}
print(user['password_hash'])
# User tries to log in
password = "admin123"  # User input password
# hashed_password = generate_password_hash(password)
# print("Generated Hash:", hashed_password)
# Verify password
if check_password_hash(user['password_hash'], password):
    print("Login successful!")
else:
    print("Invalid password.")
