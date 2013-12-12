import Twytbot
import time

C_KEY = ''
C_SECRET = ''
ACCESS_TOK = ''
SECRET_TOK = ''
NAME = ''

perceval = Twytbot.twytbot(C_KEY, C_SECRET, ACCESS_TOK, SECRET_TOK, NAME)

perceval.addpattern('dichotomie',"C'est pas faux !")
while True:
    perceval.run()
    time.sleep(10000)
