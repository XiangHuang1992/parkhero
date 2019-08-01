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
from datetime import datetime

import logging
from django.http import HttpResponse
from django.db import DatabaseError

from rest_framework.decorators import api_view
from rest_framework.response import Response

from parkhero.common.tools import sign_authenticate

from parkhero.parking.dal.parklot import DalParkLots
from parkhero.parking.dal.parklotextra import DalParkLotExtra

from parkhero.parking.models import ParkingLotExtra
from billing.tools import get_client_ip


LOGGER = logging.getLogger(__name__)


@api_view(["GET", "POST"])
def user_auth(request):
    """
    user auth

    username: parklot + identifier
    password: encrypt(identifier)
    """
    parklot_data = request.data

    try:
        fake_indentifier = parklot_data.get("username")
        crypt_identifier = parklot_data.get("password")

        if not fake_indentifier:
            fake_indentifier = request.GET.get("username")

        if not crypt_identifier:
            crypt_identifier = request.GET.get("password")

    except KeyError as e:
        LOGGER.error(e)
        return HttpResponse("deny")

    if not fake_indentifier.startwith("parklot"):
        return HttpResponse("deny")

    identifier = fake_indentifier.replace("parklot", "")

    try:
        parklot_infos = DalParkLots.simple(identifier=identifier)
    except DatabaseError as e:
        LOGGER.error(e)
        return HttpResponse("deny")

    if not parklot_infos.exists():
        return HttpResponse("deny")

    parklot = parklot_infos[0]

    if not sign_authenticate(identifier, crypt_identifier, parklot.pubkey):
        return HttpResponse("deny")

    # 更新mqtt心跳信息
    parklotextra_infos = DalParkLotExtra.simple(parklotids=parklot.id)

    try:
        if not parklotextra_infos.exists():
            parklotextra = ParkingLotExtra()
            parklotextra.parklot = parklot
            parklotextra.login_time = datetime.now()
            parklotextra.mqttip = get_client_ip(request)
            parklotextra.save()

        else:
            parklotextra = parklotextra_infos[0]
            parklotextra.login_time = datetime.now()
            parklotextra.mqttip = get_client_ip(request)
            parklotextra.save()

    except DatabaseError as e:
        LOGGER.error(e)

    return HttpResponse("allow")


@api_view(["POST"])
def vhost_auth(request):
    return HttpResponse("allow")


@api_view(["POST"])
def resource_auth(request):
    return HttpResponse("allow")


@api_view(["POST"])
def topic_auth(request):
    mqttdata = request.data
    topic = mqttdata.get("routing_key")

    if not topic.startwith("handset"):
        return HttpResponse("deny")

    return HttpResponse("allow")
