#!/usr/bin/env python

import sys, twitter, os, random
from datetime import date, datetime, time, timedelta
import serial

class Hackbot(object):

    def __init__(self):
        self.LATESTFILE = 'newyearlastest.txt'
        self.LOGFILE = 'newyearlog.txt'
        # Add your twitter dev keys here
        # Use this tutorial if you need help https://facelesstech.wordpress.com/2014/01/01/tweeting-from-python/
        self.api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

    def time_maths(self, now):
        self.now = now
        newyear = datetime(2015,01,01,00,00) # This is the countdown to date and time
        # This is the maths to work out how long till the countdown
        self.take = newyear - self.now

        start = self.now
        finish = newyear
        math = finish - start
        final = ':'.join(str(math).split(':')[:2])
        first = int(math.seconds) / 60
        self.hour = first / 60
        extra = self.hour * 60
        self.final = first - extra
        seconds = extra * 60
        takeseconds  = math.seconds - seconds
        self.finalseconds = self.final * 60
        self.finalseconds = takeseconds - self.finalseconds
        return;

    def thebot(self, results,lastid):
        # This is where the magic happens and what handles the tweeting side of the bot
        self.results = results
        self.lastid = lastid
        repliedTo = []
        for statusObj in results:
      
            left_newyear = "%r hours %r minutes %r seconds till newyear" % (self.hour, self.final, self.finalseconds)
            print left_newyear

            print 'Posting in reply to @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            self.api.PostUpdate('@%s %r' % (statusObj.user.screen_name, left_newyear), in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('ascii', 'replace')))
           
            # Writes the last checked position to file
            print 'writing lastestfile'            
            fp = open(self.LATESTFILE, 'w')
            fp.write(str(max([x.id for x in results])))
            fp.close()
            
            # Keeps a log of whos been using the bot and writes it to file
            print 'writing logfile'
            fp = open(self.LOGFILE, 'a')
            fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
            fp.write('\n')
            fp.close()

if __name__ == '__main__':
    begin = Hackbot()
    fp = open(begin.LATESTFILE)
    lastid = fp.read().strip()
    fp.close()
    
    # These are the hashtages its searching for on twitter
    search = '#newyear_uk'
    search1 = '#newyear_east'
    search2 = '#newyear_central'
    search3 = '#newyear_mountain'
    search4 = '#newyear_west'

    # This is where it searches twitter then passes it off to be twitter if its finds a match
    results = begin.api.GetSearch(search, since_id=lastid)
    print "Searching twitter for %r" % search 
    results1 = begin.api.GetSearch(search1, since_id=lastid)
    print "Searching twitter for %r" % search1 
    results2 = begin.api.GetSearch(search2, since_id=lastid)
    print "Searching twitter for %r" % search2
    results3 = begin.api.GetSearch(search3, since_id=lastid)
    print "Searching twitter for %r" % search3
    results4 = begin.api.GetSearch(search4, since_id=lastid)
    print "Searching twitter for %r" % search4

    if (len(results) > 0):
        print 'Found %s results.' % (len(results))
        begin.time_maths(datetime.now())
        begin.thebot(results, lastid)
           
    elif (len(results1) > 0):
        print 'Found %s results.' % (len(results1))
        us1time = datetime.now() - timedelta(hours=5)
        begin.time_maths(us1time)
        begin.thebot(results1, lastid)

    elif (len(results2) > 0):
        print 'Found %s results.' % (len(results2))
        us2time = datetime.now() - timedelta(hours=6)
        begin.time_maths(us2time)
        begin.thebot(results2, lastid)

    elif (len(results3) > 0):
        print 'Found %s results.' % (len(results3))
        us3time = datetime.now() - timedelta(hours=7)
        begin.time_maths(us3time)
        begin.thebot(results3, lastid)

    elif (len(results4) > 0):
        print 'Found %s results.' % (len(results4))
        us4time = datetime.now() - timedelta(hours=8)
        begin.time_maths(us4time)
        begin.thebot(results4, lastid)

