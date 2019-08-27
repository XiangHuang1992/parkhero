# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: comment.py
# @ide: PyCharm
# @time: 2019-08-02 09:30
# @desc: ===============================================
# comment's dal, return queryset
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from django.db.models.manager import Manager
from apps.common.paginator import Paginator


class DalComment:
    def simple(self):
        pass

    @classmethod
    def complex(
        cls,
        commentmanobj,
        user=None,
        created_time=None,
        orderby=None,
        maxres=None,
        startindex=None,
        pagedorect=None,
    ):

        if not isinstance(commentmanobj, Manager):
            return None, None, None

        comment_infos = commentmanobj

        if user:
            comment_infos = comment_infos.filter(owner=user)

        if created_time:
            comment_infos = comment_infos.filter(created_time__gt=created_time)

        if orderby:
            comment_infos = comment_infos.order_by(orderby)

        if maxres is None or startindex is None or pagedorect is None:
            return comment_infos, None, None

        return Paginator.paginate(
            comment_infos, maxres, startindex, pagedorect
        )
