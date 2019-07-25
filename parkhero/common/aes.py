# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: aes.py
# @ide: PyCharm
# @time: 2019-07-24 22:46
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import base64

from crypto.Cipher import AES


BS = AES.block_size


def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s): return s[0:-ord(s[-1])]


class Aes:
    key = None
    encryptor = None

    def __int__(self):
        self.mode = AES.MODE_CBC

    def specifykey(self, key):
        self.key = key
        self.encryptor = AES.new(self.key)

    def encrypt(self, plaintext):
        return base64.b64encode(self.encryptor.encrypt(pad(plaintext)))

    def decrypt(self, ciphertext):
        un64_text = base64.b64decode(ciphertext)
        return unpad(self.encryptor.decrypt(un64_text).decode("utf-8"))
