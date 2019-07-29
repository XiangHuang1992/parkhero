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
    "non_unpaid_bill": 30001,  # 没有支付的订单
    "paychannel_nonsupport": 30002,  # 该支付方式不支持
    "service_nonsupport": 30003,  # 该服务不支持
    "such_bill_exists": 30004,  # 该账单已存在
    "non_enough_balance": 30005,  # 余额不足
    "non_such_bill": 30006,  # 没有该账单
    "non_bill": 30007,  # 没有账单
    "bill_paid": 30008,  # 订单已支付
    # web后台模块
    "non_valid_packname": 40001,  # 不是有效的app包名
    "non_app_release": 40002,  # 没有app发布
    "non_such_parklot": 40003,  # 没有该停车场
    "such_parklot_exist": 40004,  # 该停车场已存在
    "non_parklot": 40005,  # 没有停车场
    "non_vehiclein_record": 40006,  # 没有停车入场记录
    "non_vehicleout_record": 40007,  # 没有停车出场记录
    "non_offlinepay_record": 40008,  # 没有线下缴费记录
    "non_onlinepay_record": 40009,  # 没有线上缴费记录
    "non_such_parkgate": 40010,  # 没有该停车场入口
    "non_parkgate": 40011,  # 该停车场没有入口
    "invalid_plate_number": 40012,  # 不正确的车牌号
    "non_vehicle_found": 40013,  # 不存在该号牌的车辆
    "such_parkgate_exist": 40015,  # 该停车场出入口已存在
    "non_recharge_record": 40016,  # 没有充值记录
    # 停车场模块
    "non_inout_record": 50001,  # 没有进出场记录
    "such_inout_exist": 50002,  # 该进出场记录已存在
    # 停车场通信模块
    # app 用户概况模块
    "only_appuser": 70001,  # 仅限于app用户
    "has_non_vehicle": 70002,  # 没有车辆
    "has_non_userprofile": 70003,  # 没有用户配置数据
    # app版本模块
    "non_file_exists": 80001,  # 文件不存在
    "non_startup_image": 80002,  # 没有启动页面图片
    "non_index_image": 80003,  # 没有首页页面图片
    "non_cover_image": 80004,  # 没有封面图片
    "such_version_exists": 80005,  # 该版本已存在
    # 短信模块
    # 路边停车模块
}
