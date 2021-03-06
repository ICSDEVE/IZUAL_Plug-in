#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ///////////////////////////////////////////////////////////////
#
# @Author  : Jehovah
# @File    : SpeakTemperature.py
# @Time    : 09/25/21 22:17:03
# @Version : v1.0
#
# We will use this project for commercial purposes in the future.
# If you need to change or imitate (including GUI), please let us know about it.
#
# ///////////////////////////////////////////////////////////////

## ==> IMPORT MODULE
# ///////////////////////////////////////////////////////////////
import importlib
import time

from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "temperature"

    def getTempperature(self, temp):
        from RPI import GPIO
        data = []
        j = 0
        # ENTER THE GPIO NUMBER
        channel =0
        channel = int(temp)
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(channel, GPIO.HIGH)
        GPIO.setup(channel, GPIO.IN)

        while GPIO.input(channel) == GPIO.LOW:
          continue
        while GPIO.input(channel) == GPIO.HIGH:
          continue

        while j < 40:
          k = 0
          while GPIO.input(channel) == GPIO.LOW:
            continue
          while GPIO.input(channel) == GPIO.HIGH:
            k += 1
            if k > 100:
              break
          if k < 8:
            data.append(0)
          else:
            data.append(1)
          j += 1
        logger.info("SENSOR IS WORKING...")
        logger.debug(data)
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

        for i in range(8):
          humidity += humidity_bit[i] * 2 ** (7-i)
          humidity_point += humidity_point_bit[i] * 2 ** (7-i)
          temperature += temperature_bit[i] * 2 ** (7-i)
          temperature_point += temperature_point_bit[i] * 2 ** (7-i)
          check += check_bit[i] * 2 ** (7-i)

        tmp = humidity + humidity_point + temperature + temperature_point

        if check == tmp:
           logger.info("temperature :", temperature, "*C, humidity :", humidity, "%")
           return "????????????"+str(temperature)+"??????????????????????????????"+str(humidity)
        else:
          # return "SENSOR ERROR"
          self.getTempperature(channel)
        GPIO.cleanup()

    def handle(self, text, parsed):
        profile = config.get()
        if self.SLUG not in profile or \
           'gpio' not in profile[self.SLUG]:
            self.say('DHT11?????????????????????????????????', cache=True)
            return
        if 'gpio' in profile[self.SLUG]:
            temp = profile[self.SLUG]['gpio']
        else:
            temp = profile['gpio']
        try:
            temper = self.getTempperature(temp)
            logger.debug('getTempperature: ', temper)
            self.say(temper)
        except Exception as e:
            logger.critical("???????????? {}".format(e))
            self.say('??????????????????', cache=True)

    def isValid(self, text, parsed):
        return importlib.util.find_spec('RPI') and \
            any(word in text for word in [u"??????", u"????????????"])
