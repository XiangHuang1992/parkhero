import os
import logging

from collections import OrderedDict

from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.tools import local_time_str
from apps.common.usercheck import UserCheck
from config.settings.base import MEDIA_ROOT
from config.status_code import STATUS_CODE

from .models import ParkLot
from .dal.parklot import DalParkLots


logger = logging.getLogger(__name__)


class ParklotImageMan(APIView):
    def get(self, request, format=None):
        identifier = request.GET.get("identifier")
        detail = dict()

        if not identifier:
            detail["detail"] = "Please provide a vaild parklot id"
            detail["status"] = STATUS_CODE["lostparam"]

            return Response(detail)
        try:
            parklots = DalParkLots.simple(identifier)

            if not parklots.exists():
                detail["detail"] = "no such parklot."
                detail["status"] = STATUS_CODE["non_such_parklot"]
                return Response(detail)

            detail["detail"] = parklots[0].image
            detail["status"] = STATUS_CODE["success"]

            return Response(detail)

        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            return Response(detail)

    def post(self, request, format=None):
        retval, retdetail = UserCheck.auth_check(
            request, "operator_parkinglot"
        )

        detail = dict()

        if retval != 0:
            logger.error(retdetail)
            return Response(retdetail)

        try:
            identifier = request.data["identifier"]
            up_file = request.FILES["filename"]
        except KeyError as e:
            detail["detail"] = "Please provide a valid %s" % e
            detail["status"] = STATUS_CODE["errparam"]
            logger.error(detail)
            return Response(detail)

        try:
            parlots = DalParkLots.simple(identifier=identifier, is_active=True)

            if not parlots.exists():
                detail["detail"] = (
                    "No parking lot with identifier %s" % identifier
                )
                detail["status"] = STATUS_CODE["non_such_parklot"]
                logger.error(detail)
                return Response(detail)
        except DatabaseError as e:
            detail["detail"] = "Can not get parklot with id %s, ex: %s." % (
                identifier,
                e,
            )
            detail["status"] = STATUS_CODE["database_err"]

            logger.error(detail)

            return Response(detail)

        _local_time_str = local_time_str(time_fmt="%g%m%d%H%M%S")

        try:
            m, ext = os.path.splitext(up_file.name)
            file_name = str(identifier) + "_" + _local_time_str + ext
            file_path = os.path.join(MEDIA_ROOT, file_name)
            logger.info(file_path)

            destination = open(file_path, "wb+")

            for chunk in up_file.chunks():
                destination.write(chunk)

            destination.close()
        except Exception as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["unknown_err"]
            logger.error(detail)
            return Response(detail)

        try:
            parklot = parlots[0]
            parklot.image = file_name
            parklot.save()
        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            logger.error(detail)
            return Response(detail)

        detail["detail"] = "parking lot image[%s] added" % file_path
        detail["status"] = STATUS_CODE["success"]
        logger.info(detail)
        return Response(detail)
