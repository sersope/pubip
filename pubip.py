#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pubip.py
#
#  Obtener la IP pública de tu conexión a Internet
#

from __future__ import print_function

import os,json,datetime,argparse
from urllib2 import urlopen

parser = argparse.ArgumentParser(description="Get your public IP")
parser.add_argument("-l","--log",help="file for log IP changes")
args = parser.parse_args()

urls=[ ['http://www.telize.com/jsonip','ip'],
       ['http://httpbin.org/ip','origin'],
       ['http://jsonip.com','ip'] ]

#Obteber ultima IP registrada
if args.log!=None:
    try:
        f=open(args.log)
        last=f.readlines()[-1:][0]
        cip=last.split("IP:")[1].rstrip("\n")
        f.close()
    except:
        cip='0.0.0.0'

#Averigua la nueva ip
for url in urls:
    try:
        r=urlopen(url[0]).read().decode()
        nip=json.loads(r)[url[1]]
    except:
        nip=None
        continue
    else:
        break
if nip==None:
    print("Error: can't get your IP.")
    exit()

if args.log==None:
    print('Your public IP is',nip)

#Registra la IP en el log sólo si es nueva
if args.log!=None and nip!=cip :
    try:
        hoy=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f=open(args.log,'a')
        f.write(hoy + ' IP:' + nip + '\n')
        f.close()
    except:
        print("Error: Can't save to",args.log)
