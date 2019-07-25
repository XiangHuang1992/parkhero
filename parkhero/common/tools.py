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
from urllib.parse import quote_plus

import rsa

from rsa.pkcs1 import VerificationError

from rest_framework.response import Response

from config.status_code import STATUS_CODE


logger = logging.getLogger(__name__)

KEYDIR_PREFIX = "keyperms/parklots/"
PRIVATE_KEY_SUFFIX = "_pri_key.pem"
PRIVATE_KEY_PKCS_SUFFIX = "_pri_key_pkcs8.pem"
PUBLIC_KEY_SUFFIX = "_pub_key.pem"


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
        logger.error("{0}".format(e))
        return get_projdir()


def get_keydir(keyname):
    _full_prefix = keydir_full_prefix(KEYDIR_PREFIX)
    pri_keyname = _full_prefix + keyname + PRIVATE_KEY_SUFFIX
    pri_keyname_pkcs8 = _full_prefix + keyname + PRIVATE_KEY_PKCS_SUFFIX
    pub_keyname = _full_prefix + keyname + PUBLIC_KEY_SUFFIX
    return (pri_keyname, pri_keyname_pkcs8, pub_keyname)


def get_before_str(qdays):
    before = datetime.now() + timedelta(days=-qdays)
    return before.strftime("%Y-%m-%d %H:%M:%S")


def local_time_str(sp_time=None, time_fmt="%Y-%m-%d %H:%M:%S"):
    str_time = None
    try:
        if sp_time is None:
            sp_time = datetime.now()
        if not isinstance(sp_time, str):
            str_time = datetime.strftime(sp_time, time_fmt)
        else:
            str_time = sp_time
    except ValueError as e:
        ext_time_fmt = "%Y-%m-%d %H:%M:%S.%f"
        try:
            str_time = datetime.strftime(sp_time, ext_time_fmt)
        except Exception as e:
            logger.error("{0}, time_fmt:{1}".format(e, ext_time_fmt))
    except Exception as e:
        logger.error("{0}".format(e))
    return str_time


def local_time_fmt(sp_time=None, time_fmt="%Y-%m-%d %H:%M:%S"):
    ptime = None
    try:
        if sp_time is None:
            sp_time = datetime.now()
        if not isinstance(sp_time, str):
            sp_time = local_time_str(sp_time)
        ptime = datetime.strptime(sp_time, time_fmt)
    except ValueError as e:
        ext_time_fmt = "%Y-%m-%d %H:%M:%S.%f"
        try:
            temp = datetime.strptime(sp_time, ext_time_fmt)
            sp_time = local_time_str(temp)
            ptime = datetime.strptime(sp_time, time_fmt)
        except Exception as e:
            logger.error("{0}, time_fmt:{1}".format(e, ext_time_fmt))
    except Exception as e:
        logger.error("{0}".format(e))
    return ptime


def local_timestamp(sp_time=None, time_fmt="%Y-%m-%d %H:%M:%S"):
    try:
        local_fmt = local_time_fmt(sp_time, time_fmt)
        return time.mktime(local_fmt.timetuple())
    except ValueError as e:
        raise e


def pack_response(**kwargs):
    # fill in response headers
    logger.debug("{0}".format(kwargs))
    if "status" in kwargs:
        status_code = STATUS_CODE[kwargs.pop("status")]
    else:
        status_code = STATUS_CODE["success"]
    kwargs["status"] = status_code

    if "detail" not in kwargs:
        kwargs["detail"] = ""
        if status_code == 0:
            kwargs["detail"] = "It's success"

    response = Response(kwargs)
    return response


def gen_uuid():
    return str(uuid.uuid1())


def sign_authenticate(data, sign, pubkey):
    """ verify data signature for upload tool"""
    alt_pubkey = rsa.PublicKey.load_pkcs1(pubkey.encode("utf-8"))
    alt_sign = base64.b64decode(sign.encode("utf-8"))

    try:
        result = rsa.verify(data.encode("gbk"), alt_sign, alt_pubkey)
    except VerificationError:
        result = False

    return result


def calc_md5_hexdigest(cf):
    return hashlib.md5(cf.encode("utf-8")).hexdigest()


def strftime(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    return timestamp.strftime(fmt)


def float2int(_float):
    """
    浮点数取整
    :param _float:
    :return:
    """
    str_float = "{0}".format(_float)
    _list = str_float.split(".")
    _int = int(_list[0])
    _point = 0

    if len(_list) > 1:
        _point = float(_list[1])
    if _point > float(0.5):
        _int += 1
    return _int


def calc_md5(msg, entrance):
    """ md5 implement for broker module """
    msg = OrderedDict(sorted(msg.items()))
    targets = ""
    for (k, v) in msg.items():
        targets += k
        targets += "="
        targets += str(v)

        sch = str(v)
        s_url = ""

        # url encode
        for i in range(0, len(sch)):
            # if sch[i] >= u"\u4e00" and sch[i] <= u"\u9fa5":
            if u"\u4e00" <= sch[i] <= u"\u9fa5":
                s_url += quote_plus(sch[i]).lower()

        targets += "&"
    targets = targets[:-1]
    targets += str(entrance)

    md5obj = hashlib.md5()
    md5obj.update(targets.encode("gbk"))

    ret = md5obj.hexdigest()
    return ret
