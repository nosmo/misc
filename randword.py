#!/usr/bin/env python

import random
import sys

runtimes = 1

if len(sys.argv) > 1:
    try:
        runtimes = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("Failed to parse argument %s", sys.argv[1])

for i in range(runtimes):
    with open("/usr/share/dict/words") as wordsfile:
        wordlist = wordsfile.read().split("\n")
        print wordlist[int(random.random() * len(wordlist))]

