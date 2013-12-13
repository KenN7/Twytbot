#! /usr/bin/python
#! *-* encoding: utf-8 *-*

import Twytbot
import time
import settings
import logging

logging.basicConfig(level=logging.INFO, filename='perceval.log')

perceval = Twytbot.twytbot(settings.C_KEY, settings.C_SECRET, settings.ACCESS_TOK, settings.SECRET_TOK, settings.NAME)

perceval.addpattern('dichotomie',"C'est pas faux !")
while True:
    perceval.run()
    time.sleep(420)
