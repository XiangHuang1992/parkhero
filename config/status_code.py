# -*- encoding: utf-8 -*-
"""
# @version: 0.1
# @author: ferdinand
# @email: ferinandhx@gmail.com
# @flie: status_code.py
# @ide: PyCharm
# @time: 2019-07-23 18:22
# @desc: ===============================================
# Life is Short I Use Python!!!                      ===
# 描述系统状态码为200的情况下，本应用的异常状态
# ======================================================
"""

STATUS_CODE = {
    # 系统级状态码
    "success": 0,
    "unknown_err": 10000,  # 未知原因错误
    "err_param": 10001,  # 参数错误
    "lost_param": 10002,  # 缺少必要参数
    "database_err": 10003,  # 数据库错误
    "network_err": 10004,  # 网络错误
    "need_login": 10005,  # 需要登录才能进行下一步操作
    "non_right": 10006,  # 没有权限
    "invalid_opt": 10007,  # 无效操作
    "file_op_err": 10008,  # 文件操作出错
    "rsa_sign_err": 10009,  # 签名出错

    # 账号模块
    "verify_code_expired": 20000,  # 验证码过期
    "verify_code_invalid": 20001,  # 验证码无效
    "verify_code_wait": 20002,  # 请等待验证码下发
    "phone_number_registered": 20003,  # 该手机号已被注册

}
