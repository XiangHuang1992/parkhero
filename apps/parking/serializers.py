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
from .models import ParkLot, ParkingGate, ParkingLotExtra, VehicleInOut


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkLot
        fields = (
            "id",
            "name",
            "city_code",
            "type",
            "price",
            "image",
            "parking_space_total",
        )


class ParkingLotSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ParkLot
        fields = (
            "id",
            "identifier",
            "name",
            "address",
            "city_code",
            "type",
            "price",
            "parking_space_total",
            "image",
        )


class ParkingGateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingGate
        fields = ("gateid", "longitude", "latitude", "gatename", "isdefault")


class VehicleInOutSerializer(serializers.ModelSerializer):
    in_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    out_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = VehicleInOut
        fields = (
            "id",
            "phone_number",
            "park_card_num",
            "card_type",
            "out_time",
            "in_time",
            "parklot",
        )


class ParkingLotExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLotExtra
        fields = (
            "parklot",
            "parkspace_available",
            "login_time",
            "heartbeat_time",
            "mqttip",
            "httpip",
        )
