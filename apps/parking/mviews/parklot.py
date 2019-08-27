# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: parklot.py
# @ide: PyCharm
# @time: 2019-08-02 11:56
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import logging
from datetime import datetime

from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView

from config.status_code import STATUS_CODE
from apps.common.paginator import PaginatorParaVerify
from apps.parking.dal.parklot import DalParkGate, DalParkLots
from apps.parking.dal.parklotextra import DalParkLotExtra
from apps.parking.serializers import (
    ParkingGateSerializer,
    ParkingLotExtraSerializer,
    ParkingLotSerializer,
)
from ..tools import get_region

logger = logging.getLogger(__name__)


class ParkingLotView(APIView):
    def get(self, request):
        city_code = request.GET.get("city_code")
        lot_type = request.GET.get("lot_type")
        parklotid = request.GET.get("parklotid")
        name = request.GET.get("name")

        longtitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")
        distance = request.GET.get("distance")

        try:
            lng = float(longtitude or 0)
            lat = float(latitude or 0)
            dist = 3 if int(distance or 0) > 3 else int(distance or 0)
        except Exception as e:
            logger.error(e)

        startindex = request.GET.get("start_index")
        maxresults = request.GET.get("max_results")
        pagedirect = request.GET.get("pagedirect")
        maxres, start, pagedirect = PaginatorParaVerify.composite(
            maxresults, startindex, pagedirect
        )
        detail = dict()
        try:
            parklotids = None
            detail["kind"] = "parking_lots#nearby"

            if lng and lat and dist:
                latmin, latmax, lngmin, lngmax = get_region(lng, lat, dist)
                parkgates = DalParkGate.simple(
                    gatetype=1,
                    lngmin=lngmin,
                    lngmax=lngmax,
                    latmin=latmin,
                    latmax=latmax,
                )

                parklotids = [gateitem.parklot.id for gateitem in parkgates]

            if not (parklotids is None) and parklotids == []:
                detail["parking_lots"] = []
                detail["update_time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                detail["status"] = STATUS_CODE["success"]
                logger.info(detail)
                return Response(detail)
        except DatabaseError as e:
            detail["parking_lots"] = []
            detail["update_time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            detail["status"] = STATUS_CODE["database_err"]
            logger.info(detail)
            return Response(detail)

        parklot_toquery = parklotid if parklotid else parklotids

        try:
            parklot_infos, maxid, minid = DalParkLots.complex(
                parklotid=parklot_toquery,
                city_code=city_code,
                is_active=True,
                name=name,
                maxres=maxres,
                startindex=start,
                pagedirect=pagedirect,
                lot_type=lot_type,
            )

            if (parklot_infos is None) or (
                parklot_infos and not parklot_infos.exists()
            ):
                detail["parking_lots"] = []
                detail["update_time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                detail["status"] = STATUS_CODE["success"]
                logger.info(detail)
                return Response(detail)

        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            logger.info(detail)
            return Response(detail)

        if maxid:
            detail["maxid"] = maxid

        if minid:
            detail["minid"] = minid

        resparklotids = []

        for lotitem in parklot_infos:
            resparklotids.append(lotitem.id)
            lotitem.type = lotitem.get_type_display()

        data_mod = ParkingLotSerializer(parklot_infos, many=True).data

        try:
            lotid2gates = {}
            resparkgates = DalParkGate.simple(
                parklotid=resparklotids, gatetype=1
            )

            for gateitem in resparkgates:
                if not lotid2gates.get(gateitem.parklot.id):
                    lotid2gates[gateitem.parklot.id] = []

                lotid2gates[gateitem.parklot.id].append(gateitem)
        except DatabaseError as e:
            logger.error(e)

        try:
            lotid2extras = {}
            resparkextra_infos = DalParkLotExtra.simple(
                parklotids=resparklotids
            )
            resparkextras_data = ParkingLotExtraSerializer(
                resparkextra_infos, many=True
            ).data

            for item in resparkextras_data:
                lotid2extras[item["parklot"]] = item

        except DatabaseError as e:
            logger.error(e)

        for i in data_mod:
            if lotid2gates and lotid2gates.get(i["id"]):
                i["parkgate"] = ParkingGateSerializer(
                    lotid2gates[i["id"]], many=True
                ).data
            else:
                i["parkgate"] = []

            if (
                lotid2extras
                and lotid2extras.get(i["id"])
                and lotid2extras.get(i["id"]).get("parkspace_available")
            ):
                i["parking_space_available"] = lotid2extras.get(i["id"]).get(
                    "parkspace_available"
                )
            else:
                i["parking_space_available"] = 0

            if i["parking_space_available"] > i["parking_space_total"]:
                i["parking_space_available"] = i["parking_space_total"]

        # 处理上一页
        if pagedirect == 0 and start != 0:
            data_mod.reverse()

        detail["parking_lots"] = data_mod
        detail["update_time"] = datetime.now()
        detail["status"] = STATUS_CODE["success"]
        return Response(detail)
