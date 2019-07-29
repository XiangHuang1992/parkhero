# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: alipay.py
# @ide: PyCharm
# @time: 2019-07-29 11:32
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import base64
from collections import OrderedDict
import rsa

from django.utils.http import urlquote_plus


class AliPay(object):
    def __int__(self, alipay_config):
        self.partner = alipay_config.partner
        self.seller_id = alipay_config.seller_id
        self.partner_private_key_file = alipay_config.partner_private_key_file
        self.partner_public_key_file = alipay_config.partner_public_key_file
        self.alipay_public_key_file = alipay_config.alipay_public_key_file
        self.notify_url = alipay_config.notify_url
        self.sign_type = alipay_config.sign_type

        self.common_params = {
            "partner": self.partner,
            "seller_id": self.seller_id,
        }

        self.params = {}

    def set_params(self, **kwargs):
        for (k, v) in kwargs["params"].items():
            self.params[k] = v

        self.params.update(self.common_params)

    def get_order_string(self):
        msg = OrderedDict(sorted(self.params.items()))

        s = ""

        for (k, v) in msg.items():
            s += k
            s += "="
            s += '"'
            s += str(v)
            s += '"'
            s += "&"

        sign_pre = s[:-1]

        sign = self.get_sign(sign_pre)

        signed = (
            sign_pre
            + '&sign="'
            + sign
            + '"&sign_type="'
            + self.sign_type
            + '"'
        )

        return signed

    def get_sign(self, content):
        with open(self.partner_private_key_file, mode="rb") as privatefile:
            keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)

        print("Input string to RSA signature[%s]" % content)

        sign_bytes = rsa.sign(content.encode("utf-8"), privkey, "SHA-1")
        sign = base64.b64encode(sign_bytes)
        sign_urlencode = urlquote_plus(sign.decode("utf-8"))

        return sign_urlencode
