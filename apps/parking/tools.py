# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: tools.py
# @ide: PyCharm
# @time: 2019-08-02 13:50
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import hashlib
from math import asin, cos, degrees, fabs, radians, sin, sqrt
import time
from django.contrib.auth import get_user_model

from apps.common.tools import pack_response

import logging
from apps.parking.models import ParkLot, VehicleInOut
from apps.users.models import Vehicle
from django.db import DatabaseError


logger = logging.getLogger(__name__)

EARTH_RADIUS = 6371


def get_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = fabs(lon2 - lon1)
    dlat = fabs(lat2 - lat1)
    havesine = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * EARTH_RADIUS * asin(sqrt(havesine))
    return distance


def get_region(lng, lat, dist):
    """
    :return two pairs lng/lat
    经纬度转换成弧度
    :param lng:
    :param lat:
    :param dist:
    :return:
    """
    rlat = radians(lat)
    dlng = 2 * asin(sin(dist / (2 * EARTH_RADIUS)) / cos(rlat))
    dlat = dist / EARTH_RADIUS

    # 弧度转成角度
    adlng = degrees(dlng)
    adlat = degrees(dlat)

    return lat - adlat, lat + adlat, lng - adlng, lng + adlng


def cacl_notice_id(in_time, carno, identifier):
    input = in_time + carno + identifier
    m = hashlib.md5()
    m.update(input.encode("utf-8"))
    output = m.hexdigest()

    return output


def auth_parkinglot_identifier(identifier):
    try:
        if identifier:
            parking_lots = ParkLot.objects.filter(identifier=int(identifier))
            if len(parking_lots) == 1:
                return parking_lots.first()
            errmsg = "Invalid identifier, It return {0} Parkinglot".format(
                len(parking_lots)
            )
        else:
            errmsg = "Invalid identifier, It'sin() null"
    except Exception as e:
        errmsg = "Exception: {0}".format(str(e))

    logging.error(errmsg)


def get_parkinglot_with_id(parkinglot_id):
    resp = None
    try:
        resp = ParkLot.objects.get(pk=parkinglot_id)
    except (ParkLot.DoesNotExist, ParkLot.MultipleObjectsReturned) as e:
        resp = pack_response(status="errparam", detail="{0}".format(e))
    except Exception as e:
        resp = pack_response(status="database_err", detail="{0}".format(e))
    finally:
        return resp
