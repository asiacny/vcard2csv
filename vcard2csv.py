#!/usr/bin/env python

import argparse
import csv
import sys

import vobject


def repair_vcard(s):
    return s.replace('\r\nBEGIN:VCARD','BEGIN:VCARD') + 'END:VCARD\r\n'

def read_vcards(filename):
    text = open(filename).read()
    rawcards0 = text.split('END:VCARD')[:-1]
    rawcards1 = map(lambda c: c.replace('\r\nBEGIN:VCARD','BEGIN:VCARD'), rawcards0)
    rawcards2 = map(lambda c: c + 'END:VCARD\r\n', rawcards1)
    return map(vobject.readOne, rawcards2)

def get_name(vc):
    if 'n' in vc.contents:
        return (vc.n.value.given, vc.n.value.family)
    names = vc.fn.value.split()
    return (' '.join(names[:-1]), names[-1])

def get_street(vc):
    return (vc.adr.value.street.replace('\n',' '), '')

def get_email(vc):
    if 'email' in vc.contents: return vc.email.value
    return ''

def write_vcard(writer, vc):
    if 'adr' not in vc.contents: return
    first, last = get_name(vc)
    str1, str2 = get_street(vc)
    writer.writerow([first, last, str1, str2, vc.adr.value.city,
                     vc.adr.value.region, vc.adr.value.code, vc.adr.value.country,
                     get_email(vc)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='convert vCard contacts to CSV import format')
    parser.add_argument('srcfile', help='vCard input file')
    args = parser.parse_args()

    writer = csv.writer(sys.stdout)
    writer.writerow(['First Name', 'Last Name', 'Home Street', 'Home Street 2',
                     'Home City', 'Home State', 'Home Postal Code', 'Home Country',
                     'E-mail Address'])
    for vc in read_vcards(args.srcfile):
        write_vcard(writer, vc)
        
    
        
