from socket import *
import string
import sys
import time
import zmq
import random
import json


def PID(): #gen random PID
    new_ID = ''.join(random.choice(string.ascii_uppercase) for _ in range(3)) 
    return new_ID

pid = PID()
requests = []
stagger = random.randint(1,2)

def randrequest(): #create random GET/SET requests 
    request = {
        'Request': random.choice(['SET','GET']),
        'Key': random.choice('abcd'),
        'Value': random.randint(1,7)
    }
    return request

for i in range(10): #create 10 requests 
    rand = randrequest()
    requests.append({
        'PID': pid,
        'Time': i,
        'Key': rand['Key'],
        'Value': rand['Value'],
        'Request': rand['Request']
    })


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4100")

print("Connecting...")

def SeqConsistency():
    random.shuffle(requests) 
    for i in range(len(requests)): #go thru all requests
        for request in requests: #organize/sort them
            if request['Time'] == i: #basd on time
                req = request
        RepReq = json.dumps(req).encode() #send to server
        socket.send(RepReq)
        conf = socket.recv().decode('utf-8')
        print(conf)
        time.sleep(stagger) #stagger

SeqConsistency()


##helpers