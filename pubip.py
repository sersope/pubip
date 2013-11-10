#!/usr/bin/env python

from __future__ import print_function

from dbupload import DropboxConnection
from getpass import getpass

import sys,os,json,datetime
from urllib2 import urlopen


fnom='pubip.txt'
fhis='pubip.his'
email = 'sersope@gmail.com'
password = '#######'


urls=[ ['http://www.telize.com/jsonip','ip'],
       ['http://httpbin.org/ip','origin'],
       ['http://jsonip.com','ip'] ]

#Get destination folder from command line
df=os.getcwd()
if len(sys.argv) > 1 :
    df=sys.argv[1]

#Set working folder
try:
    os.chdir(df)
except:
    print('Error:',df,"no existe.")
    exit()

#Comprueba si existe fichero
try:
    f=open(fnom)
    cip=f.read()
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
    print('Error: No se pudo obtener la IP.')
    exit()
    
#Salva la IP solo si es nueva
if nip!=cip :
    f=open(fnom,'w')
    f.write(nip)
    f.close()
    #Actualiza el historico
    f=open(fhis,'a')
    f.write(str(datetime.datetime.now())+' IP: '+nip+'\n')
    f.close()
    #Sube a Dropbox
    try:
        conn = DropboxConnection(email, password).upload_file(fnom,"/",fnom)
    except:
        print("Error: Dropbox upload failed")




