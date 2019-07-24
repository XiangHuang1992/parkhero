# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: serializers.py
# @ide: PyCharm
# @time: 2019-07-24 22:35
# todo: 后续需要添加需要序列化的字段
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from rest_framework import serializers
from .models import ParkingLot, ParkingGate, ParkingLotExtra, VehicleInOut


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ()


class ParkingGateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingGate
        fields = ()


class VehicleInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInOut
        fields = ()


class ParkingLotExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLotExtra
        fields = ()
