# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: actin.py
# @ide: PyCharm
# @time: 2019-08-02 16:22
# @desc: ===============================================
# handle vehicle in event
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import json
import logging
from datetime import datetime

from django.db import DatabaseError, transaction

from config.status_code import STATUS_CODE
from apps.parking.dal.parklot import DalParkLots
from apps.parking.dal.parklotextra import DalParkLotExtra
from apps.parking.dal.vehicleinout import DalVehicleInOut
from apps.parking.models import ParkingLotExtra, VehicleInOut
from .evenbase import ACTHANDLERS, EventBase

logger = logging.getLogger(__name__)


class ActinHandler(EventBase):
    """ handle vehicle in class"""

    def acthandle(self, eventdata):
        plate_number = eventdata.get("carno")
        vehicle_inid = str(eventdata.get("inid"))

        space_total = eventdata.get("space_total")
        space_available = eventdata.get("space_available")
        pricelist = eventdata.get("pricelist")
        parklotid = eventdata.get("identifier")

        detail = dict()

        parklot_infos = DalParkLots.simple(identifier=parklotid)
        if not parklot_infos.exists():
            logger.info(detail)
            detail["status"] = STATUS_CODE["non_such_parklot"]
            return detail

        vehicleinout_infos = DalVehicleInOut.simple(
            parklotids=parklot_infos, parklot_inid=vehicle_inid
        )

        if vehicleinout_infos.exists():
            detail["status"] = STATUS_CODE["non_vehiclein_record"]
            return detail

        vehicleinout = VehicleInOut()
        vehicleinout.parklot = parklot_infos[0]
        vehicleinout.plate_number = plate_number
        vehicleinout.parklot_in_id = vehicle_inid
        vehicleinout.in_time = eventdata.get("intime")
        vehicleinout.in_prices = json.dumps(pricelist) if pricelist else None
        vehicleinout.in_upload_datetime = datetime.now()
        vehicleinout.created_time = datetime.now()

        parklotextra_infos = DalParkLotExtra.simple(
            parklotids=parklot_infos[0].id
        )
        parklotextra = None

        try:
            if not parklotextra_infos.exists():
                parklotextra = ParkingLotExtra()
                parklotextra.parklot = parklotextra_infos[0]
            else:
                parklotextra = parklotextra_infos[0]

            with transaction.atomic():
                vehicleinout.save()

                if int(space_total) > parklot_infos[0].parking_space_total:
                    parklot_infos[0].parking_space_total = int(space_total)
                    parklot_infos[0].save()

                parklotextra.parkspace_available = int(space_available) or 0
                parklotextra.save()

        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            logging.error(detail)
            return detail


ACTHANDLERS["in"] = ActinHandler
