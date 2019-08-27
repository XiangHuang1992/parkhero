# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: vehicle_tools.py
# @ide: PyCharm
# @time: 2019-07-29 17:08
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import logging
from django.db import DatabaseError


from apps.parking.models import ParkLot, VehicleInOut

from config.status_code import STATUS_CODE
from guardian.shortcuts import get_objects_for_user
from apps.users.models import Vehicle

logger = logging.getLogger(__name__)


class VehicleTools:
    @staticmethod
    def vehicle_latest_record(plate_number, parkinglot=None, lot_type=None):
        if not plate_number:
            return None
        try:
            records = VehicleInOut.objects.filter(plate_number=plate_number)
            if parkinglot is not None:
                records = records.filter(parklot=parkinglot)
            if lot_type is not None:
                records = records.filter(parklot__type=lot_type)
            return records.latest("id")
        except VehicleInOut.DoesNotExist as e:
            logger.error(
                "No inout record found for plate number[{0}] in parking lot[{1}]"
            ).format(plate_number, parkinglot)
            logger.error(e)
        except Exception as e:
            logger.error("{0}").format(e)

    @staticmethod
    def inter_parklot_ids(user, parklot_ids=None):
        parklots = get_objects_for_user(user, "parking.act_analyse_parkinglot")
        if parklot_ids:
            interparklot_ids = [
                item.id for item in parklots if str(item.id) in parklot_ids
            ]
        else:
            interparklot_ids = [item.id for item in parklots]

        logger.info("interparklot_ids: %s" % interparklot_ids)
        return interparklot_ids

    @staticmethod
    def check_plate_number(user, plate_number):

        detail = "Please provide a valied plate number"

        if not plate_number:
            logger.error(detail)
            return STATUS_CODE["invalid_plate_number"]

        try:
            vehicles = Vehicle.objects.filter(owner=user, plate_number=plate_number)
            if not vehicles.exists():
                logger.error(detail)
                return STATUS_CODE["non_vehicle_found"]
        except DatabaseError as e:
            logger.error(e)
            return STATUS_CODE["database_err"]

        return STATUS_CODE["success"]

    @staticmethod
    def vehicle_join_parklot(serializer_data, parklot_ids):
        try:
            parkinglots = ParkLot.objects.filter(id__in=parklot_ids)
            lots_id2name = {p.id: (p.name, p.get_type_display()) for p in parkinglots}

            for i in serializer_data:
                i["parklot"], i["lottype"] = lots_id2name[i["parklot"]]

        except Exception as e:
            logger.error("Can not find parking lot has e: %s", e)

        return serializer_data
