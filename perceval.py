#! /usr/bin/python
#! *-* encoding: utf-8 *-*

import Twytbot
import time
import settings

perceval = Twytbot.twytbot(C_KEY, C_SECRET, ACCESS_TOK, SECRET_TOK, NAME)

perceval.addpattern('dichotomie',"C'est pas faux !")
while True:
    perceval.run()
    time.sleep(420)
