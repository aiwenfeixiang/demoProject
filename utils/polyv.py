#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/5/29

import json
import time
import requests
import logging
import hashlib

# from django.conf import settings


def _generate_md5_num(string):
    md5 = hashlib.md5()
    md5.update(bytes(str(string), encoding="utf8"))  # 对字符串加密
    return md5.hexdigest()  # 取到密文


logger = logging.getLogger(__name__)


class PolyvVideo(object):

    # USER_ID = settings.VIDEO_CONFIG["POLYV"]["USER_ID"]
    USER_ID = "03b56854c0"

    # SECRET_KEY = settings.VIDEO_CONFIG["POLYV"]["SECRET_KEY"]
    SECRET_KEY = "G128dqgzTp"

    def get_verify_data(self, vid, remote_addr, uid=None, username="", extra_params="HTML5"):
        """获取加密视频播放数据

        Parameters
        ----------
        vid : string
            视频 `vid`

        remote_addr: dict
            请求地址

        uid: string
            用户UID

        username: int
            用户username

        extra_params: string

            扩展参数

        Returns
        -------
        string
        """
        time_stamp = int(time.time() * 1000)

        # 加密数据
        sign_data = {
            "userId": self.USER_ID,
            "videoId": vid,
            "ts": time_stamp,
            "viewerIp": remote_addr,
            "viewerId": uid,
            "viewerName": username,
            "extraParams": extra_params
        }
        # 数据排序
        ordered_data = sorted(
            (
                (k, v if not isinstance(v, dict) else json.dumps(v, separators=(',', ':')))
                for k, v in sign_data.items()
            )
        )
        # 拼接加密数据
        sign_string = "{}{}{}".format(
            self.SECRET_KEY,
            "".join(["{}{}".format(item[0], item[1]) for item in ordered_data]),
            self.SECRET_KEY,
        )

        sign_data.update({"sign": _generate_md5_num(sign_string).upper()})
        # 请求可以播放视频的凭证

        res = requests.post(
            url="https://hls.videocc.net/service/v1/token",
            headers={
                "Content-type": "application/x-www-form-urlencoded"
            },
            data=sign_data
        ).json()

        logger.info("POLYV TOKEN RESULT： {}".format(res))

        data = {} if isinstance(res, str) else res.get("data", {})

        return {
            "token": data.get("token"),
            "sign": _generate_md5_num("{}{}{}".format(self.SECRET_KEY, vid, time_stamp)),
            "time_stamp": time_stamp
        }

    def get_play_key(self, vid, username, code, status, t):
        """获取授权播放 `key`

        Parameters
        ----------
        vid : string
            视频 `vid`

        username: dict
            响应跑马灯展示

        code: string
            自定义参数

        status: int

            是否可播放,  1、可播放 2、禁播

        t: string

            时间戳

        Returns
        -------
        string
        """
        return _generate_md5_num("vid={}&secretkey={}&username={}&code={}&status={}&t={}".format(
            vid, self.SECRET_KEY, username, code, status, t
        )).lower()

    @staticmethod
    def get_resp(status, username, sign, msg="授权暂未通过"):
        return {
            "status": status,
            "username": username,
            "sign": sign,
            "msg": msg,
            "fontSize": "18",
            "fontColor": "0xFF0000",
            "speed": "50",
            "filter": "on",
            "setting": "2",
            "alpha": "0.7",
            "filterAlpha": "1",
            "filterColor": "0x3914AF",
            "blurX": "2",
            "blurY": "2",
            "tweenTime": "1",
            "interval": "3",
            "lifeTime": "3",
            "strength": "4",
            "show": "on"
        }


polyv_video = PolyvVideo()
