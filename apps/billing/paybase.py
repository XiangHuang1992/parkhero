# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: paybase.py
# @ide: PyCharm
# @time: 2019-07-29 11:22
# @desc: ===============================================
# pay base class, to offer public interface
# Life is Short I Use Python!!!                      ===
# ======================================================
"""
PAYHANDLERS = {}


class PayBase:
    """ pay public interface """

    def verify_params(self):
        """
         specific handler verify the params. return params:
         { spbill_create_ip, order_desc }, status
         """
        pass

    def generate_trade(self, out_trade_no):
        """ init specific pay config, return specific order number """
        pass

    def generate_order(self, journalaccount):
        """ generate specific pay order """
        pass

    def notify_preproces(self, data):
        """ preprocess notify content """
        pass

    def update_order(self, journalaccount, notice):
        """ update order at notify stage """
        pass

    def complete_trade(self, statuscode=None):
        """ return specific success value """
        pass
