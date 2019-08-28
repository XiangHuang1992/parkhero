#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class ParkingLot(models.Model):
    COMMON_PARKING_LOT = "CP"
    SMART_PARKING_LOT = "SP"
    ROAD_SIDE_PARKING_LOT = "RP"
    PARKING_LOT_TYPES = (
        (COMMON_PARKING_LOT, "Common Parking Lot"),
        (SMART_PARKING_LOT, "Smart Parking Lot"),
        (ROAD_SIDE_PARKING_LOT, "Rode-side Parking Lot"),
    )

    # TODO unique
    name = models.CharField(max_length=128)
    identifier = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    city_code = models.IntegerField(default=0)
    type = models.CharField(
        max_length=2, choices=PARKING_LOT_TYPES, default=COMMON_PARKING_LOT
    )

    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    diatance = models.FloatField(default=0)
    price = models.CharField(max_length=200)

    parking_space_total = models.CharField(max_length=1000)
    public_key = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class ParkingSpace(models.Model):
    SMALL = "S"
    MIDDLE = "M"
    LARGE = "L"
    PARKING_SPACE_TYPE = (
        (SMALL, "Small Parking Space"),
        (MIDDLE, "Middle Parking Space"),
        (LARGE, "Large Parking Space"),
    )

    AVALIABLE = "A"
    OCCUPIED = "O"
    PROPRIETARY = "P"
    PARKING_SPACE_STATUS = (
        (AVALIABLE, "Avaliable"),
        (OCCUPIED, "Occupied"),
        (PROPRIETARY, "Proprietary"),
    )

    identifier = models.CharField(max_length=10)
    type = models.CharField(max_length=1, choices=PARKING_SPACE_TYPE, default=SMALL)
    parking_lot = models.ForeignKey("ParkingLot")
    floor = models.SmallIntegerField(default=1)
    status = models.CharField(
        max_length=1, choices=PARKING_SPACE_STATUS, default=AVALIABLE
    )

    def __str__(self):
        return self.identifier


class VehicleIn(models.Model):
    parking_lot = models.ForeignKey("ParkingLot")
    plate_number = models.CharField(max_length=15)
    parking_card_number = models.CharField(max_length=20)
    vehicle_img = models.URLField()
    plate_img = models.URLField()
    type = models.CharField(max_length=15)
    out_time = models.CharField(max_length=25)
    time_stamp = models.BigIntegerField(default=0)
    notice_id = models.CharField(max_length=40)
    price_list = models.CharField(max_length=1000)
    parkling_space_total = models.IntegerField(default=0)
    parking_space_available = models.IntegerField(default=0)
    created_time = models.DateTimeField()

    def __str__(self):
        return self.plate_number


class RoadSideParkingRegister(models.Model):
    user = models.ForeignKey(User)
    parking_space = models.ForeignKey("ParkingSpace")
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)
