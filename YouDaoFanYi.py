#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : YouDaoFanYi.py
# @Time    : 09/25/21 22:20:53
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
import hashlib
import json
import random
import re

import requests
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "youdao"

    def translate(self, appId, appSecret, sentence):
        url = 'https://openapi.youdao.com/api'
        salt = random.randint(1, 65536)
        sign = appId+sentence+str(salt)+appSecret
        m1 = hashlib.md5(sign.encode('utf-8'))
        sign = m1.hexdigest()
        params = {
                 'q': sentence,
                 'from': 'auto',
                 'to': 'auto',
                 'appKey': appId,
                 'salt': salt,
                 'sign': sign
        }
        result = requests.get(url, params=params)
        res = json.loads(result.text, encoding='utf-8')
        s = res['translation'][0]
        return s


    def getSentence(self, text):
        pattern1 = re.compile("翻译.*?")
        pattern2 = re.compile(".*?的翻译")

        if re.match(pattern1, text) is not None:
            sentence = text.replace("翻译", "")
        elif re.match(pattern2, text) is not None:
            sentence = text.replace("的翻译", "")
        else:
            sentence = ""
        sentence = sentence.replace(",", "")
        sentence = sentence.replace("，", "")
        return sentence


    def handle(self, text, parsed):
        profile = config.get()
        if self.SLUG not in profile or \
           'appId' not in profile[self.SLUG] or\
           'appSecret' not in profile[self.SLUG]:
            self.say('有道翻译插件配置错误，激活插件失败', cache=True)
            return
        appId = profile[self.SLUG]['appId']
        appSecret = profile[self.SLUG]['appSecret']
        sentence = self.getSentence(text)
        logger.info('sentence: ' + sentence)
        if sentence:
            try:
                s = self.translate(appId, appSecret, sentence)
                if s:
                    self.say(sentence+"的翻译是" + s, cache=False)
                else:
                    self.say("翻译" + sentence + "失败，请稍后再试", cache=False)
            except Exception as e:
                logger.error(e)
                self.say('无法翻译此内容' + sentence, cache=False)
        else:
            self.say(u"没有听清，请重试", cache=True)


    def isValid(self, text, parsed):
        return u"翻译" in text
