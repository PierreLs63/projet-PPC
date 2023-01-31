import threading
import random
import multiprocessing 
import time
import signal
import os
import sysv_ipc
import socket

PORT = 6667
HOST = 'localhost'


def Home(stock,equilibre,politique):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            print("hello1\n")
            home_socket.connect((HOST, PORT))
            print("hello2\n")
            if stock<equilibre:
                msg = 'InNeed '+str(equilibre-stock)
                home_socket.sendall(msg.encode())
            else: 
                if(politique=='ASell'):
                    msg = 'ToSell '+str(stock-equilibre)
                    home_socket.sendall(msg.encode())
                    stock=equilibre
                elif(politique=='AGive'):
                        #massageQueue
                        pass
                elif(politique=='SellOrGive'):
                    if(True):
                        pass
                    else:
                        msg = 'ToSell '+str(stock-equilibre)
                        home_socket.sendall(msg.encode())
                        stock=equilibre
            data = home_socket.recv(1024)
            stock+=int(data.decode()) 
            print('home1:'+str(stock))
        #stock+=UpdateSurplus(temperature.value,ensoleillement.value)   
        time.sleep(1)    

def Home2(stock,equilibre):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            home_socket.connect((HOST, PORT))
            if stock>equilibre:
                msg = 'ToSell '+str(stock-equilibre)
                home_socket.sendall(msg.encode())
            else:
                msg = 'InNeed '+str(equilibre-stock)
                home_socket.sendall(msg.encode())    
            data = home_socket.recv(1024)
            stock+=int(data.decode()) 
            print('home2:'+str(stock))  
        time.sleep(1)    

def Market(stock):
    e=multiprocessing.Process(target=External)
    e.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as market_socket:
        market_socket.bind((HOST, PORT))
        market_socket.listen(2)
        print('market:'+str(stock))
        while True:
            print("conn\n")
            conn, addr = market_socket.accept()
            stock = handleMsg(conn,addr,stock)
            print('market:'+str(stock))
    e.join()        

def UpdatePrice(actualPrice):
    pass

def UpdateConsumation(temperature):
    if(temperature.value>15):
        return 6
    else:
        return 6 + int((15-temperature.value)/3)

def UpdateProduction(ensoleillement):
    return int(ensoleillement.value*10)

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


def External():
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

if __name__=='__main__':
    temperature = multiprocessing.Value('i', 22)
    ensoleillement = multiprocessing.Value('d', 0.5)
    temp_change = multiprocessing.Value('i', 2)
    duration = multiprocessing.Value('i', 4)
    upDown = multiprocessing.Value('i', -1)
    home = multiprocessing.Process(target=Home, args=(10,9,'ASell'))
    #home2 = multiprocessing.Process(target=Home2, args=(5,7))
    market = multiprocessing.Process(target=Market, args=(5,))
    market.start()
    time.sleep(2)
    home.start()
    #home2.start()
    w=multiprocessing.Process(target=Weather, args=(temperature,ensoleillement,temp_change,duration,upDown))
    w.start()
    w.join()
    home.join()
    #home2.join()
    market.join()

