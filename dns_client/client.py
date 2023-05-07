from socket import *
from dnslib import *
import argparse
import sys


PORT = 53
HOST = '127.0.0.1'

parser = argparse.ArgumentParser()
parser.add_argument("domain")
parser.add_argument("record_type")
args =parser.parse_args()




with socket.socket(socket.AF_INET, SOCK_DGRAM) as client:
    client.connect((HOST, PORT))

    req = 0
    match args.record_type:
        case "AAAA":
            req = DNSRecord(q=DNSQuestion(args.domain, QTYPE.AAAA))
        case "NS":
            req = DNSRecord(q=DNSQuestion(args.domain, QTYPE.NS))
        case _:
            req = DNSRecord(q=DNSQuestion(args.domain, QTYPE.A))

    client.send(req.pack())
    m, a = client.recvfrom(1024)
    print(DNSRecord.parse(m))
    client.close()




