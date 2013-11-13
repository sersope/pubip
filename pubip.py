#!/usr/bin/env python3
#  pubip.py
#  
#  Obtener la IP pública de tu conexión a Internet
#  
#  Copyright 2013 Sergio Soriano Peiró <sersope@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#~ from __future__ import print_function #python2

import os,json,datetime,argparse
from urllib.request import urlopen
#~ from urllib2 import urlopen #python2

parser = argparse.ArgumentParser(description="Get your public IP")
parser.add_argument("-l","--log",help="file for log IP changes")
#~ parser.add_argument("-u","--upload",help="upload file to Dropbox",action='store_true')
args = parser.parse_args()

email = 'sersope@gmail.com'
password = '#######'


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

if args.log==None: #and args.upload==False:
    print('Your public IP is',nip)

#Registra la IP en el log sólo si es nueva
if args.log!=None and nip!=cip :
    try:
        hoy=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f=open(args.log,'a')
        f.write(hoy + ' IP:' + nip + '\n')
        f.close()
        #Sube a Dropbox TODO
        #~ if args.upload==True:
            #~ try:
                #~ from dbupload import DropboxConnection
                #~ conn = DropboxConnection(email, password).upload_file(fnom,"/",fnom)
            #~ except:
                #~ print("Error: Dropbox upload failed")
    except:
        print("Error: Can't save to",args.log)
