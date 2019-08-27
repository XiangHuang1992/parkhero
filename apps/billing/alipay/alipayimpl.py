# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: alipayimpl.py
# @ide: PyCharm
# @time: 2019-07-29 15:20
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
from datetime import datetime
import logging
from urllib.parse import parse_qs
from django.http import HttpResponse

from config.settings.local import BASE_URL

from config.status_code import STATUS_CODE

from ..models import AliPayLog
from ..paybase import PayBase, PAYHANDLERS
from .alipay import AliPay
from .alipayconfig import AliPayConfig
from .alipaynotify import AliPayNotify


ali_channel_config = {
    'partner': '2088702805407911',
    'seller_id': '18600508272',
    'partner_private_key_file': 'config/keyperms/ali_partner_pri_key.pem',
    'partner_public_key_file': 'config/keyperms/ali_partner_pub_key.pem',
    'alipay_public_key_file': 'config/keyperms/ali_pub_key.pem',
    'notify_url': BASE_URL + '/billing/onlinepay/',
    'sign_type': 'RSA'
}

logger = logging.getLogger(__name__)


class AliPayImpl(PayBase):
    """ alipay interface """

    def __int__(self, request, it_b_pay="30m"):
        self.params = dict()
        self.params["subject"] = "哒哒停车"
        self.params["body"] = "哒哒停车-账户充值"
        self.params["service"] = "mobile"
        self.params["payment_type"] = 1
        self.params["_input_charset"] = "utf-8"
        self.params["it_b_pay"] = it_b_pay

        self.request = request
        self.amount = 0

    def verify_params(self):
        amount = self.request.Get.get["amount"]

        try:
            self.amount = float(amount)
        except ValueError:
            detail = dict()
            detail["detail"] = "Please provide a valid amount value."
            detail["status"] = STATUS_CODE["errparam"]
            logger.error(detail)
            return None, STATUS_CODE["errparam"]

        amount_fen = int(self.amount * 100)
        return (
            {"order_desc": self.params["body"], "amount": amount_fen},
            STATUS_CODE["success"],
        )

    def generate_trade(self, out_trade_no):
        """ init alipay config, return specific order number """
        alipayconfig = AliPayConfig(ali_channel_config)
        alipay = AliPay(alipayconfig)
        self.params["out_trade_no"] = out_trade_no
        self.params["total_fee"] = self.amount
        self.params["notify_url"] = alipayconfig.notify_url

        alipay.set_params(params=self.params)
        order = alipay.get_order_string()

        return order, None

    def generate_order(self, journalaccount):
        """ generate alipay order """
        alipaylog = AliPayLog()
        alipaylog.journal = journalaccount
        alipaylog.subject = self.params["subject"]
        alipaylog.payment_type = self.params["payment_type"]
        alipaylog.service = self.params["service"]
        alipaylog.it_b_pay = self.params["it_b_pay"]

        alipaylog.save()

    def notify_preproces(self, data):
        """ preprocess notify content """
        notify = data.decode("utf-8")
        notify_list_value = parse_qs(notify)

        notice = {}
        for (k, v) in notify_list_value.items():
            notice[k] = v[0]

        alipayconfig = AliPayConfig(ali_channel_config)
        alipaynotify = AliPayNotify(alipayconfig)

        verify = alipaynotify.sign_verify(notice)
        retval = (
            STATUS_CODE["success"] if verify else STATUS_CODE["wrong_param"]
        )
        return retval, notice

    def update_order(self, journalaccount, notice):
        """ update order at notify stage """
        alipaylog = AliPayLog.objects.get(journal=journalaccount)
        alipaylog.trade_no = notice.get("trade_no")
        alipaylog.trade_status = notice.get("trade_status")
        alipaylog.buyer_email = notice.get("buyer_email")
        alipaylog.buyer_id = notice.get("buyer_id")
        alipaylog.quantity = notice.get("quantity")
        alipaylog.price = notice.get("price")
        alipaylog.total_fee = notice.get("total_fee")
        alipaylog.discount = notice.get("discount")
        alipaylog.is_total_fee_adjust = notice.get("is_total_fee_adjust")
        alipaylog.use_coupon = notice.get("use_coupon")
        alipaylog.payment_type = notice.get("payment_type")
        alipaylog.gmt_create = notice.get("gmt_create")
        alipaylog.gmt_payment = notice.get("gmt_payment", "")
        alipaylog.notify_time = notice.get("notify_time")
        alipaylog.notify_id = notice.get("notify_id")

        alipaylog.save()

    def complete_trade(self, statuscode=None):
        return HttpResponse("success", content_type="application/text")


PAYHANDLERS["alipay"] = AliPayImpl
