# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: payment.py
# @ide: PyCharm
# @time: 2019-08-02 21:56
# @desc: ===============================================
# payonline payoffline's dal, return queryset
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from apps.common.paginator import Paginator
from ..models import JournalAccount, OfflinePayment
from django.db import models


class DalOfflinePay:
    offlinepayment = OfflinePayment.objects

    """ offline payment module's dal """

    @classmethod
    def simple(
        cls, parklotids=None, platenums=None, payment_time=None, parklot_inid=None
    ):
        """ no input parameter query, return queryset """
        offlinepay_infos = cls.offlinepayment

        if parklotids and isinstance(parklotids, list):
            offlinepay_infos = offlinepay_infos.filter(parklot_id__in=parklotids)

        elif parklotids:
            offlinepay_infos = offlinepay_infos.filter(parklot=parklotids)

        if payment_time:
            offlinepay_infos = offlinepay_infos.filter(payment_time__gt=payment_time)

        if platenums and not isinstance(platenums, list):
            offlinepay_infos = offlinepay_infos.filter(
                plate_number__startswith=platenums
            )

        if platenums and isinstance(platenums, list):
            offlinepay_infos = offlinepay_infos.filter(plate_number__in=platenums)

        if parklot_inid:
            offlinepay_infos = offlinepay_infos.filter(parklot_inid=parklot_inid)

        return offlinepay_infos

    @classmethod
    def complex(
        cls,
        parklotids=None,
        platenums=None,
        payment_time=None,
        orderby=None,
        maxres=None,
        startindex=None,
        pagedirect=None,
    ):
        """ contain vary condition query, return queryset, default order by id """

        offlinepay_infos = cls.offlinepayment

        if parklotids and isinstance(parklotids, list):
            offlinepay_infos = offlinepay_infos.filter(parklot_id__in=parklotids)
        elif parklotids:
            offlinepay_infos = offlinepay_infos.filter(parklot_id=parklotids)

        if payment_time:
            offlinepay_infos = offlinepay_infos.filter(payment_time__gt=payment_time)

        if platenums and not isinstance(platenums, list):
            offlinepay_infos = offlinepay_infos.filter(
                plate_number__startswith=platenums
            )

        if platenums and isinstance(platenums, list):
            offlinepay_infos = offlinepay_infos.filter(plate_number__in=platenums)

        if orderby:
            offlinepay_infos = offlinepay_infos.order_by(orderby)

        if maxres is None or startindex is None or pagedirect is None:
            return offlinepay_infos, None, None

        return Paginator.paginate(offlinepay_infos, maxres, startindex, pagedirect)


class DalOnlineBill:
    """ online bill module's dal """

    onlinebill = JournalAccount.objects

    @classmethod
    def simple(
        cls,
        journalid=None,
        out_trade_no=None,
        appuser=None,
        paid=None,
        payment_channel=None,
    ):
        """ no input parameter query, return queryset and not paging """
        onlinebill_infos = cls.onlinebill

        if journalid:
            onlinebill_infos = onlinebill_infos.filter(pk=journalid)

        if out_trade_no:
            onlinebill_infos = onlinebill_infos.filter(out_trade_no=out_trade_no)

        if appuser:
            onlinebill_infos = onlinebill_infos.filter(user=appuser)

        if payment_channel:
            onlinebill_infos = onlinebill_infos.filter(payment_channel=payment_channel)

        if not (paid is None):
            onlinebill_infos = onlinebill_infos.filter(paid=paid)

        return onlinebill_infos

    @classmethod
    def complex(
        cls,
        journalids=None,
        user=None,
        paid=None,
        payment_channel=None,
        mincreatedtime=None,
        maxcreatedtime=None,
        minupdatedtime=None,
        maxupdatedtime=None,
        orderby=None,
        maxres=None,
        startindex=None,
        pagedirect=None,
    ):

        """ contain vary condition query, return queryset, default order by id and
        paging """

        onlinebill_infos = cls.onlinebill

        if journalids:
            onlinebill_infos = onlinebill_infos.filter(pk__in=journalids)

        if user:
            onlinebill_infos = onlinebill_infos.filter(user=user)

        if not (paid is None):
            onlinebill_infos = onlinebill_infos.filter(paid=paid)

        if payment_channel:
            onlinebill_infos = onlinebill_infos.filter(payment_channel=payment_channel)

        if mincreatedtime:
            onlinebill_infos = onlinebill_infos.filter(created_time__gt=mincreatedtime)

        if maxcreatedtime:
            onlinebill_infos = onlinebill_infos.filter(created_time__lt=maxcreatedtime)

        if minupdatedtime:
            onlinebill_infos = onlinebill_infos.filter(updated_time__gt=minupdatedtime)

        if maxupdatedtime:
            onlinebill_infos = onlinebill_infos.filter(updated_time__lt=maxupdatedtime)

        if orderby:
            onlinebill_infos = onlinebill_infos.order_by(orderby)

        if maxres is None or startindex is None or pagedirect is None:
            return onlinebill_infos, None, None

        return Paginator.paginate(onlinebill_infos, maxres, startindex, pagedirect)
