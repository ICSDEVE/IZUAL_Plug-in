#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : Reboot.py
# @Time    : 09/25/21 22:46:57
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
import subprocess
import time

from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = 'reboot'

    def onConfirm(self, input):
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK", u"Okay"]):
            self.say('Authorization succeeded', cache=True)
            time.sleep(3)
            subprocess.Popen("reboot -f", shell=True)
            return
        self.say('Authorization failed', cache=True)

    def handle(self, text, parsed):
        try:
            self.say('即将重启系统，请在提示音后进行确认，授权相关操作', cache=True, onCompleted=self.onConfirm(self.activeListen()))
        except Exception as e:
            logger.error(e)
            self.say('Reboot failed', cache=True)

    def isValid(self, text, parsed):
        return any(word in text for word in [u"重启", u"重新启动"])
