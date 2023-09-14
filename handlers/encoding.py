import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import string
import random


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class AESCipher:
    def __init__(self, key: str):
        if len(key) != 16:
            raise Exception("INVALID LEN OF KEY (not 16)")
        self.key = key

    def encrypt(self, data: str):
        data = pad(data.encode(), 16)
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC)
        return base64.b64encode(cipher.encrypt(data)), base64.b64encode(cipher.iv).decode('utf-8')

    def decrypt(self, enc: str, iv: str):
        enc = base64.b64decode(enc)
        iv = base64.b64decode(iv)
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(enc), 16)


# a = AESCipher("aaaaaaaaaaaaaaaa")
# encrypted, iv_ = a.encrypt("test")
# decrypted = a.decrypt(encrypted, iv_)
#
# print('encrypted: \n\t', encrypted.decode("utf-8"), "\n\t", iv_)
# print('data: ', decrypted.decode("utf-8"))
