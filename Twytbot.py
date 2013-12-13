#!/usr/bin/python

import twython
import time
import json

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
        self.id_dict = {}

    def authentificate(self):
        self.twitter = twython.Twython(self.KEY, self.SECRET, self.ACCESS_TOKEN, self.SECRET_TOKEN)
        try:
            self.twitter.verify_credentials()
            #pass
        except:
            log.warning("Twitter login failed")
            raise

    def addpattern(self, search, response):
        self.patterns[search] = response
        log.info("Added pattern : '"+search+" : "+response+"'")

    def sendtweet(self, user, response, message_id):
        text = "@"+user+" "+response
        log.info("Sending '"+text+"'")
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
        log.info("Bot started on "+time.ctime())
        self.authentificate()
        try:
            self.id_dict = self.getid()
        except:
            log.debug("Dict file not found, will be created")

        for req in self.patterns:
            try:
                self.last_id = self.id_dict[req]
            except:
                self.last_id = 0

            log.info("Search : "+req+" since "+str(self.last_id))
            result = self.twitter.search(q=req, since_id=self.last_id, lang='fr')
            log.info("Found "+str(len(result['statuses']))+" tweets")
                
            if result['search_metadata']['max_id'] > self.last_id:
                self.id_dict[req] = result['search_metadata']['max_id'] 
               
            for tweet in result['statuses']:
                if tweet['user']['screen_name'] == self.MYNAME:
                    continue
                log.info(tweet['user']['screen_name']+" said : "+tweet['text'])
                try:
                    self.sendtweet(tweet['user']['screen_name'], self.patterns[req], tweet['id_str'])
                except Exception as e:
                    log.warning(e)
                time.sleep(5)
        
        self.saveid(self.id_dict)
        log.info("Bot stopped on "+time.ctime())



