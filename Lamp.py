#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : Lamp.py
# @Time    : 09/25/21 23:19:00
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
import importlib

from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG="Lamp"

    def handle(self, text, parsed):
        import wiringpi

        # get config
        profile = config.get()
        pin=profile[self.SLUG]['pin']
        wiringpi.wiringPiSetupPhys()
        wiringpi.pinMode(pin,1)

        if any(word in text for word in [u"打开",u"开启"]):
            wiringpi.digitalWrite(pin,0)
            self.say("已打开台灯", cache=True)
        elif any(word in text for word in [u"关闭",u"关掉",u"熄灭"]):
            wiringpi.digitalWrite(pin,1)
            self.say("已关闭台灯", cache=True)

    def isValid(self, text, parsed):
        return importlib.util.find_spec('wiringpi') and \
            "台灯" in text
