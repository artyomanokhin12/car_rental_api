import bcrypt


def hash_password(
	password: str
):
	salt = bcrypt.gensalt()
	pass_bytes = password.encode()
	return bcrypt.hashpw(pass_bytes, salt)
