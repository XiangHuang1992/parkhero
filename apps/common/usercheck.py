# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: usercheck.py
# @ide: PyCharm
# @time: 2019-07-24 22:46
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
import base64
import binascii

from django.contrib.auth import authenticate, login
from rest_framework.authentication import get_authorization_header

from config.status_code import STATUS_CODE

import logging

logger = logging.getLogger(__name__)


class UserCheck:
    @staticmethod
    def login_check(request):
        """
        todo: diff anonymous user and login user
        :return:
        """
        logger.info("login as user[%s]", request.user)
        if not request.user.is_authenticated():
            detail = dict()
            detail["detail"] = "Please login"
            detail["status"] = STATUS_CODE["need_login"]
            return 1, detail
        return 0, None

    @staticmethod
    def group_check(user, groupname):
        """
        todo: verify user whether not belong so specify group
        # only spec group are allowed to operate on parking lot objects
        :param groupname:
        :return:
        """
        role_list = [i["name"] for i in user.groups.values()]
        logger.info("Role list[%s]", role_list)
        if groupname not in role_list:
            logger.error("Please login as %s.", groupname)
            detail = dict()
            detail["detail"] = {"Please login as %s." % groupname}
            detail["status"] = STATUS_CODE["non_right"]
            return 1, detail
        return 0, role_list

    @staticmethod
    def auth_check(request, groupname):
        """
        todo: verify user whether not login and belong to specify group
        :return:
        """
        ret_val, ret_detail = UserCheck.login_check(request)
        if ret_val != 0:
            return 1, ret_detail
        ret_val, ret_detail = UserCheck.group_check(request.user, groupname)

        if ret_val != 0:
            return 2, ret_detail

        return 0, ret_detail

    @staticmethod
    def app_user_login(user):
        """
        todo: verify whether not app user
        :return:
        """
        role_list = [i["name"] for i in user.groups.values()]

        _is_app_user = False

        if isinstance(role_list, list):
            _is_app_user = not role_list or (
                role_list and "default" not in role_list
            )

        return _is_app_user
