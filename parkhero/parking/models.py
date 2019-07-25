from django.contrib.auth import get_user_model
from django.db import models
import architect

# Create your models here.

User = get_user_model()


class ParkingLot(models.Model):
    COMMON_PARKING_LOT = "CP"
    SMART_PARKING_LOT = "SP"
    RODE_SIDE_PARKING_LOT = "RP"
    PARKING_LOT_TYPES = (
        (COMMON_PARKING_LOT, "封闭"),
        (SMART_PARKING_LOT, "智能"),
        (RODE_SIDE_PARKING_LOT, "路边"),
    )
    name = models.CharField(max_length=128)
    identifier = models.IntegerField(default=0, unique=True, db_index=True)
    address = models.CharField(max_length=200)
    city_code = models.IntegerField(default=0, db_index=True)
    type = models.CharField(
        choices=PARKING_LOT_TYPES, max_length=2, default=COMMON_PARKING_LOT
    )
    price = models.CharField(max_length=200)
    parking_space_total = models.IntegerField(default=0)
    image = models.CharField(max_length=200)

    # RSA KEY
    private_key = models.CharField(max_length=1000)
    public_key = models.CharField(max_length=1000)

    # never delete parking lots, just mark as inactive
    is_active = models.BooleanField(default=True)
    owner = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        permissions = ()
        default_permissions = ()

        verbose_name = "停车场"
        verbose_name_plural = verbose_name


class ParkingLotExtra(models.Model):
    parklot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE)
    parkspace_available = models.IntegerField(default=None, null=None)
    login_time = models.DateTimeField(default=None, null=None)
    heartbeat_time = models.DateTimeField(default=None, null=None)
    mqttip = models.GenericIPAddressField(max_length=50, null=True)
    httpip = models.GenericIPAddressField(max_length=50, null=True)

    class Meta:
        default_permissions = ()


class VehicleIn(models.Model):
    parklot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE)
    plate_number = models.CharField(null=True, max_length=15, default=None)
    parkcard_num = models.CharField(null=True, max_length=20, default=None)
    cardgenre = models.CharField(null=True, max_length=15, default=None)
    created_time = models.DateTimeField(db_index=True)
    updated_time = models.DateTimeField(null=True, default=None)
    parklot_inid = models.CharField(db_index=True, max_length=40)

    in_vehicle_img = models.URLField(null=True, default=None)
    in_plate_img = models.URLField(null=True, default=None)
    in_time = models.DateTimeField(db_index=True, null=True, default=None)
    in_prices = models.CharField(max_length=1000, null=True, default=None)
    in_space_available = models.IntegerField(null=True, default=None)
    in_updated_time = models.DateTimeField(null=True, default=None)

    out_prices = models.CharField(max_length=1000, null=True, default=None)
    out_price_change_time = models.DateTimeField(null=True, default=None)

    class Meta:
        default_permissions = ()


# 该装饰器的功能是对数据库表分区
@architect.install(
    "partition",
    type="range",
    subtype="date",
    constraint="month",
    column="created_time",
)
class VehicleInOut(models.Model):
    parklot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE)  # 停车场
    plate_number = models.CharField(
        null=True, max_length=15, default=None
    )  # 车牌号
    park_card_num = models.CharField(
        null=True, max_length=20, default=None
    )  # 停车卡号
    card_type = models.CharField(
        null=True, max_length=15, default=None
    )  # 类型，卡类型
    parking_space_total = models.IntegerField(default=0)  # 该停车场的总车位数
    created_time = models.DateTimeField(db_index=True)  # record created
    user = models.ForeignKey(
        User, null=True, default=None, on_delete=models.CASCADE
    )  # 进出场记录的付费用户
    updated_time = models.DateTimeField(null=True, default=None)
    parklot_in_id = models.CharField(db_index=True, max_length=40)

    in_vehicle_img = models.URLField(null=True, default=None)
    in_plate_img = models.URLField(null=True, default=None)
    in_time = models.DateTimeField(db_index=True, null=True, default=True)
    in_prices = models.CharField(max_length=1000, null=True, default=None)
    in_space_available = models.IntegerField(null=True, default=None)
    in_upload_datetime = models.DateTimeField(null=True, default=None)

    out_vehicle_img = models.URLField(null=True, default=None)
    out_plate_img = models.URLField(null=True, default=None)
    out_time = models.DateTimeField(db_index=True, null=True, default=None)
    out_prices = models.CharField(max_length=1000, null=True, default=None)
    out_prices_change_time = models.DateTimeField(null=True, default=None)
    out_space_available = models.IntegerField(null=True, default=None)
    out_upload_time = models.DateTimeField(null=True, default=None)

    class Meta:
        default_permissions = ()


class ParkingGate(models.Model):
    gateid = models.AutoField(primary_key=True)
    longitude = models.FloatField(default=0, db_index=True)
    latitude = models.FloatField(default=0, db_index=True)
    gatetype = models.PositiveSmallIntegerField()  # 1. 入口  2. 出口 3. 出入口
    getename = models.CharField(max_length=20, null=True, default=None)
    isdefault = models.BooleanField(default=True)
    parklot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE)

    class Meta:
        db_table = "parking_parkgate"
        default_permissions = ()
