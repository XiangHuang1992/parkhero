# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: actout.py
# @ide: PyCharm
# @time: 2019-08-02 16:44
# @desc: ===============================================
# todo: handle vehicle out event
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from datetime import datetime

import logging

from django.db import DatabaseError, transaction

from apps.parking.dal.parklot import DalParkLots
from apps.parking.dal.vehicleinout import DalVehicleInOut
from apps.parking.dal.parklotextra import DalParkLotExtra
from apps.parking.models import ParkingLotExtra

from config.status_code import STATUS_CODE

from .evenbase import ACTHANDLERS
from .evenbase import EventBase

logger = logging.getLogger(__name__)


class ActoutHandler(EventBase):
    """handle vehicle out event class"""

    def acthandle(self, eventdata):
        plate_number = eventdata.get("carno")
        vehicle_inid = str(eventdata.get("inid"))

        space_total = eventdata.get("space_total")
        space_avaliable = eventdata.get("space_avaliable")
        identifier = eventdata.get("identifier")

        detail = dict()

        parklot_infos = DalParkLots.simple(identifier=identifier)

        if not parklot_infos.exists():
            detail["status"] = STATUS_CODE["non_such_parklot"]
            return detail

        vehicleinout_infos = DalVehicleInOut.simple(
            parklotids=parklot_infos, parklot_inid=vehicle_inid
        )

        # 必须先上传入场记录
        if not vehicleinout_infos.exists():
            detail["status"] = STATUS_CODE["non_vehiclein_record"]
            return detail

        _record = vehicleinout_infos[0]

        # 已经上传过的数据不允许修改，不完整的不允许上传
        if _record.out_time or not vehicle_inid:
            detail["status"] = STATUS_CODE["success"]
            return detail

        # 出场时允许修改车牌号
        if plate_number and _record.plate_number != plate_number:
            _record.plate_number = plate_number

        _record.out_uploadedtime = datetime.now()
        _record.out_time = eventdata.get("outtime")
        _record.updated_time = datetime.now()

        parklotextra_infos = DalParkLotExtra.simple(parklotids=parklot_infos[0].id)
        parklotextra = None

        try:
            if not parklot_infos.exists():
                parklotextra = ParkingLotExtra()
                parklotextra.parklot = parklot_infos[0]
            else:
                parklotextra = parklotextra_infos[0]

            with transaction.atomic():
                _record.save()

                if int(space_total) > parklot_infos[0].parking_space_total:
                    parklot_infos[0].parking_space_total = int(space_total)
                    parklot_infos[0].save()

                parklotextra.parkspace_available = int(space_avaliable) or 0
                parklotextra.save()

        except DatabaseError as e:
            logger.error(e)
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            return detail

        detail["status"] = STATUS_CODE["success"]
        return detail


ACTHANDLERS["out"] = ActoutHandler
