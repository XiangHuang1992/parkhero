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
    "phone_number_not_registered": 20004,  # 该手机号未被注册
    "user_no_profile": 20005,  # 该用户没有配置数据
    "pay_password_err": 20006,  # 支付密码错误
    "pay_password_not_exists": 20007,  # 没有支付密码
    "trade_num_not_exists": 20008,  # 该订单号不存在
    "user_password_err": 20009,  # 用户名密码错误
    "non_administrator": 20010,  # 不是管理员
    "non_such_user": 20011,  # 没有该用户
    "non_such_role": 20012,  # 没有该角色
    "username_exists": 20013,  # 用户名已存在
    "non_operator": 20014,  # 不是操作员
    "non_auth_del_group": 20015,  # 没有删除用户组的权限
    "group_name_exists": 20016,  # 该用户组已存在
    "user_inactive": 20017,  # 该用户未被激活

    # 支付模块(billing)

}
