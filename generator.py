import random
import string


def generate_password(length, use_letters, use_digits, use_symbols):
    chars = ""

    if use_letters:
        chars += string.ascii_letters

    if use_digits:
        chars += string.digits

    if use_symbols:
        chars += string.punctuation

    return "".join(random.choice(chars) for _ in range(length))