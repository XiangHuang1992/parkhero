# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: parklot.py
# @ide: PyCharm
# @time: 2019-07-26 16:58
# @desc: ===============================================
# parklot's dal, return queryset
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from parkhero.common.paginator import Paginator
from parkhero.parking.models import ParkingGate, ParkingLot


class DalParkLots:
    parklots_infos = ParkingLot.objects

    @classmethod
    def simple(
        cls, parklotid=None, identifier=None, is_active=None, parklotname=None
    ):
        parklots_infos = cls.parklots_infos

        if parklotid:
            parklots_infos = parklots_infos.filter(pk=parklotid)

        if identifier:
            parklots_infos = parklots_infos.filter(identifier=identifier)

        if not (is_active is None):
            parklots_infos = parklots_infos.filter(is_active=is_active)

        if parklotname:
            parklots_infos = parklots_infos.filter(name=parklotname)

        return parklots_infos

    @classmethod
    def complex(cls, **kwargs):
        lot_type = kwargs.get("lot_type", None)
        identifier = kwargs.get("identifier", None)
        is_active = kwargs.get("is_active", None)
        parklotid = kwargs.get("parklotid", None)
        name = kwargs.get("name", None)
        city_code = kwargs.get("city_code", None)
        orderby = kwargs.get("orderby", None)
        maxres = kwargs.get("maxres", None)
        startindex = kwargs.get("startindex", None)
        pagedirect = kwargs.get("pagedirect", None)

        parklot_infos = cls.parklots_infos

        if identifier:
            parklot_infos = parklot_infos.filter(identifier=identifier)
        if lot_type is not None:
            lot_type = (
                "CP"
                if "common" == lot_type.lower()
                else "RP"
                if "open" == lot_type.lower()
                else "SP"
            )
            parklot_infos = parklot_infos.filter(lot_type=lot_type)
        if not (is_active is None):
            parklot_infos = parklot_infos.filter(is_active=is_active)

        if parklotid and not isinstance(parklotid, list):
            parklot_infos = parklot_infos.filter(pk=parklotid)
        if parklotid and isinstance(parklotid, list):
            parklot_infos = parklot_infos.filter(pk__in=parklotid)
        if city_code:
            parklot_infos = parklot_infos.filter(city_code=city_code)
        if name:
            parklot_infos = parklot_infos.filter(name__contains=name)
        if orderby:
            parklot_infos = parklot_infos.order_by(orderby)
        if maxres is None or startindex is None or pagedirect is None:
            return parklot_infos, None, None

        return Paginator.paginate(
            parklot_infos, maxres, startindex, pagedirect
        )


class DalParkGate:
    parkgate_infos = ParkingGate.objects

    @classmethod
    def simple(
        cls,
        parklotid=None,
        gateid=None,
        gatetype=None,
        longitude=None,
        latitude=None,
        lngmin=None,
        lngmax=None,
        latmin=None,
        latmax=None,
    ):

        parkgate_infos = cls.parkgate_infos

        if parklotid and not isinstance(parklotid, list):
            parkgate_infos = parkgate_infos.filter(parklot=parklotid)
        if parklotid and isinstance(parklotid, list):
            parkgate_infos = parkgate_infos.filter(parklot__in=parklotid)
        if gateid:
            parkgate_infos = parkgate_infos.filter(gateid=gateid)
        if gatetype:
            parkgate_infos = parkgate_infos.filter(gatetype=gatetype)
        if latitude:
            parkgate_infos = parkgate_infos.filter(latitude=latitude)
        if longitude:
            parkgate_infos = parkgate_infos.filter(longitude=longitude)
        if lngmin:
            parkgate_infos = parkgate_infos.filter(longitude__gt=lngmin)
        if lngmax:
            parkgate_infos = parkgate_infos.filter(longitude__lt=lngmax)
        if latmin:
            parkgate_infos = parkgate_infos.filter(latitude__gt=latmin)
        if latmax:
            parkgate_infos = parkgate_infos.filter(latitude__lt=latmax)

        return parkgate_infos
