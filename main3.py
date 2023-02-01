import threading
import random
import multiprocessing 
import time
import signal
import os
import sysv_ipc
import socket

PORT = 10003
HOST = 'localhost'


def Home(stock,equilibre,politique,temperature,ensoleillement):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            print('home1-debut de tour:'+str(stock))
            home_socket.connect((HOST, PORT))
            if stock<equilibre:
                if(stock<equilibre):
                    msg = 'InNeed '+str(equilibre-stock)
                    home_socket.sendall(msg.encode())
            else: 
                if(politique=='ASell'):
                    msg = 'ToSell '+str(stock-equilibre)
                    home_socket.sendall(msg.encode())
                    stock=equilibre
                elif(politique=='AGive'):   
                    pass
                elif(politique=='SellOrGive'):
                    pass
            data = home_socket.recv(1024)
            stock+=int(data.decode()) 
            print('home1-fin de tour:'+str(stock))
        stock+=UpdateSurplus(temperature.value,ensoleillement.value)   
        time.sleep(1)    

def Home2(stock,equilibre):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            print('home2-debut de tour:'+str(stock)) 
            home_socket.connect((HOST, PORT))
            if stock>equilibre:
                msg = 'ToSell '+str(stock-equilibre)
                home_socket.sendall(msg.encode())
            else:
                msg = 'InNeed '+str(equilibre-stock)
                home_socket.sendall(msg.encode())    
            data = home_socket.recv(1024)
            stock+=int(data.decode()) 
            print('home2-fin de tour:'+str(stock))  
        time.sleep(1)    

def recevoirEtEchanger(surplus,equilibre,queue):
    a=surplus
    try:
        m,t=queue.receive(block=False)
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
        return surplus
    except sysv_ipc.BusyError:
        return a

def Market(stock):
    e=multiprocessing.Process(target=External)
    e.start()
    signal.signal(signal.SIGINT, HiverVolcanique)
    signal.signal(signal.SIGUSR1, GulfWar)
    signal.signal(signal.SIGUSR2, Siberia)
    signal.signal(signal.SIGALRM, RetourNormal)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as market_socket:
        market_socket.bind((HOST, PORT))
        market_socket.listen(2)
        print('market:'+str(stock))
        while True:
            conn, addr = market_socket.accept()
            stock = handleMsg(conn,addr,stock)
            print('market:'+str(stock))
    e.join()        

def UpdatePrice(ancienStock,nouveauStock,ancienPrix):
    return ancienPrix (nouveauStock-ancienPrix)/10

def UpdateConsumation(temperature):
    if(temperature>15):
        return 3
    else:
        return 3 + int((15-temperature)/3)

def UpdateProduction(ensoleillement):
    return int(ensoleillement*10)

def UpdateSurplus(temperature,ensoleillement):
        surplus= UpdateProduction(ensoleillement)-UpdateConsumation(temperature)
        return surplus

    

def handleMsg(conn,addr,stock):
    data = conn.recv(1024)
    dataStr=data.decode()
    message=dataStr.split(' ')[0]
    quantite=dataStr.split(' ')[1]
    if message=='ToSell':
        conn.sendto('0'.encode(),addr)
        return stock+int(quantite)
    elif message=='InNeed':
        if int(quantite)<=stock:
            conn.sendto(quantite.encode(),addr)
            return stock-int(quantite) 
        else:
            conn.sendto(str(stock).encode(),addr)
            return 0

def Weather(temperature,ensoleillement,temp_change,duration,upDown):
    while True:
        update_temperature(duration,temperature,upDown,temp_change)
        update_ensoleillement(ensoleillement)  
        print(temperature.value)
        print(ensoleillement.value)
        time.sleep(1)  

def update_temperature(duration,temperature,upDown,temp_change):
    if duration.value>=0:
        duration.value-=1
        temperature.value += upDown.value*int(temp_change.value*random.randrange(0,10)/10)
    else:
        upDown.value=random.choice([-1, 1])
        duration.value = random.randrange(3,7)
        temperature.value+= upDown.value*int(temp_change.value*random.randrange(0,10)/10)
def update_ensoleillement(ensoleillement):
    a= random.randrange(-10,10)/100
    if a+ensoleillement.value >=1:
        ensoleillement.value=1
    elif a+ensoleillement.value <=0:
        ensoleillement.value=0   
    else:
        ensoleillement.value+=a     

def HiverVolcanique(s,t):
    print("Hiver Volcanique")
    exit(0)
    
def GulfWar(s,t):
    print("GulfWar")

def Siberia(s,t):
    #temp.duration =20
        #temp.temp_change = 3
        #temp.upDown = -1
        #temp.ensoleillement = 0.01
    print("Siberia")

def RetourNormal(s,t):
    #temp.duration =5
        #temp.temp_change = 2
        #temp.ensoleillement = 0.5
        #temp.temperature = 22
    print("Retour Normal") 

def External():
    r=random.randrange(0,1000)
    if r<1:
        os.kill(os.getppid(), signal.SIGINT)
    elif r<31:
        os.kill(os.getppid(), signal.SIGUSR2)
    elif r<81:
        os.kill(os.getppid(), signal.SIGALRM)
    elif r<91:
        os.kill(os.getppid(), signal.SIGUSR1)
    else:
        pass

if __name__=='__main__':
    temperature = multiprocessing.Value('i', 22)
    ensoleillement = multiprocessing.Value('d', 0.5)
    temp_change = multiprocessing.Value('i', 2)
    duration = multiprocessing.Value('i', 4)
    upDown = multiprocessing.Value('i', -1)
    market = multiprocessing.Process(target=Market, args=(5,))
    market.start()
    queue=sysv_ipc.MessageQueue(130,sysv_ipc.IPC_CREAT)
    home = multiprocessing.Process(target=Home, args=(10,9,'ASell',temperature,ensoleillement))
    home2 = multiprocessing.Process(target=Home2, args=(5,7)) 
    w=multiprocessing.Process(target=Weather, args=(temperature,ensoleillement,temp_change,duration,upDown))
    w.start()
    time.sleep(2)
    home.start()
    home2.start()
    w.join()
    home.join()
    home2.join()
    market.join()

