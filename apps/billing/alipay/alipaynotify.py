# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: alipaynotify.py
# @ide: PyCharm
# @time: 2019-07-29 15:30
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import base64
from collections import OrderedDict
import logging
import rsa

from .alipay import AliPay


logger = logging.getLogger(__name__)


class AliPayNotify(AliPay):

    def __int__(self, alipay_config):
        super(AliPayNotify, self).__int__(alipay_config)

    def sign_verify(self, content):
        msg_dict = OrderedDict(sorted(content.items()))
        s = ''
        for (k, v) in msg_dict.items():
            if k != 'sign' and k != 'sign_type':
                s += k
                s += '='
                s += str(v)
                s += '&'

        msg_str = s[:-1]

        with open(self.alipay_public_key_file, mode='rb') as publicfile:
            keydata = publicfile.read()

        pubkey = rsa.PublicKey.load_pkcs1(keydata)
        sign_list = content.get('sign', '')
        sign_str = sign_list

        if sign_str == '':
            return False

        sign_bytes = sign_str.encode('utf-8')

        sign = base64.b64decode(sign_bytes)

        logger.info('Input string to RSA signature[%s]' % msg_str)

        try:
            result = rsa.verify(msg_str.encode('utf-8'), sign, pubkey)
            logger.log('Alipay notification verified')
        except rsa.pkcs1.VerificationError:
            logger.error('Alipay notification verify FAILED')
            result = False

        return result
