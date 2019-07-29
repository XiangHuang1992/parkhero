# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: parklotextra.py
# @ide: PyCharm
# @time: 2019-07-26 17:48
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from parkhero.parking.models import ParkingLotExtra


class DalParkLotExtra:
    parklotextra_infos = ParkingLotExtra.objects

    @classmethod
    def simple(cls, parklotids=None):
        parklotextra_infos = ParkingLotExtra.objects

        if parklotids and not isinstance(parklotids, list):
            parklotextra_infos = parklotextra_infos.filter(
                parklot_id=parklotids
            )
        if parklotids and isinstance(parklotids, list):
            parklotextra_infos = parklotextra_infos.filter(
                parklot_id__in=parklotids
            )

        return parklotextra_infos

    @classmethod
    def complex(cls, **kwargs):
        pass
