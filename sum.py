#!/usr/bin/env python

#Dumb summing script. Using as a framework later
# Better done via `awk '{ sum += $1 } END { print sum }'`

from ast import literal_eval
import fileinput
import sys

def parses_to_integer(s):
    val = literal_eval(s)
    return isinstance(val, int) or (isinstance(val, float) and val.is_integer())

def main():

    total = 0

    for line in fileinput.input():
        line = line.strip()
        number = None
        try:
            if parses_to_integer(line):
                number = int(line)
            else:
                number = float(line)
        except Exception as e:
            sys.stderr.write("Couldn't parse number %s")
            continue
        total += number

    print total

if __name__ == "__main__":
    main()
