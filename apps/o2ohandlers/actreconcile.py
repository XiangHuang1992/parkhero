# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: actreconcile.py
# @ide: PyCharm
# @time: 2019-08-02 16:46
# @desc: ===============================================
# handle reconcile event
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime
import logging

from django.db import DatabaseError, transaction

from apps.billing.models import DaDaPayLog, Reconcile, JournalAccount
from apps.parking.dal.parklot import DalParkLots
from apps.parking.dal.vehicleinout import DalVehicleInOut
from config.status_code import STATUS_CODE

from .evenbase import ACTHANDLERS
from .evenbase import EventBase

logger = logging.getLogger(__file__)


class ActReconcileHandler(EventBase):
    """ handle online pay Reconcile event class"""

    def acthandle(self, eventdata):
        identifier = eventdata.get("idnetifier")
        starttime = eventdata.get("starttime")
        endtime = eventdata.get("endtime")

        reconciles = eventdata.get("reconciles")

        parklotinfos = DalParkLots.simple(identifier=identifier)

        detail = dict()

        if not parklotinfos.exists():
            detail["status"] = STATUS_CODE["non_such_parklot"]
            logger.warning(detail)
            return detail

        parklot = parklotinfos[0]

        vehicle_inidset = set()

        for item in reconciles:
            vehicle_inid = str(item.get("inid"))
            vehicle_inidset.add(vehicle_inid)
        plateforminouts = DalVehicleInOut.simple(parklotids=[parklot.id])
        # 上传时间小于支付时间
        plateforminouts = plateforminouts.filter(user__isnull=False)
        plateforminouts = plateforminouts.filter(updated_time__gt=starttime).filter(
            updated_time__lt=endtime
        )

        if not plateforminouts.exists():
            detail["status"] = STATUS_CODE["non_inout_record"]
            logger.warning(detail)
            return detail

        detail["status"] = STATUS_CODE["success"]

        vehicleid2inids = {}
        identicals = (
            []
        )  # platenumber and parlot both have. just judge amount are consistent
        parklotlose = []  # parklot non

        for item in plateforminouts:
            vehicleid2inids[item.id] = [item.parklot_inid, item.plate_number]

            if item.parklot_inid in vehicle_inidset:
                identicals.append(item.id)
                vehicle_inidset.remove(item.parklot_inid)
            else:
                parklotlose.append(item.id)

        if not detail.get("plateformlose"):
            detail["plateformlose"] = []

        newreconciles = []

        # vehicle_inidset is not none, otherwise plateformlose
        for item in reconciles:
            vehicle_inid = str(item.get("inid"))

            if vehicle_inid in vehicle_inidset:
                reconcile_infos = Reconcile.objects.filter(
                    parklot_inid=item.get("inid")
                ).filter(parklot=parklot)
                if reconcile_infos.exists():
                    continue

                reconcile = Reconcile()
                reconcile.parklot = parklot
                reconcile.plate_number = item.get("carno")
                reconcile.parklot_inid = item.get("inid")
                reconcile.paymoney = item.get("paymoney")
                reconcile.paytime = item.get("paytime")
                reconcile.status = 1
                newreconciles.append(reconcile)

                loseitem = {
                    "paymoney": item.get("paymoney"),
                    "inid": item.get("inid"),
                    "carno": item.get("carno"),
                    "paytime": item.get("paytime"),
                }

                detail["plateformlose"].append(loseitem)

        dadapaylog_infos = DaDaPayLog.objects.filter(
            serviceid__in=list(vehicleid2inids.keys())
        ).filter(servicetype="parkingpay")

        if not detail.get("parklotlose"):
            detail["parklotlose"] = []

        checkjournals = []

        for item in dadapaylog_infos:
            if item.serviceid in identicals:
                item.journal.ischeck = True
                item.journal.checktime = datetime.now()
                checkjournals.append(item.journal)

            if item.serviceid in parklotlose:
                item.journal.checktime = datetime.now()
                checkjournals.append(item.journal)
                loseitem = {
                    "paymony": item.journal.amount,
                    "inid": vehicleid2inids.get(item.serviceid)[0],
                    "carno": vehicleid2inids.get(item.serviceid)[1],
                    "paytime": item.trade_time.strftime("%Y-%m-%d %H:%M:%S"),
                }

                detail["parklotlose"].append(loseitem)

        try:
            with transaction.atomic():
                Reconcile.objects.bulk_create(newreconciles)
                JournalAccount.objects.bulk_create(checkjournals)

        except DatabaseError as e:
            detail["detail"] = "%s" % e
            detail["status"] = STATUS_CODE["database_err"]
            return detail

        detail["disaccord"] = []
        logger.warning(detail)
        return detail


ACTHANDLERS["reconcile"] = ActReconcileHandler
