import re

def check_email(email: str):
    assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Please enter a valid email."


def check_username(username: str):
    assert (
        len(username) >= 6 and len(username) <= 20
    ), "username length should be greater than 6 and less than 20."
    assert re.match(
        r"^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", username
    ), "Please use only alphanumeric characters in username(a-z, A-Z, 0-9, . and _)."
    return username.lower()


def check_password(password: str):
    assert len(password) >= 8, "Password must be atleast 8 characters long."
