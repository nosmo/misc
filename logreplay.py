#!/usr/bin/env python
import re
import fileinput
import datetime
import time
import logging

# Replay an apache log file in "real" time

DATE_RE = re.compile("\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}")
DATE_STR = "%d/%b/%Y:%H:%M:%S"

class LogReplayer(object):

    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.last_time = None

    @staticmethod
    def __parsedate(datestring):
        datematch = DATE_RE.search(datestring)
        if not datematch:
            return None
        else:
            return datetime.datetime.strptime(datematch.group(),
                                              DATE_STR)

    @staticmethod
    def timeshift_line(line, newdate):
        linesplit = DATE_RE.split(line)
        if not linesplit or len(linesplit) < 2:
            logging.error("Line %s didn't split correctly, skipping")
        linesplit.insert(1, newdate.strftime(DATE_STR))
        return "".join(linesplit)

    def replay(self, faketoday=True):
        #faketoday makes the log replay all dates,
        #  shifted to the current time (onwards)

        outfile = open(self.outputfile, "w")
        time_shift = datetime.timedelta(0)
        linecount = 0
        for line in fileinput.input(self.inputfile):
            datenow = self.__parsedate(line) + time_shift
            if not self.last_time:
                if faketoday:
                    time_shift = datetime.datetime.now() - datenow
                    datenow = datenow + time_shift
                self.last_time = datenow
                if faketoday:
                    line = self.timeshift_line(line, datenow)
                outfile.write(line)
            else:
                timediff = datenow - self.last_time
                logging.info( "Sleeping %f seconds at %s" % timediff.total_seconds(),
                              datenow)

                time.sleep(timediff.total_seconds())
                if faketoday:
                    line = self.timeshift_line(line, datenow)
                outfile.write(line)
                self.last_time = datenow
                linecount += 1

                if linecount % 1000 == 0:
                    print "Wrote %d lines, last wrote %s" % (linecount, line)

def main():

    l = LogReplayer("dl_web_access.log", "dl_access.log")
    l.replay()

if __name__ == "__main__":
    main()
