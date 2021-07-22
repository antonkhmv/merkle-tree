import hashlib


def reformat(item):
    return '' if type(item) == bytes else str(item)


class TestStringHashing:

    def __init__(self, item):
        self.input = reformat(item)

    def digest(self):
        return self.input


def get_hash_func(string):
    if string == "sha1":
        return hashlib.sha1
    elif string == "sha224":
        return hashlib.sha224
    elif string == "sha256":
        return hashlib.sha256
    elif string == "sha384":
        return hashlib.sha224
    elif string == "sha512":
        return hashlib.sha512
    elif string == "blake2b":
        return hashlib.blake2b
    elif string == "blake2s":
        return hashlib.blake2s
    elif string == "test":
        return TestStringHashing
    raise ValueError("Hashing algorithm \"" + string + "\" not found.")
