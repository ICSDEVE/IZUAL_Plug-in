#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : SpeakIP.py
# @Time    : 09/25/21 21:56:03
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
import socket
import subprocess
import time

from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "local_ip"

    def getLocalIP(self):
        ip = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('114.114.114.114', 0))
            ip = s.getsockname()[0]
        except:
            name = socket.gethostname()
            ip = socket.gethostbyname(name)
        if ip.startswith("127."):
            cmd = '''/sbin/ifconfig | grep "inet " | cut -d: -f2 | awk '{print $1}' | grep -v "^127."'''
            a = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            a.wait()
            out = a.communicate()
            # ALL LISTS
            ip = out[0].strip().split("\n")
            if len(ip) == 1 and ip[0] == "" or len(ip) == 0:
                return False
            ip = 'Completed'.join(ip)
        return ip

    def handle(self, text, parsed):
        try:
            count = 0
            while True:
                ip = self.getLocalIP()
                logger.debug('getLocalIP: ', ip)
                if ip == False:
                    self.say('Getting local ip...', cache=True)
                else:
                    count += 1
                    ip += 'Completed'
                    self.say(ip, cache=True)
                if count == 1:
                    break
                time.sleep(1)
        except Exception as e:
            logger.error(e)
            self.say('IP address not found', cache=True)

    def isValid(self, text, parsed):
        return any(word in text for word in [u"IP", u"网络地址", u"IP地址"])
