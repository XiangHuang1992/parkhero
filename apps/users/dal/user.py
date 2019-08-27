# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: user.py
# @ide: PyCharm
# @time: 2019-08-02 09:30
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from django.db.models.manager import Manager
from apps.common.paginator import Paginator

from django.contrib.auth import get_user_model

User = get_user_model()


class DalUser:
    """ User's module's dal """

    usermanobj = User.objects

    @classmethod
    def simple(
        cls,
        profileid=None,
        userid=None,
        idnum=None,
        nickname=None,
        orderby=None,
    ):

        user_infos = cls.usermanobj

        if profileid:
            user_infos = user_infos.filter(pk=profileid)

        if userid:
            user_infos = user_infos.filter(user=userid)

        if idnum:
            user_infos = user_infos.filter(id_card_num=idnum)

        if nickname:
            user_infos = user_infos.filter(nick_name__startswith=nickname)

        if orderby:
            user_infos = user_infos.order_by(orderby)

        return user_infos

    @classmethod
    def complex(
        cls,
        profileid=None,
        userid=None,
        idnum=None,
        nickname=None,
        orderby=None,
        maxres=None,
        startindex=None,
        pagedirect=None,
    ):

        user_infos = cls.usermanobj

        if profileid:
            user_infos = user_infos.filter(pk=profileid)

        if userid:
            user_infos = user_infos.filter(user=userid)

        if idnum:
            user_infos = user_infos.filter(id_card_number=idnum)

        if nickname:
            user_infos = user_infos.filter(nick_name__contains=nickname)

        if orderby:
            user_infos = user_infos.order_by(orderby)

        if maxres is None or startindex is None or pagedirect is None:
            return user_infos, None, None

        return Paginator.paginate(user_infos, maxres, startindex, pagedirect)
