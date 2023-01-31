import threading
import random
import multiprocessing
import time
import signal
import os
import sysv_ipc
import socket
class DataEchange():
    def __init__(self, pid, quantite,message):
        self.pid=pid
        self.quantite =quantite 
        self.message=message
# Create a Python script that simulates an energy-producing and consuming home
class Home(multiprocessing.Process):
    def __init__(self, production_rate, consumption_rate, trade_policy,socket_number, queue):
        super().__init__()
        self.a=production_rate
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.trade_policy = trade_policy
        self.achat=0
        self.surplus = 0
        self.socket_number=socket_number
        self.queue=queue
        self.a = 1
        self.b = 2
        self.c = 3
        
    def calculate_surplus(self):
        self.surplus = self.production_rate - self.consumption_rate
        
    def trade_energy(self):
        pass
    def run(self):
        time.sleep(1)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 10000))
        data = f"{self.a} {self.b} {self.c}"
        client.sendall(data.encode())
        print(f"Sent: {data}")
        client.close()    
         


class Market(multiprocessing.Process):
    def __init__(self, initial_price, temperature,ensoleillement,temp_change,duration,upDown):
        super().__init__()
        self.temperature = temperature
        self.temp_change = temp_change
        self.upDown = upDown
        self.duration = duration
        self.ensoleillement = ensoleillement
        self.price = initial_price
        self.transactions_lock =  multiprocessing.Lock()
        signal.signal(signal.SIGINT, self.HiverVolcanique)
        signal.signal(signal.SIGUSR1, self.GulfWar)
        signal.signal(signal.SIGUSR2, self.Siberia)
        signal.signal(signal.SIGALRM, self.RetourNormal)

    def HiverVolcanique(self, signum, frame):
        print("Hiver Volcanique")
        exit(0)
    
    def GulfWar(self, signum, frame):
        print("Received SIGUSR1. Outputting data to output1.txt...")
        self.update_price(50)
        #print(self.price)
        with open('output1.txt', 'w') as f:
            f.write('Data outputted by SIGUSR1')

    def Siberia(self, signum, frame):
        #temp.duration =20
            #temp.temp_change = 3
            #temp.upDown = -1
            #temp.ensoleillement = 0.01
        print("Received SIGUSR2. Outputting data to output2.txt...")

    def RetourNormal(self, signum, frame):
        #temp.duration =5
            #temp.temp_change = 2
            #temp.ensoleillement = 0.5
            #temp.temperature = 22
        print("Received SIGUSR2. Outputting data to output2.txt...")        

    def update_price(self, transaction_amount):
        # acquire lock to prevent multiple transactions from happening simultaneously
        self.transactions_lock.acquire()
        self.price += transaction_amount
        self.transactions_lock.release()
        
    def run(self):
        print('salut')
        t=External()
        threadh1=threading.Thread(target=self.communicate_with_h1)
        threadh2=threading.Thread(target=self.communicate_with_h2)
        threadh3=threading.Thread(target=self.communicate_with_h3)
        threadh1.start()
        threadh2.start()
        threadh3.start()
        threadh1.join()
        threadh2.join()
        threadh3.join()
        while True:
            t.run()
        
    
    def communicate_with_h1(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 10000))
        server.listen()
        client, address = server.accept()
        print(f"Connected to {address}")
        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            a, b, c = map(int, data.split())
            print(f"Received: {a=} {b=} {c=}")    
        client.close()    
    def communicate_with_h2(self):
        print('test')
        pass
    def communicate_with_h3(self):
        print('test')
        pass

class Weather(multiprocessing.Process):
    def __init__(self, temperature,ensoleillement,temp_change,duration,upDown):
        super().__init__()
        self.temperature = temperature
        self.temp_change = temp_change
        self.upDown = upDown
        self.duration = duration
        self.ensoleillement = ensoleillement
    def update_temperature(self):
        if self.duration.value>=0:
            self.duration.value-=1
            self.temperature.value += self.upDown.value*int(self.temp_change.value*random.randrange(0,10)/10)
        else:
            self.upDown.value=random.choice([-1, 1])
            self.duration.value = random.randrange(3,7)
            self.temperature.value+= self.upDown.value*int(self.temp_change.value*random.randrange(0,10)/10)
    def update_ensoleillement(self):
        a= random.randrange(-10,10)/100
        if a+self.ensoleillement.value >=1:
            self.ensoleillement.value=1
        elif a+self.ensoleillement.value <=0:
            self.ensoleillement.value=0   
        else:
            self.ensoleillement.value+=a     
    def run(self):
        while True:
            self.update_temperature()
            self.update_ensoleillement()  
            #print(self.temperature.value)
            #print(self.ensoleillement.value)
            time.sleep(1)     

class External(multiprocessing.Process):
        def __init__(self):
            super().__init__() 
        def run(self):
            time.sleep(1)
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
    queue = sysv_ipc.MessageQueue
    time.sleep(1)
    m = Market(10,temperature,ensoleillement,temp_change,duration,upDown)
    p=Weather(temperature,ensoleillement,temp_change,duration,upDown)
    h1=Home(10,8,"always give",10000,queue)
    h1.start()
    m.start()
    p.start()
    m.join()
    p.join()
    h1.join()
    

