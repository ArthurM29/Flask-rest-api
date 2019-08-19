from Section5_SQLLite.src.user import User
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):  # safer way to compare strings in different encodings
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
