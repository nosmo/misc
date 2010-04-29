#!/usr/bin/env python

# Get timetables for Irish Rail trains based on route locationsx

__author__ = "Hugh Nowlan (nosmo@netsoc.tcd.ie)"

import BeautifulSoup
import datetime
import sys
import urllib2


def main():
    now = datetime.datetime.now()
    hour = now.hour
    day = now.day
    month = now.month
    
    if now.day < 10:
        day = "0%d" % now.day
        
    if now.month < 10:
        month = "0%d" % now.month
        
    url="http://www.irishrail.ie/your_journey/timetables_junction1.asp?txtFromStation=%s&txtToStation=%s&RadioOutDirect=direct&ToStations=NULL&OutSelectDay=%s&OutSelectMonth=%s&RadioOutStatus=D&OutFromTime=%s&OutToTime=24&RadioReserve=1&NumPass=01&cmdSubmit3.x=13&cmdSubmit3.y=19&optionWalk=yes&optionBus=yes&hidOutDate=&hidRtnDate=" % (sys.argv[1], sys.argv[2], day, month, hour)

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()

    soup = BeautifulSoup.BeautifulSoup(the_page)
    dorts = soup.findAll("strong")[7:]

    print "From\t\tTo\tDate\tDep.\tArr."
    
    for i in range(len(dorts)):
        if i%7 == 0:
            print "%s\t%s\t%s\t%s\t%s\t" % (dorts[i].contents[0].rstrip(), dorts[i+1].contents[0].rstrip(),
                                            dorts[i+2].contents[0].rstrip(), dorts[i+3].contents[0].rstrip(),
                                            dorts[i+4].contents[0].rstrip())

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "Usage: train [location] [destination]"
        sys.exit(1)

    main()
