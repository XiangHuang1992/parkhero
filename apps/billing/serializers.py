# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: serializers.py
# @ide: PyCharm
# @time: 2019-07-29 09:53
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from rest_framework import serializers
from .models import OfflinePayment
from .models import (
    JournalAccount,
    AliPayLog,
    DaDaPayLog,
    UnionPayLog,
    WeChatPayLog,
)


class OfflinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflinePayment
        fields = ("id", "plate_number", "payment_time", "parklot", "amount")


class JournalAccountSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = JournalAccount
        fields = (
            "id",
            "user",
            "out_trade_no",
            "created_time",
            "updated_time",
            "paid",
            "payment_channel",
            "amount",
            "balance",
            "order_desc",
        )


class AliPayLogSerializer(serializers.ModelSerializer):
    notify_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = AliPayLog
        fields = (
            "subject",
            "payment_type",
            "service",
            "trade_no",
            "trade_status",
            "buyer_email",
            "buyer_id",
            "quantity",
            "price",
            "total_fee",
            "discount",
            "is_total_fee_adjust",
            "user_coupon",
            "gmt_create",
            "gmt_payment",
            "notify_time",
            "notify_id",
        )


class DaDaPayLogSerializer(serializers.ModelSerializer):
    trade_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:S")

    class Meta:
        model = DaDaPayLog
        fields = (
            "service_id",
            "service_type",
            "charged_duration",
            "price",
            "trade_time",
            "bill_type",
        )


class UnionPayLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnionPayLog
        fields = (
            "trade_time",
            "pay_timeout",
            "cert_id",
            "tn",
            "resp_code",
            "resp_msg",
            "query_id",
            "notify_code",
            "notify_msg",
            "settle_amount",
            "settle_currency_code",
            "settle_date",
            "trace_no",
            "trace_time",
        )


class WeChatPayLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatPayLog
        fields = (
            "app_id",
            "mch_id",
            "trade_type",
            "prepay_id",
            "open_id",
            "transaction_id",
            "fee_type",
            "bank_type",
            "total_fee",
            "cash_fee",
            "is_subscribe",
            "time_end",
        )
