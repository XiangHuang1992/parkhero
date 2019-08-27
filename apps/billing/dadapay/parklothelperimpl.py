# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: parklothelperimpl.py
# @ide: PyCharm
# @time: 2019-07-29 17:04
# @desc: ===============================================
# dadapay 帮助接口
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime
import logging
import json
from collections import OrderedDict
from paho.mqtt import publish as mqttpub
from apps.billing.models import DaDaPayLog
from apps.common.tools import strftime, local_timestamp, float2int, calc_md5
from config.settings.local import MQTTAUTH, MQTTHOST
from config.status_code import STATUS_CODE

from apps.parking.models import VehicleInOut
from apps.parking.dal.vehicleinout import DalVehicleInOut
from .dadapayhelperbase import DadapayHelperBase, DADAPAYHELPERS

logger = logging.getLogger(__name__)


class ParklotHelperImpl(DadapayHelperBase):
    """停车场缴费相关的帮助接口"""

    def _evalfee(self, pricelist, timespan):
        if pricelist and isinstance(pricelist, str):
            pricelist = json.loads(pricelist)

        if timespan <= 0:
            return 0

        _pricelist = sorted(pricelist, key=lambda price: price["time"])

        def _get_price(_span):
            for _price in _pricelist:
                if _span <= _price["time"]:
                    return _price["price"]

        price = _get_price(timespan)

        if price is not None:
            return price

        max_per_time = _pricelist[-1]["time"]
        max_per_price = _pricelist[-1]["price"]

        delta_span = timespan % max_per_time
        delta_price = _get_price(delta_span)

        over_span = (timespan - delta_span) / max_per_time
        amount = over_span * max_per_price + delta_price

        return amount

    def verifyparamshelper(self, request):
        try:
            plate_number = request.GET["plate_number"]

        except KeyError as e:
            detail = dict()
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["lostparam"]
            logger.error(detail)

            return STATUS_CODE["lostparam"], detail

        self.plate_number = plate_number

        return STATUS_CODE["success"], None

    def orderservicehelper(self, request):
        """返回价格、金额、相应的服务对象"""
        inout_record = VehicleTools
        pass
