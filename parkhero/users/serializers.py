# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: serializers.py
# @ide: PyCharm
# @time: 2019-07-23 18:16
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'account_balance', 'avatar', 'id_card_number', 'nickname',
            'password']
