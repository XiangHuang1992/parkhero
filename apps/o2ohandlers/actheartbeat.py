# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: actheartbeat.py
# @ide: PyCharm
# @time: 2019-08-02 16:00
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime

from config.status_code import STATUS_CODE
from .evenbase import ACTHANDLERS, EventBase


class ActheartbeatHanler(EventBase):
    """handle parklot heartbeat class"""

    def acthandle(self, eventdata):
        detail = dict()
        detail["servertime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        detail["status"] = STATUS_CODE["success"]
        return detail


ACTHANDLERS["heartbeat"] = ActheartbeatHanler
