# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: alipayconfig.py
# @ide: PyCharm
# @time: 2019-07-29 12:01
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""


class AliPayConfig:
    def __int__(self, channel_config):
        self.partner = channel_config["partner"]
        self.seller_id = channel_config["seller_id"]
        self.partner_private_key_file = channel_config[
            "partner_private_key_file"
        ]
        self.partner_public_key_file = channel_config[
            "partner_public_key_file"
        ]
        self.alipay_public_key_file = channel_config["alipay_public_key_file"]
        self.notify_url = channel_config["notify_url"]
        self.sign_type = channel_config["sign_type"]

    def __str__(self):
        return "AliPayConfig object: " + str(self.__dict__)
