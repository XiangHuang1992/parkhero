# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: tools.py
# @ide: PyCharm
# @time: 2019-07-29 11:04
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from collections import OrderedDict
from datetime import datetime
import hashlib
import logging
from random import Random
import time
from django.contrib.sessions.backends.db import SessionStore


logger = logging.getLogger(__name__)


def get_sign(params, key):
    msg = OrderedDict(sorted(params.items()))

    s = ""
    for (k, v) in msg.items():
        s += k
        s += "="
        s += str(v)
        s += "&"
    s += "key="
    s += str(key)

    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    ret = m.hexdigest().upper()

    return ret


def random_str(length):
    randstr = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    count = len(chars) - 1
    random = Random()

    for i in range(length):
        randstr += chars[random.randint(0, count)]

    return randstr


def get_client_ip(request):
    x_forwarded_for = request.Meta.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.Meta.get("REMOTE_ADDR")

    return ip


def get_trade_no(length):
    now = int(time.time())
    datearray = datetime.utcfromtimestamp(now)
    tradetimestamp = datearray.strptime("%Y%m%d%H%M%S")
    append = ""
    chars = ""
    count = len(chars) - 1
    random = Random()
    for i in range(length):
        append += chars[random.randint(0, count)]

    trade_no = tradetimestamp + append

    return trade_no


def get_userid_from_session(session_key):
    try:
        s = SessionStore(session_key=session_key)
        userid = s["_auth_user_id"]
    except KeyError:
        logger.error("No user Id found, invalid session key")
    except Exception as e:
        logger.error("{0}".format(e))
    else:
        return userid
