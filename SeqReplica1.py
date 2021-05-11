import redis
import logging
import zmq
import time



context = zmq.Context()
#SOCKET TO TALK TO SERVER
print("Connecting...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4000")

client = redis.Redis(host='localhost',port=6380)
print("ready1")
client.slaveof(host='localhost', port=6379) #this is the replica
print("ready2")
socket.send(b"connecting")

logging.basicConfig(filename="SequentialReplica.log",level=logging.DEBUG) #logging output

while True:
    request = socket.recv_json()
    print(request)
    result = client.get(request['Key'])
    if result == None:
        logging.info('PID:%s, Time:%s GET %s: %s' % (request['PID'], request['Time'], request['Key'],result))
    else:
        logging.info('PID:%s, Time:%s GET %s: %s' % (request['PID'], request['Time'], request['Key'],result.decode('utf-8')))
    socket.send(b"got em")