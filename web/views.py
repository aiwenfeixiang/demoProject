#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/2/27

import json

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from utils.polyv import polyv_video

from web import models


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # logger.debug("get ip:{} from request.".format(ip))
    return ip


def sentry_demo(request):
    """
    关于 `sentry` 的具体使用, 主要用作于日志收集的管理工具

    访问 `sentry.io` 注册，并创建项目, 在settings添加DSN
    """
    division_by_zero = 1 / 0


def log(request):
    """
    `django` 日志系统

    文档参见: https://docs.djangoproject.com/en/1.11/topics/logging/
    """
    import logging
    logger = logging.getLogger('django.request')
    logger.error("你好")
    return HttpResponse("OK")


def send_mail(request):
    """
    发送邮件

    前提：请在配置文件中配置邮箱属性
    """
    from django.core.mail import send_mail
    # 关于更多邮件客户端可使用
    # from django.core.mail import EmailMultiAlternatives
    # msg = EmailMultiAlternatives(
    #     "邮件标题", "邮件内容", from_email=settings.DEFAULT_FROM_EMAIL, to=settings.SEND_EMAIL_NOTICE
    # )
    # 如果发送内容为`html`格式的话, 设置这个属性即可
    # msg.content_subtype = "html"
    # msg.send()

    # 如果发送内容为`html`格式的话, 多传 `html_message`
    result = send_mail(
        "你好", "世界", "admin@luffycity.com", ["404042726@qq.com", ],
    )
    print(result)

    return HttpResponse("Ok")


def play(request):

    vid = "03b56854c0970bde8598a0659e8cafa6_0"

    extra_params = polyv_video.get_verify_data(
        vid, _get_client_ip(request), 'customuserid', 'customid',
    )
    # print(extra_params)

    return render(request, "play.html", context={"vid": vid, "extra_params": extra_params})


def verify(request):
    vid = request.GET.get("vid")
    # 自定义
    code = request.GET.get("code", "")

    # 获取签名使用
    t = request.GET.get("t")
    callback = request.GET.get("callback")

    # 逻辑校验是否可进行观看视频
    # auth_video_play = AuthVideoPlay(request, vid)
    # if auth_video_play.is_valid():
    #     status = 1
    # else:
    #     status = 2

    username = "xxx"

    # 计算可播放的签名
    play_sign = polyv_video.get_play_key(vid, username, code, 2, t)

    resp = polyv_video.get_resp(2, username, play_sign, '放置具体的异常信息')

    if callback:
        resp = "{}({})".format(callback, resp)
    else:
        resp = json.dumps(resp)

    from django.shortcuts import HttpResponse

    return HttpResponse(resp)


def rw(request):

    res = models.Tag.objects.all()
    print(res)

    models.Tag.objects.create(name="哈哈哈哈")

    return HttpResponse("ok")


def delay_task(request):
    """
    celery 调用方式

    更多请参见: https://docs.celeryproject.org/en/latest/userguide/calling.html

    """
    from web import tasks

    # --- Params ----
    # countdown  多少秒之后执行 type: int
    # eta        具体什么时间执行 type: datetime
    # retry      是否启用重试   type: bool

    # 第一种
    tasks.add.delay()
    # 第二种
    # tasks.reduce.apply_async(args=(10, 5))
    # 第三种
    # from celery import current_app
    # current_app.send_task("add", )

    return HttpResponse("ok")


def jwt(request):
    """依托于 `pyjwt` 库

    示例框架库:

    # django
        djangorestframework-jwt

    # sanic (在生产中进行应用过)
    sanic-jwt

    # other

    """

    import jwt

    encoded_jwt = jwt.encode(
        # 存储的内容
        {'username': 'liuzhichao', 'mobile': '12312', 'email': '23@qq.com'},
        # 秘钥
        settings.SECRET_KEY,
        # 加密方式
        algorithm='HS256'
    )

    data = jwt.decode(encoded_jwt, key=settings.SECRET_KEY)
    print(data)
    return HttpResponse("ok")


def send_template(request):

    from utils.wx.api import wx_api

    resp1 = wx_api.client.message.send_text("ogPhC1Il5Vy4YmHR4PM3c3WqKOKE", "sdf")
    print(resp1)
    resp2 = wx_api.client.message.send_template(
        "ogPhC1Il5Vy4YmHR4PM3c3WqKOKE",
        "5Gi6etDlj9Q8q1Sj1wwQ1KgZ1v3q-16eTJDr0AUsMRE",
        {"first": {"value": "哈哈"}},
        url="www.baidu.com"
    )
    print(resp2)
    return HttpResponse("ok")


def ali_pay(request):
    # 支付宝支付接口使用
    from utils.ali.api import ali_api
    # PC支付
    ali_api.pay.pc.direct("洗发水", "1231231331", "100")
    # 移动端支付
    ali_api.pay.wap.direct("洗发水", "1231231331", "100")
    # app支付
    ali_api.pay.app.direct("洗发水", "1231231331", "100")

    return HttpResponse("ok")


def ali_sms(request):
    """
    发送短信

    doc:
    https://dysms.console.aliyun.com/dysms.htm
    """
    import json

    from django.utils.crypto import get_random_string

    from utils.ali.api import ali_api

    # 如果是多个手机号, 逗号隔开即可
    ali_api.yun.sms.send(
        "18803561683",
        "海贼王",
        "SMS_157282376",
        json.dumps({"code": get_random_string("1234567890", 6)})
    )

    return HttpResponse("ok")
