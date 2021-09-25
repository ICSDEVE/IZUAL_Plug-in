#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : WeiBo.py
# @Time    : 09/25/21 22:16:18
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

from sdk.weibo import WeiBo


weibo = WeiBo()

class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.playList = []
        self.idx = 0

    def handle(self, text, parsed):
        if self.nlu.hasIntent(parsed, "GET_WEIBO"):
            slots = self.nlu.getSlots(parsed, 'GET_WEIBO')
            for slot in slots:
                if slot['name'] == 'user_person':
                    self.person = slot['normalized_word']
                    if self.person == "MiracleInk":
                        self.person = "Jehovah"
                    self.playList = weibo.getInfo(self.person)
                    self.say("{}最近的一条微博发布于{}。{}".format(slot['normalized_word'], self.playList[0]['time'], self.playList[0]['content']))
        elif self.nlu.hasIntent(parsed, "NEXT_CONTENT"):
            if self.idx + 1 >= len(self.playList):
                self.say("已经是最后一条信息了")
            else:
                self.idx += 1
                self.say("{}发布于{}的一条微博。{}".format(self.person, self.playList[self.idx]['time'], self.playList[self.idx]['content']))
        elif self.nlu.hasIntent(parsed, 'LAST_CONTENT'):
            if self.idx - 1 <= 0:
                self.say("已经是第一条微博了")
            else:
                self.idx -= 1
                self.say("{}发布于{}的一条微博。{}".format(self.person, self.playList[self.idx]['time'], self.playList[self.idx]['content']))
        elif self.nlu.hasIntent(parsed, 'EXIT_WEIBO'):
            self.clearImmersive()
            self.say('已退出微博插件')
        else:
            self.say('无法理解您的意思，如果要退出微博，请说退出微博')

    def restore(self):
        pass

    def isValidImmersive(self, text, parsed):
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['LAST_CONTENT', 'NEXT_CONTENT',
                                                                     'GET_WEIBO', 'EXIT_WEIBO'])

    def isValid(self, text, parsed):
        return unit.hasIntent(parsed, 'GET_WEIBO')

