# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: tools.py
# @ide: PyCharm
# @time: 2019-07-24 22:46
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import base64
from datetime import datetime, timedelta
from builtins import str
import hashlib
import logging
import os
import time
import uuid
from collections import OrderedDict
import rsa

from rsa.pkcs1 import VerificationError

from rest_framework.response import Response

from config.status_code import STATUS_CODE


logger = logging.getLogger(__name__)

KEYDIR_PREFIX = 'keyperms/parklots/'
PRIVATE_KEY_SUFFIX = '_pri_key.pem'
PRIVATE_KEY_PKCS_SUFFIX = '_pri_key_pkcs8.pem'
PUBLIC_KEY_SUFFIX = '_pub_key.pem'

def get_projdir():
    return os.path.dirname(os.path.dirname(__file__))

def md5Encode(password):
    md5orig = hashlib.md5(password.encode(encoding="utf-8"))
    return md5orig.hexdigest()

def keydir_full_prefix(prefix):
    _prefix = os.path.join(get_projdir(), prefix)

    try:
        if not os.path.exists(_prefix):
            os.makedirs(_prefix)
        return _prefix
    except Exception as e:
        logger.error('{0}'.format(e))
        return get_projdir()

def get_keydor(keyname):
    _full_prefix = keydir_full_prefix(KEYDIR_PREFIX)
    pri_keyname = _full_prefix + keyname + PRIVATE_KEY_SUFFIX
    pri_keyname_pkcs8 = _full_prefix + keyname + PRIVATE_KEY_PKCS_SUFFIX
    pub_keyname = _full_prefix + keyname + PUBLIC_KEY_SUFFIX
    return (pri_keyname, pri_keyname_pkcs8, pub_keyname)

def get_before_str(qdays):
    before = datetime.now() + timedelta(days=-qdays)
    pass
