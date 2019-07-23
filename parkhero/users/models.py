from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    avatar = CharField(_("avatar profile"), max_length=100)
    nick_name = CharField(_("user nick name"), max_length=100)
    id_card_number = CharField(_("parking card number"), max_length=20)
    account_balance = IntegerField(_("account balance"), default=0)
    payment_password = CharField(_("user payment password"), max_length=50)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {'name': self.name, 'nick_name': self.nick_name}

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
