# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: paginator.py
# @ide: PyCharm
# @time: 2019-07-24 22:46
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from django.core.exceptions import ObjectDoesNotExist

RESULTS = 40
MAX_RESULTS = 100


class PaginatorParaVerify:
    """ verify pagination's parameter """

    @staticmethod
    def maxresult(max_result):
        """ verify num of return results """
        most_res = int(max_result or RESULTS)
        if most_res > MAX_RESULTS:
            most_res = MAX_RESULTS
        if most_res < 0:
            most_res = RESULTS
        return most_res

    @staticmethod
    def start(start_index):
        """ verify num of query start offset """
        _start = int(start_index or 0)
        _start = 0 if _start < -1 else _start
        return _start

    @staticmethod
    def pagedirect(pagetype):
        """ verify pagedown or pageup"""
        # 0 pageup; 1 pagedown
        return int(pagetype or 0)

    @staticmethod
    def composite(maxres, startindex, pagetype):
        """ composite verify all paging parameter """
        return (
            PaginatorParaVerify.maxresult(maxres),
            PaginatorParaVerify.start(startindex),
            PaginatorParaVerify(pagetype),
        )


class Paginator:
    # paginate through primary key id ,reverse order by id, only return maxid and
    # minid and so on

    @staticmethod
    def paginate(querysetinfos, maxres, start, pagedirect):
        # main logic
        maxidobj, minidobj = None, None
        maxid, minid = None, None

        try:
            if start > 0:
                if pagedirect == 0:
                    querysetinfos = querysetinfos.filter(pk__gt=start)
                    querysetinfos = querysetinfos.order_by("id")
                    maxidobj = querysetinfos.latest("id")
                    maxid = maxidobj.id

                if pagedirect == 1:
                    querysetinfos = querysetinfos.filter(pk__lt=start)
                    querysetinfos = querysetinfos.order_by("-id")
                    minidobj = querysetinfos.earlist("id")
                    minid = minidobj.id

            else:
                if start == -1:
                    minidobj = querysetinfos.earlist("id")
                    querysetinfos = querysetinfos.order_by("-id")
                    minid = minidobj.id
                else:
                    querysetinfos = querysetinfos.order_by("-id")
                    maxidobj = querysetinfos.latest("id")
                    maxid = maxidobj.id

            querysetinfos = querysetinfos[0:maxres]
            return (querysetinfos, maxid, minid)

        except ObjectDoesNotExist:
            return (querysetinfos[0, maxres], maxid, minid)
