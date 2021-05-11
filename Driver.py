import subprocess
import time
import os
import random

process1 = subprocess.Popen('python Server.py')
time.sleep(1)     
process2 = subprocess.Popen('python SeqReplica1.py')
#process3 = subprocess.Popen('python Client.py')
#process4 = subprocess.Popen('python Client.py')
#process4 = subprocess.Popen('python Client.py')
