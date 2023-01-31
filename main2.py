import threading
import random
from multiprocessing import Process
import time
import signal
import os
import sysv_ipc
import socket

PORT = 6666
HOST = 'localhost'


def Home(stock,equilibre):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as home_socket:
            home_socket.connect((HOST, PORT))
            if stock>equilibre:
                msg = 'ToSell '+str(stock-equilibre)
                home_socket.sendall(msg.encode())
                stock=equilibre
            else:
                msg = 'InNeed '+str(equilibre-stock)
                home_socket.sendall(msg.encode())     
            data = home_socket.recv(1024)
            stock+=int(data.decode()) 
            print('home1:'+str(stock))
        stock+=1    
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
        stock-=1    
        time.sleep(1)    

def Market(stock):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as market_socket:
        market_socket.bind((HOST, PORT))
        market_socket.listen(2)
        print('market:'+str(stock))
        while True:
            conn, addr = market_socket.accept()
            stock = handleMsg(conn,addr,stock)
            print('market:'+str(stock))

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

if __name__=='__main__':
    home = Process(target=Home, args=(10,9))
    home2 = Process(target=Home2, args=(5,7))
    market = Process(target=Market, args=(5,))
    market.start()
    time.sleep(1)
    home.start()
    home2.start()
    home.join()
    home2.join()
    market.join()

