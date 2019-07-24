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

    def login_check(request):
        """
        todo: diff anonymous user and login user
        :return:
        """
        pass

    def group_check(user, groupname):
        """
        todo: verify user whether not belong so specify group
        # only spec group are allowed to operate on parking lot objects
        :param groupname:
        :return:
        """
        pass

    def auth_check(self):
        """
        todo: verify user whether not login and belong to specify group
        :return:
        """
        pass

    def app_user_login(user):
        """
        todo: verify whether not app user
        :return:
        """
        pass

