#!/usr/bin/env python
import re
import fileinput
import datetime
import time
import logging

# Replay an apache log file in "real" time

DATE_RE = re.compile("\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}")

class LogReplayer(object):

    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.last_time = None

        #self.last_time = self.__parsedate(self.line)

    @staticmethod
    def __parsedate(datestring):
        datematch = DATE_RE.search(datestring)
        if not datematch:
            return None
        else:
            return datetime.datetime.strptime(datematch.group(),
                                              "%d/%b/%Y:%H:%M:%S")

    def replay(self):
        outfile = open(self.outputfile, "w")
        for line in fileinput.input(self.inputfile):
            datenow = self.__parsedate(line)
            if not self.last_time:
                self.last_time = datenow
                outfile.write(line)
            else:
                timediff = datenow - self.last_time
                print "Sleeping %f seconds at %s" % (timediff.total_seconds(),
                                                     datenow)
                time.sleep(timediff.total_seconds())
                outfile.write(line)
                self.last_time = datenow

def main():

    l = LogReplayer("dl_web_access.log", "access_log")
    l.replay()

if __name__ == "__main__":
    main()
