from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    avatar = models.CharField(_("avatar profile"), max_length=100, default='')
    nick_name = models.CharField(_("user nick name"), max_length=100, default='')
    id_card_number = models.CharField(_("parking card number"), max_length=20, default=0)
    account_balance = models.IntegerField(_("account balance"), default=0)
    payment_password = models.CharField(_("user payment password"), max_length=50,
        blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {'name': self.name, 'nick_name': self.nick_name}

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class VerificationCode(models.Model):
    phone_number = models.CharField(_("phone number"), max_length=11)
    verification_code = models.CharField(_("verification code"), max_length=6)
    created_time = models.DateTimeField(_("created time"), auto_now=True)

    class Meta:
        default_permissions = ()
        verbose_name = "验证码"
        verbose_name_plural = verbose_name


class BlackList(models.Model):
    uuid = models.CharField(max_length=40)
    plate_number = models.CharField(max_length=15, db_index=True)
    user_id = models.CharField(max_length=20, null=True)
    amount = models.IntegerField(default=0)
    blacking = models.SmallIntegerField(default=1)
    created_time = models.DateTimeField()
    update_time = models.DateTimeField()
    memo = models.CharField(max_length=1024)

    class Meta:
        db_table = "account_blacklist"
        default_permissions = ()
        verbose_name = "黑名单"
        verbose_name_plural = verbose_name
