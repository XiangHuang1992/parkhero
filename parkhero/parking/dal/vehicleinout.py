# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: vehicleinout.py
# @ide: PyCharm
# @time: 2019-07-26 17:53
# @desc: ===============================================
# vehicleinout's dal, return queryset
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from parkhero.common.paginator import Paginator
from parkhero.parking.models import VehicleInOut


class DalVehicleInOut:

    vehicleinout_infos = VehicleInOut.objects

    @classmethod
    def simple(
        cls,
        pkid=None,
        parklotids=None,
        platenum=None,
        intime=None,
        parklot_inid=None,
        orderby=None,
    ):

        vehicleinout_infos = cls.vehicleinout_infos

        if pkid:
            vehicleinout_infos = vehicleinout_infos.filter(pk__in=pkid)

        if parklotids:
            vehicleinout_infos = vehicleinout_infos.filter(
                parklot__id__in=parklotids
            )
        if platenum:
            vehicleinout_infos = vehicleinout_infos.filter(
                plate_number__startswith=platenum
            )
        if intime:
            vehicleinout_infos = vehicleinout_infos.filter(in_time__gt=intime)
        if parklot_inid and not isinstance(parklot_inid, list):
            vehicleinout_infos = vehicleinout_infos.filter(
                parklot_inid=parklot_inid
            )
        if parklot_inid and isinstance(parklot_inid, list):
            vehicleinout_infos = vehicleinout_infos.filter(
                parklot_inid__in=parklot_inid
            )
        if orderby:
            vehicleinout_infos = vehicleinout_infos.order_by(orderby)

        return vehicleinout_infos

    @classmethod
    def complex(
        cls,
        parklotids=None,
        platenum=None,
        min_intime=None,
        max_intime=None,
        min_outtime=None,
        max_outtime=None,
        appuser=None,
        orderby=None,
        maxres=None,
        startindex=None,
        pagedirect=None,
    ):

        vehicleinout_infos = cls.vehicleinout_infos

        if min_intime:
            vehicleinout_infos = vehicleinout_infos.filter(
                in_time__gt=min_intime
            )

        if max_intime:
            vehicleinout_infos = vehicleinout_infos.filter(
                in_time__lt=max_intime
            )

        if min_outtime:
            vehicleinout_infos = vehicleinout_infos.filter(
                out_time__gt=min_outtime
            )

        if max_outtime:
            vehicleinout_infos = vehicleinout_infos.filter(
                out_time__lt=max_outtime
            )

        if platenum:
            vehicleinout_infos = vehicleinout_infos.filter(
                plate_number__startswith=platenum
            )

        if parklotids:
            vehicleinout_infos = vehicleinout_infos.filter(
                parklot_id__in=parklotids
            )

        if appuser:
            vehicleinout_infos = vehicleinout_infos.filter(user_id=appuser)

        if orderby:
            vehicleinout_infos = vehicleinout_infos.order_by(orderby)

        if vehicleinout_infos is None:
            return None, None, None

        if maxres is None or startindex is None or pagedirect is None:
            return vehicleinout_infos, None, None

        return Paginator.paginate(
            vehicleinout_infos, maxres, startindex, pagedirect
        )
