import architect
from django.contrib.auth import get_user_model
from django.db import models

from apps.parking.models import ParkLot

User = get_user_model()

# Create your models here.

"""
todo:需要增加一张冻结表，所有未完成的交易记录都放在该表中。比如往IC卡充值。先将账余额相应充值数额的条目放在该表中，交易成功后，将它删除，交易失败退给相应用户。

length of each field:
type     - 10
amount   - 13
id       - 32
time     - 30
desc     - 50
url      - 80
"""


@architect.install(
    "partition", type="range", subtype="date", constraint="month", column="created_time"
)
class JournalAccount(models.Model):
    user = models.ForeignKey(
        User, null=True, default=None, on_delete=models.CASCADE
    )  # 兼容第三方缴费，app用户id
    out_trade_no = models.CharField(
        max_length=50, db_index=True
    )  # 外部交易号，用来和WeChat，alipay，等交互
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 该流水创建时间
    updated_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 该流水更新时间
    paid = models.BooleanField(default=False)  # 是否支付完成
    payment_channel = models.CharField(max_length=10)  # 支付通道，目前有四种
    amount_receivable = models.IntegerField(default=0)  # 本流水设计的应收金额数量，即总金额，以分计
    amount_paid = models.IntegerField(default=0)  #
    # 本流水涉及的实收金额数量，以分计，如果是缴费，则从app账户实收，不能出现负数
    balance = models.IntegerField(default=0)  # 用户的余额，当为第三方缴费时，可能为0，或者直接使用amount
    spbill_create_ip = models.GenericIPAddressField(max_length=50)  # 该流水创建时的app用户ip
    order_desc = models.CharField(max_length=50)  # 该流水的描述名称
    is_check = models.BooleanField(default=False)  # 对账标志，已对账为True，False为消费
    check_time = models.DateTimeField(db_index=True, null=True)  #
    # 对账时间，只要对过账，就需要更新这个字段，不管是否一致

    """
    a. 未支付，等待付款
    b. 未支付，订单超时关闭
    c. 已付款，订单未完成
    d. 已支付，订单已完成
    e. 正在退款，订单未完成
    f. 已退款，订单已完成
    g. 线下已支付（线上未支付），订单关闭
    h. 用户取消
    """
    status = models.SmallIntegerField(null=True)  # 账单状态
    service_id = models.IntegerField(db_index=True, null=True, default=None)  #
    # 业务流水id，根据业务类型来定

    service_type = models.CharField(max_length=32, null=True, default=None)  #
    # 业务类型，如充值退款各作为一种， 停车缴费，充电缴费各作为一种
    memo = models.CharField(max_length=200, null=True, default=None)  # 该交易记录的备注

    class Meta:
        default_permissions = ()


class WeChatPayLog(models.Model):
    journal = models.ForeignKey("JournalAccount", on_delete=models.CASCADE)
    app_id = models.CharField(max_length=32)
    mch_id = models.CharField(max_length=32)
    trade_type = models.CharField(max_length=20)
    prepay_id = models.CharField(max_length=50)

    open_id = models.CharField(max_length=32, null=True)
    transaction_id = models.CharField(max_length=32, null=True)
    fee_type = models.CharField(max_length=10, null=True)
    bank_type = models.CharField(max_length=10, null=True)
    total_fee = models.CharField(max_length=13, null=True)
    cash_fee = models.CharField(max_length=13, null=True)
    is_subscribe = models.CharField(max_length=4, null=True)
    time_end = models.DateTimeField(db_index=True, default=None, null=True)

    class Meta:
        default_permissions = ()


class AliPayLog(models.Model):
    journal = models.ForeignKey("JournalAccount", on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=4)
    service = models.CharField(max_length=80)
    it_b_pay = models.CharField(max_length=5)
    trade_no = models.CharField(max_length=32, null=True)
    trade_status = models.CharField(max_length=20, null=True)
    buyer_email = models.CharField(max_length=50, null=True)
    buyer_id = models.CharField(max_length=50, null=True)
    quantity = models.CharField(max_length=5, null=True)
    price = models.CharField(max_length=13, null=True)
    total_fee = models.CharField(max_length=13, null=True)
    discount = models.CharField(max_length=13, null=True)
    is_total_fee_adjust = models.CharField(max_length=4, null=True)
    use_coupon = models.CharField(max_length=4, null=True)
    gmt_create = models.CharField(max_length=30, null=True)
    gmt_payment = models.CharField(max_length=30, null=True)
    notify_time = models.CharField(db_index=True, default=None, null=True, max_length=20)
    notify_id = models.CharField(max_length=50, null=True)

    class Meta:
        default_permissions = ()


class UnionPayLog(models.Model):
    journal = models.ForeignKey("JournalAccount", on_delete=models.CASCADE)
    trade_time = models.DateTimeField(db_index=True)
    pay_timeout = models.CharField(max_length=30)

    cert_id = models.CharField(max_length=32)
    tn = models.CharField(max_length=32)
    resp_code = models.CharField(max_length=10)
    resp_msg = models.CharField(max_length=50)

    query_id = models.CharField(max_length=32, null=True)
    notify_code = models.CharField(max_length=10, null=True)
    notify_msg = models.CharField(max_length=50, null=True)
    settle_amount = models.CharField(max_length=13, null=True)
    settle_currency_code = models.CharField(max_length=10, null=True)
    settle_date = models.CharField(max_length=30, null=True)
    trace_no = models.CharField(max_length=32, null=True)
    trace_time = models.DateTimeField(db_index=True, default=None, null=True)

    class Meta:
        default_permissions = ()


class DaDaPayLog(models.Model):
    journal = models.ForeignKey("JournalAccount", on_delete=models.CASCADE)
    charged_duration = models.IntegerField(default=0)
    price = models.CharField(max_length=1000)

    trade_time = models.DateTimeField(db_index=True, null=True)

    bill_type = models.CharField(max_length=10, default="normal")
    memo = models.CharField(max_length=200, null=True, default=None)

    class Meta:
        default_permissions = ()


class Reconcile(models.Model):
    """ 对账不一致的数据保存在此表 """

    journal = models.ForeignKey(
        JournalAccount, null=True, default=None, on_delete=models.CASCADE
    )
    parklot = models.ForeignKey(ParkLot, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=15)
    parklot_inid = models.CharField(db_index=True, max_length=40)
    paytime = models.DateTimeField(db_index=True, null=True)
    paymoney = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    class Meta:
        default_permissions = ()


@architect.install(
    "partition", type="range", subtype="date", constraint="month", column="created"
)
class OfflinePayment(models.Model):
    PAYMENT = "PY"
    TIMEOUT_PAYMENT = "TO"
    PAYMENT_TYPES = (
        (PAYMENT, "payment for parking time"),
        (TIMEOUT_PAYMENT, "payment for not leaving on time"),
    )

    parklot = models.ForeignKey(ParkLot, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=15)
    parking_card_number = models.CharField(max_length=20)
    amount = models.CharField(default=0, max_length=10)
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPES, default=PAYMENT)

    payment_time = models.DateTimeField(db_index=True)
    uploaded_time = models.DateTimeField(
        null=True, default=None
    )  # uploaded by parking lot
    parklot_in_id = models.CharField(max_length=40, null=True)  # 停车场的进场记录id
    price_list = models.CharField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)  # record created

    def __str__(self):
        return self.plate_number

    class Meta:
        default_permissions = ()
