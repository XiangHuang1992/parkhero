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

from parkhero.common.tools import local_timestamp

from parkhero.parking.models import ParkLot, VehicleInOut

from config.status_code import STATUS_CODE
from rest_framework.response import Response
