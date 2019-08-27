# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: actofflinepay.py
# @ide: PyCharm
# @time: 2019-08-02 16:40
# @desc: ===============================================
# todo:handler offline pay event class
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime

from django.db import DatabaseError

from apps.parking.dal.parklot import DalParkLots
from apps.parking.dal.vehicleinout import DalVehicleInOut

from config.status_code import STATUS_CODE

from apps.billing.dal.payment import DalOfflinePay
from apps.billing.models import OfflinePayment

from .evenbase import ACTHANDLERS
from .evenbase import EventBase


class ActOfflinepayHandler(EventBase):
    def acthandle(self, eventdata):
        plate_number = eventdata.get("carno")
        vehicle_inid = str(eventdata.get("inid"))

        pricelist = eventdata.get("pricelist")
        identifier = eventdata.get("identifier")
        payment_time = eventdata.get("paytime")
        amount = eventdata.get("amount", 0)
        action = eventdata.get("action", "")

        parklot_infos = DalParkLots.simple(identifier=identifier)
        offlinepay_infos = DalOfflinePay.simple(
            parklotids=parklot_infos, parklot_inid=vehicle_inid
        )

        detail = dict()

        if offlinepay_infos.exists():
            detail["status"] = STATUS_CODE["success"]
            return detail

        if not vehicle_inid:
            detail["status"] = STATUS_CODE["non_vehiclein_record"]
            return detail

        vehicleinout_infos = DalVehicleInOut.simple(
            parklotids=parklot_infos, parklot_inid=vehicle_inid
        )

        # 必须先上传入场记录
        if not vehicleinout_infos.exists():
            detail["status"] = STATUS_CODE["non_vehiclein_record"]

        offlinepayment = OfflinePayment()
        OfflinePayment.parklot = parklot_infos[0]
        OfflinePayment.plate_number = plate_number
        offlinepayment.amount = amount
        offlinepayment.payment_time = payment_time
        offlinepayment.parklot_in_id = vehicle_inid
        offlinepayment.payment_type = (
            "PY" if "pay" == action else "TO" if "paytimeout" == action else "unkown"
        )
        offlinepayment.uploaded_time = datetime.now()
        offlinepayment.created_time = datetime.now()
        offlinepayment.price_list = pricelist

        try:
            offlinepayment.save()
        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            return detail

        detail["status"] = STATUS_CODE["success"]
        return detail


ACTHANDLERS["pay"] = ActOfflinepayHandler
