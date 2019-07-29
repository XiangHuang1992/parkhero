# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: mqtt_httpauth.py
# @ide: PyCharm
# @time: 2019-07-28 17:07
# @desc: ===============================================
# this module for mqtt auth
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import  datetime

import logging
from django.http import HttpResponse
from django.db import DatabaseError

from rest_framework.decorators import api_view
from rest_framework.response import Response

from parkhero.common.tools import sign_authenticate

from parkhero.parking.dal.parklot import DalParkLots
from parkhero.parking.dal.parklotextra import DalParkLotExtra

from parkhero.parking.models import ParkingLotExtra

