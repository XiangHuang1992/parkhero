from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class ParkingLot(models.Model):
    pass


class ParkingLotExtra(models.Model):
    pass


class VehicleIn(models.Model):
    pass


class VehicleInOut(models.Model):
    pass


class ParkingGate(models.Model):
    pass
