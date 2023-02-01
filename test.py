import threading
import random
import multiprocessing 
import time
import signal
import os
import sysv_ipc
import socket






def Home(surplus,equilibre,queue):
    pid=os.getpid()
    mess=str(surplus)+","+str(pid)+",Besoin?"
    message=(mess).encode()
    queue.send(message)
    time.sleep(1)
    m,t=queue.receive(type=pid)
    value=m.decode().split(",")
    value=int(value[0])
    surplus-=value
    print(pid,surplus)

    
def Home2(surplus,equilibre,queue):
    while True:
        if (surplus<equilibre):
            recevoirEtEchanger(surplus,equilibre,queue)
            break

    
    
def recevoirEtEchanger(surplus,equilibre,queue):
    m,t=queue.receive()
    value=m.decode().split(",")
    print(value)
    intermediaire=int(value[0])
    pidSender=int(value[1])
    if(intermediaire<equilibre-surplus):
        surplus+=intermediaire 
    else :
        intermediaire=equilibre-surplus
        surplus=equilibre
    print(os.getpid(),surplus)
    mess=str(intermediaire)+","+str(os.getpid())+",Je suis Home2"
    message=mess.encode()
    queue.send(message,type=pidSender) 
    print(pidSender)
    


if __name__=="__main__":
    queue=sysv_ipc.MessageQueue(129,sysv_ipc.IPC_CREAT)
    h1=multiprocessing.Process(target=Home,args=(3,0,queue))
    h2=multiprocessing.Process(target=Home2,args=(7,8,queue))
    h1.start()
    h2.start()
    h2.join()
    h1.join()
