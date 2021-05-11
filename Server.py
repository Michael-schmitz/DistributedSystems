import redis
import logging
import zmq
import time
import json


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:4100")

RepSocket = context.socket(zmq.REP)
RepSocket.bind("tcp://*:4000")
client = redis.Redis(host='localhost',port=6379)

clients = {}
broadcast = RepSocket.recv().decode('utf-8')
print(broadcast)

print("connecting...")
logging.basicConfig(filename="outputSeqMain.log",level=logging.DEBUG) #logging output

while True:
    arr = socket.recv_json()
    print(arr) #show the request command
    if arr['PID'] in clients: #add the new client operations to the dictionary if they aren't already there
        clients[arr['PID']] += 1
    else:
        clients[arr['PID']] = 0

    if arr['Request'] == 'SET': #set request
        setfin = client.get(arr['Key']) 
        client.set(arr['Key'], arr['Value']) #set the key value pair
        logging.info('PID:%s, Time:%s SET %s: %s' % (arr['PID'], arr['Time'], arr['Key'], setfin))    
    elif arr['Request'] == 'GET': #GET request means send to replica
        msg = json.dumps(arr).encode()
        RepSocket.send(msg)
        message = RepSocket.recv().decode('utf-8')
        print(message)
        fin = client.get(arr['Key'])
        if fin == None:
            logging.info('PID:%s, Time:%s GET %s: %s' % (arr['PID'], arr['Time'], arr['Key'], fin))
        else:
            logging.info('PID:%s, Time:%s GET %s: %s' % (arr['PID'], arr['Time'], arr['Key'], fin.decode('utf-8')))
    print("running....")
    socket.send(("SET/GET Done %d" % clients[arr['PID']]).encode())
    time.sleep(1)

    #check if the incoming input is in some sord of order for processes
    #if replica 1 is to send 4,5,6 make sure its in that order. 
    # can interweve replica 2's, use timestamps