#! /usr/bin/python
#! *-* encoding: utf-8 *-*

import Twytbot
import time
import settings
import logging

logging.basicConfig(level=logging.INFO, filename='perceval.log', format='%(asctime)s:%(name)s:%(levelname)-8s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
logging.getLogger().addHandler(console)

perceval = Twytbot.twytbot(settings.C_KEY, settings.C_SECRET, settings.ACCESS_TOK, settings.SECRET_TOK, settings.NAME)

perceval.addpattern('dichotomie',"C'est pas faux !")
perceval.addpattern('sinécure',"Ouais, C'est pas faux !")
perceval.addpattern('insipide',"C'est pas faux !")
while True:
    perceval.run()
    time.sleep(300)
