#!/usr/bin/env python

from __future__ import print_function

import os,json,datetime,argparse
from urllib2 import urlopen

parser = argparse.ArgumentParser(description="Get your public IP")
parser.add_argument("-l","--log",help="folder for log IP changes")
parser.add_argument("-u","--upload",help="upload file to Dropbox",action='store_true')
args = parser.parse_args()


fnom='pubip.txt'
fhis='pubip.log'
email = 'sersope@gmail.com'
password = '#######'


urls=[ ['http://www.telize.com/jsonip','ip'],
       ['http://httpbin.org/ip','origin'],
       ['http://jsonip.com','ip'] ]

#Get log folder from command line
df=os.getcwd()
if args.log!=None :
    df=args.log
    try:
        os.chdir(df)
    except:
        print('Error:',df,"don't exist.")
        exit()

##TODO obtener la current ip de la ultima linea del fichero log
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
    print('Error: can't get your IP.')
    exit()

if args.log==None and args.upload==False:
    print('Your public IP is',nip)
    
#Salva la IP solo si es nueva
if args.log!=None:
    if nip!=cip :
        f=open(fnom,'w')
        f.write(nip)
        f.close()
        #Actualiza el historico
        f=open(fhis,'a')
        f.write(str(datetime.datetime.now())+' IP:'+nip+'\n')
        f.close()
        #Sube a Dropbox
        if args.upload==True:
            try:
                from dbupload import DropboxConnection
		conn = DropboxConnection(email, password).upload_file(fnom,"/",fnom)
            except:
                print("Error: Dropbox upload failed")




