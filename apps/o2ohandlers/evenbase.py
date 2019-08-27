# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: evenbase.py
# @ide: PyCharm
# @time: 2019-07-25 17:29
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import json
import logging
from abc import ABCMeta, abstractmethod
from json.decoder import JSONDecodeError

from django.db import DatabaseError

from apps.common.tools import sign_authenticate
from apps.parking.dal.parklot import DalParkLots

ACTHANDLERS = {}

logger = logging.getLogger(__name__)


def verify_enventdata(eventdata, sign):
    try:
        alt_eventdata = json.loads(eventdata)
    except JSONDecodeError:
        return False, None

    identifier = alt_eventdata["identifier"]

    try:
        parklot_infos = DalParkLots.simple(identifier=identifier)
    except DatabaseError as e:
        logging.error(e)
        return False, None

    if not parklot_infos.exists():
        return False, None

    parklot = parklot_infos[0]
    if not sign_authenticate(eventdata, sign, parklot.public_key):
        return False, None

    return True, alt_eventdata


def verify_act(eventdata, actions):
    action = eventdata["action"]

    if isinstance(action, list) and action in actions:
        return True

    if actions == action:
        return True

    return False


class EventBase(metaclass=ABCMeta):
    @abstractmethod
    def acthandle(self, eventdata):
        pass
