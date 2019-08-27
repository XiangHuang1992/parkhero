# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: o2oapiview.py
# @ide: PyCharm
# @time: 2019-08-02 16:47
# @desc: ===============================================
# todo:o2o module apiview base class which handle all o2o common business
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime
import logging

from django.db import DatabaseError
from config.status_code import STATUS_CODE

from rest_framework.response import Response
from rest_framework.views import APIView

from o2ohandlers.evenbase import verify_act, verify_enventdata
from o2ohandlers.eventimpl import ACTHANDLERS

from apps.parking.dal.parklot import DalParkLots
from apps.parking.dal.parklotextra import DalParkLotExtra
from apps.parking.models import ParkingLotExtra
from apps.parking.billing.tools import get_client_ip


logger = logging.getLogger(__file__)


class O2OAPIView(APIView):
    """all o2o common business in here"""

    def postbroker(self, request, actions):
        """handle new o2o data form upload tool"""
        detail = dict()
        try:
            rawcontent = request.data["content"]
            sign = request.data["sign"]
        except KeyError as keyerr:
            detail["detail"] = "%s" % keyerr
            detail["status"] = STATUS_CODE["errparam"]
            return Response(detail)

        retval, eventdata = verify_enventdata(rawcontent, sign)

        if not retval:
            detail["detail"] = "parklot not exists or sign error"
            detail["status"] = STATUS_CODE["errparam"]
            logger.error(detail)
            return Response(detail)

        identifier = eventdata["identifier"]

        try:
            parklot_infos = DalParkLots.simple(identifier=identifier)
        except DatabaseError as e:
            logger.error(e)

        if not parklot_infos.exists():
            # 不会发生这样的情况
            pass

        parklot = parklot_infos[0]

        # 更新http心跳
        parklotextra_infos = DalParkLotExtra.simple(parklotids=parklot.id)

        try:
            if not parklotextra_infos.exists():
                parklotextra = ParkingLotExtra()
                parklotextra.parklot = parklot
                parklotextra.heartbeat_time = datetime.now()
                parklotextra.httpip = get_client_ip(request)
                parklotextra.save()

        except DatabaseError as e:
            logger.error(e)

        if not verify_act(eventdata, actions):
            detail["detail"] = "such action not supported!"
            detail["status"] = STATUS_CODE["errparam"]
            logger.error(detail)
            return Response(detail)

        try:
            retdetail = ACTHANDLERS.get(eventdata.get("action"))().acthandle(eventdata)
        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            return Response(detail)

        return Response(retdetail)
