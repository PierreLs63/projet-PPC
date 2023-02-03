import threading
import random
import multiprocessing 
import time
import signal
import os
import sysv_ipc
import socket

PORT = 2000
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

def Home2(stock,equilibre,politique,temperature,ensoleillement):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            print('home2-debut de tour:'+str(stock))
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
            print('home2-fin de tour:'+str(stock))
        stock+=UpdateSurplus(temperature.value,ensoleillement.value)   
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

def Market(stock,temperature,ensoleillement):
    e=multiprocessing.Process(target=External)
    e.start()
    lock=multiprocessing.Lock()
    prix=100
    signal.signal(signal.SIGINT, handleSig)
    signal.signal(signal.SIGUSR1, handleSig)
    signal.signal(signal.SIGUSR2, handleSig)
    signal.signal(signal.SIGALRM, handleSig)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as market_socket:
        market_socket.bind((HOST, PORT))
        market_socket.listen(2)
        while True:   
            conn, addr = market_socket.accept()
            stock = handleMsg(conn,addr,stock)
            prix = UpdatePrice(prix,temperature.value,ensoleillement.value,lock)
            print('prix:'+str(prix))
            print('market:'+str(stock))
    e.join()        

def handleSig(a,f):
    if (a==2):
        HiverVolcanique ()
    elif (a==30):
        GulfWar()
    elif (a==14):
        Siberia ()
    elif (a==31):
        RetourNormal ()
        




def UpdatePrice(prix,temperature,ensoleillement,lock):
    lock.acquire()
    prix=0.99*prix + (temperature-10)/(1+5*ensoleillement)
    if(prix<0):
        prix=0
    lock.release()
    return prix

def UpdateConsumation(temperature):
    if(temperature>15):
        return 2
    else:
        return 2 + int((15-temperature)/4)

def UpdateProduction(ensoleillement):
    return int(ensoleillement*10)

def UpdateSurplus(temperature,ensoleillement):
        surplus= UpdateProduction(ensoleillement)-UpdateConsumation(temperature)
        return surplus

    

def handleMsg(conn,addr,stock):
    print("message")
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
        print('temperature:'+str(temperature.value))
        print('ensoleillement'+str(ensoleillement.value))
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

def HiverVolcanique():
    print("------------------------------------Hiver Volcanique")
    exit(0)
    
def GulfWar():
    print("------------------------------------GulfWar")

def Siberia():
    #temp.duration =20
        #temp.temp_change = 3
        #temp.upDown = -1
        #temp.ensoleillement = 0.01
    print("------------------------------------Siberia")

def RetourNormal():
    #temp.duration =5
        #temp.temp_change = 2
        #temp.ensoleillement = 0.5
        #temp.temperature = 22
    print("------------------------------------Retour Normal") 

def External():
    while True:
        r=random.randrange(0,1000)
        if r<1:
            os.kill(os.getppid(), signal.SIGINT)
        elif r<31:
            os.kill(os.getppid(), signal.SIGUSR2)
        elif r<81:
            os.kill(os.getppid(), signal.SIGALRM)
        elif r<901:
            os.kill(os.getppid(), signal.SIGUSR1)
        else:
            pass
        time.sleep(1)

if __name__=='__main__':
    temperature = multiprocessing.Value('i', 17)
    ensoleillement = multiprocessing.Value('d', 0.5)
    temp_change = multiprocessing.Value('i', 2)
    duration = multiprocessing.Value('i', 4)
    upDown = multiprocessing.Value('i', -1)
    market = multiprocessing.Process(target=Market, args=(5,temperature,ensoleillement))
    market.start()
    #queue=sysv_ipc.MessageQueue(130,sysv_ipc.IPC_CREAT)
    home = multiprocessing.Process(target=Home, args=(100,9,'ASell',temperature,ensoleillement))
    home2 = multiprocessing.Process(target=Home2, args=(0,7,'ASell',temperature,ensoleillement)) 
    w=multiprocessing.Process(target=Weather, args=(temperature,ensoleillement,temp_change,duration,upDown))
    w.start()
    time.sleep(2)
    home.start()
    home2.start()
    w.join()
    home.join()
    home2.join()
    market.join()

