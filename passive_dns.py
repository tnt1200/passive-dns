#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/2/5 上午9:59
# @Author  : Komi
# @File    : pdns_sniff.py
# @Ver:    : 0.1
# from https://github.com/coffeehb/tools/pdns_sniff

from gevent import monkey
monkey.patch_all()
import gevent
from scapy.all import sr1, IP, UDP, DNS, DNSQR, DNSRR
from scapy.all import sniff
import datetime
import time
import traceback
import argparse
from model import DnsRecord
from mongoengine.errors import NotUniqueError
from dbfunc import save_record


def value_sniper(arg1):
    string_it = str(arg1)
    snap_off = string_it.split('=')
    working_value = snap_off[1]
    return working_value[1:-1]


def packetHandler(a):
    for pkt in a:  # read the packet
        if pkt.haslayer(DNSRR):  # Read in a pcap and parse out the DNSRR Layer
            domain1 = pkt[DNSRR].rrname  # this is the response, it is assumed

            if domain1 != '':  # ignore empty and failures
                domain = domain1[:-1]

                record_log = {}

                # identify the response record that requires parsing
                pkt_type = pkt[DNSRR].type

                # date/time
                time_raw = pkt.time  # convert from unix to 8 digit date
                pkt_date = (datetime.datetime.fromtimestamp(
                    int(time_raw)).strftime('%Y%m%d %H:%M:%S'))
                record_log['record_time'] = str(pkt_date)

                dns_server = pkt[IP].src  # dns_server
                dns_client = pkt[IP].dst  # dns_client

                record_log['dns_client_ip'] = dns_client
                record_log['dns_server_ip'] = dns_server

                # this should work for type 5 and 2
                if pkt_type == 2 or pkt_type == 5:
                    x = pkt[DNSRR].answers
                    dns_strings = str(x)
                    fields = dns_strings.split('|')
                    for each in fields:
                        if 'type=NS' or 'type=A' in each:
                            subeach = str(each)
                            y = subeach.split(' ')  # split lines
                            for subsubeach in y:
                                if 'rdata' in subsubeach:
                                    ipaddress = value_sniper(subsubeach)

                                    if ipaddress != None:
                                        print(
                                            "[+]domain: {} ==>{}[+]2,5".format(str(domain), ipaddress))
                                        record_log['domain_ip'] = ipaddress
                                        record_log['domain'] = domain.decode(
                                            'ascii')
                                        save_record(
                                            domain.decode('ascii'), ipaddress)
                # 32bit IP addresses
                elif pkt_type == 1 or pkt_type == 12 or pkt_type == 28:
                    ipaddress = pkt[DNSRR].rdata
                    print(
                        "[+]domain: {} ==>{}[+]1,12,28".format(str(domain), ipaddress))

                    record_log['domain_ip'] = ipaddress
                    record_log['domain'] = domain.decode('ascii')
                    save_record(domain.decode('ascii'), ipaddress)
                else:
                    print("[+]domain: {}  ==>  NULL[+]".format(str(domain)))
                    record_log['domain_ip'] = "NULL"
                    record_log['domain'] = str(domain)


def run(interface='en0'):
    print("[+] Start Recording......")
    sniff(iface=interface, filter="udp and port 53", prn=packetHandler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='passive dns sniffer', usage='python3 %(prog)s [options]', prog='passive_dns.py')
    parser.add_argument('-i', help='interface default:en0', default='en0')
    args = parser.parse_args()
    try:
        gevent.joinall([gevent.spawn(run, args.i)])
    except Exception as e:
        traceback.print_exc()
