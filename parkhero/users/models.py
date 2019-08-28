from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import CharField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


UserProfile = get_user_model()


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    avatar = CharField(max_length=100)
    id_card_number = CharField(max_length=20)
    nick_name = CharField(max_length=100)
    account_balance = IntegerField(default=0)
    payment_password = CharField(max_length=50)

    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username


class BankCard(models.Model):
    owner = models.ForeignKey(UserProfile)
    number = models.CharField(max_length=20)
    binded = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class Vehicle(models.Model):
    owner = models.ManyToManyField(UserProfile)
    plate_number = models.CharField(max_length=15)

    def __str__(self):
        return self.plate_number


class Role(models.Model):
    owner = models.ManyToManyField(UserProfile)
    role = models.CharField(max_length=20)
    permssion = models.IntegerField(default=0)

    def __str__(self):
        return self.role


class OperatorProfile(models.Model):
    user = models.OneToOneField(UserProfile)

    avatar = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username


class ParkongLotGroup(models.MOdel):
    pass
