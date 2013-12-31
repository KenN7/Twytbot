#!/usr/bin/python

import twython
import time
import json
from random import choice,gauss
import re

import logging
log = logging.getLogger(__name__)

class twytbot:
    def __init__(self, key, secret, accesstok, secrettok, name):
        self.KEY = key
        self.SECRET = secret
        self.ACCESS_TOKEN = accesstok
        self.SECRET_TOKEN = secrettok
        self.MYNAME = name
        self.last_id = 0
        self.patterns = {}
        self.twitter = 0
        self.randomness = ['\o/',';)',':)',':p','/o/','|o|',':D','!','.','..',':/',':o','=)',':>']
        self.id_dict = {}

    def authentificate(self):
        self.twitter = twython.Twython(self.KEY, self.SECRET, self.ACCESS_TOKEN, self.SECRET_TOKEN)
        try:
            #self.twitter.verify_credentials()
            pass
        except Exception as e:
            log.warning("Twitter login failed : %s" % e)
            raise

    def addpattern(self, search, response):
        self.patterns[search] = response
        log.info("Added pattern : '%s : %s'" % (search,response))

    def sendtweet(self, user, response, message_id):
        text = "@%s %s %s" % (user,response,choice(self.randomness))
        log.info("Sending '%s'" % text)
        self.twitter.update_status(status=text, in_reply_to_status_id=message_id)

    def saveid(self, max_id):
        log.info("Saving max_ids")
        outfile = open('lastid.txt', 'w')
        json.dump(max_id, outfile)
        outfile.close()

    def getid(self):
        log.info("Loading last_ids")
        infile = open('lastid.txt', 'r')
        last_id = json.load(infile)
        infile.close()
        return last_id

    def run(self):
        log.info("Bot started on %s" % time.ctime())
        self.authentificate()
        try:
            self.id_dict = self.getid()
        except Exception as e:
            log.warning(e)
            log.debug("Dict file not found, will be created")

        for req in self.patterns:
            try:
                self.last_id = self.id_dict[req]
            except Exception as e:
                log.warning(e)
                log.info("New word : '%s' detected, initializing id (anti-spam)" % req)
                try:
                    antispam = self.twitter.search(q=req, since_id=0, lang='fr')
                except Exception as e:
                    log.warning(e)
                    continue
                self.last_id = antispam['search_metadata']['max_id']
                log.info("Ignoring %i tweets and using %i for last_id" % (len(antispam['statuses']),self.last_id))

            log.info("Search : %s since %i" % (req,self.last_id))
            try:
                result = self.twitter.search(q=req, since_id=self.last_id, lang='fr')
            except Exception as e:
                log.warning(e)
                continue
            log.info("Found %i tweets" % len(result['statuses']))
                
            if result['search_metadata']['max_id'] > self.last_id:
                self.id_dict[req] = result['search_metadata']['max_id'] 
               
            for tweet in result['statuses']:
                if tweet['in_reply_to_screen_name'] is not None:
                    log.warning("Incorrect tweet : reply tweet to %s" % tweet['in_reply_to_screen_name'])
                    continue
                if tweet['retweeted'] is True:
                    log.warning("Incorrect tweet : retweeted")
                    continue
                if 'RT' in tweet['text']:
                    log.warning("Incorrect tweet : retweeted")
                    continue
                if tweet['user']['screen_name'] == self.MYNAME:
                    log.warning("Incorrect tweet : my own !")
                    continue
                if req in tweet['user']['screen_name'].lower():
                    log.warning("Detected incorrect tweet : %s" % tweet['text'])
                    continue
               
                reg = re.findall('@(?P<name>\S+)',tweet['text'])
                if any(req in ex.lower() for ex in reg):
                    log.warning("Incorrect tweet : pattern in name %s" % reg)
                    continue

                log.info("%s said : %s" % (tweet['user']['screen_name'],tweet['text']))
                try:
                    self.sendtweet(tweet['user']['screen_name'], self.patterns[req], tweet['id_str'])
                except Exception as e:
                    log.warning(e)
                time.sleep(30+gauss(0,5))
        
        self.saveid(self.id_dict)
        log.info("Bot stopped on %s" % time.ctime())



