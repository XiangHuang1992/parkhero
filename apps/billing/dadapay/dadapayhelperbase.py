# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: dadapayhelperbase.py
# @ide: PyCharm
# @time: 2019-07-29 17:03
# @desc: ===============================================
# dadapay 的帮助接口
# Life is Short I Use Python!!!                      ===
# ======================================================
"""

from abc import ABCMeta, abstractmethod

# 'parkingpay': { 'orderdesc': '哒哒停车--停车缴费', 'handler': }
DADAPAYHELPERS = {}
"""

调用顺序:
    verifyparamshelper -> orderservicehelper -> tradeservicehelper -> updateorderhelper ->
    completetradehelper

    其中verifyparamshelper和updatetradehelper需要保存传进来的参数
    verifyparamshelper和orderservicehelper在dadapayimpl的verify_params里面被调用
    tradeservicehelper在dadapayimpl的generate_trade里调用
    而verifyparamshelper、orderservicehelper、tradeservicehelper三个都是在onlinepay的get方法里调用
    所以这三个方法里保存的实例变量是不能和在post里调用的方法共享。因此tradeservicehelper是不需要保存变量

    updateorderhelper和completetradehelper是在onlinepay的post方法被调用，所以在这两者之间可以进行实例变量的传递。

"""


class DadapayHelperBase(metaclass=ABCMeta):
    """
    dadapay的帮助接口类
    """

    @abstractmethod
    def verifyparamshelper(self, request):
        """参数验证帮助接口"""
        pass

    @abstractmethod
    def orderservicehelper(self, request):
        """订单服务帮助接口"""
        pass

    @abstractmethod
    def tradeservicehelper(self, request):
        """交易服务帮助接口"""
        pass

    @abstractmethod
    def updateorderhelper(self, request):
        """订单更新帮助接口"""
        pass

    @abstractmethod
    def completetradehelper(self, request):
        """交易完成帮助接口"""
        pass
