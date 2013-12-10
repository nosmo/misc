#!/usr/bin/env python3

import argparse
import os
import random
import re

ip_regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

def randomiseIPDumb(ipaddress, rand_octets=2):
    octets = ipaddress.split(".")
    for i in range(rand_octets):
        octets[-(i+1)] = str(int(random.random() * 255))
    output_ipaddress = ".".join(octets)
    return output_ipaddress

def cleanLog(inlog, outlog):

    ip_map = {}
    lines_out = []

    with open(inlog, "r") as log_file:
        for line in log_file.read().strip().split("\n"):
            line = line.strip()
            line_ip = None
            rest_of_line = line
            if ip_regex.match(line):
                line_ip, _, rest_of_line = line.partition(" ")
                line_ip = line_ip.strip()
                if line_ip not in ip_map:
                    new_ip = randomiseIPDumb(line_ip)
                    ip_map[line_ip] = new_ip

            lines_out.append((line_ip, rest_of_line))


    with open(outlog, "w") as out_file:
        for old_ip, line in lines_out:
            if not old_ip:
                out_file.write(line + "\n")
            else:
                out_file.write(ip_map[old_ip] + " " + line + "\n")
    return True

def main(input_log, output_log):

    if os.path.isfile(output_log):
        sys.stderr.write("Not overwriting %s" % output_log)
        raise SystemExit

    cleanLog(input_log, output_log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Randomise leading IP addresses in a logfile.')
    parser.add_argument('input_log', metavar='I', type=str,
                        help='The log file to be anonymized')
    parser.add_argument('output_log', metavar='O', type=str,
                        help='The file to be written out')
    args = parser.parse_args()
    main(args.input_log, args.output_log)
