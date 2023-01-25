import threading
import random
import multiprocessing
import time
import signal
import os
# Create a Python script that simulates an energy-producing and consuming home
class Home:
    def __init__(self, production_rate, consumption_rate, trade_policy):
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.trade_policy = trade_policy
        self.surplus = 0
        
    def calculate_surplus(self):
        self.surplus = self.production_rate - self.consumption_rate
        
    def trade_energy(self):
        if self.trade_policy == "always_give":
            # give away surplus energy to other homes
            pass
        elif self.trade_policy == "always_sell":
            # sell surplus energy to the market
            pass
        else:  # self.trade_policy == "sell_if_no_takers"
            # check if other homes want surplus energy
            # if not, sell to the market
            pass


class Market(multiprocessing.Process):
    def __init__(self, initial_price):
        super().__init__()
        self.price = initial_price
        self.temperature = multiprocessing.Value('d', 0.0)
        self.ensoleillement = multiprocessing.Value('i', 0)
        signal.signal(signal.SIGINT, self.HiverVolcanique)
        signal.signal(signal.SIGUSR1, self.GulfWar)
        signal.signal(signal.SIGUSR2, self.Siberia)
        signal.signal(signal.SIGALRM, self.RetourNormal)

    def HiverVolcanique(self, signum, frame):
        print("cheh")
        exit(0)
    
    def GulfWar(self, signum, frame):
        print("Received SIGUSR1. Outputting data to output1.txt...")
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
        t.run()
        while True:
            time.sleep(1)
            pass


class Weather(multiprocessing.Process):
    def __init__(self, temperature):
        super().__init__()
        self.temperature = temperature
        self.temp_change = 2
        self.upDown = -1
        self.duration = 5
        self.ensoleillement = 0.5
        
    def update_temperature(self):
        
        if self.duration>=0:
            self.duration-=1
            self.temperature += self.upDown*int(self.temp_change*random.randrange(0,10)/10)
        else:
            self.upDown=random.choice([-1, 1])
            self.duration = random.randrange(3,7)
            self.temperature += self.upDown*int(self.temp_change*random.randrange(0,10)/10)    
    def update_ensoleillement(self):
        a= random.randrange(-10,10)/100
        if a+self.ensoleillement >=1:
            self.ensoleillement=1
        elif a+self.ensoleillement <=0:
            self.ensoleillement=0   
        else:
            self.ensoleillement+=a     
    def run(self):
        while True:
            self.update_temperature()
            self.update_ensoleillement()
            #print(self.temperature)
            #print(self.ensoleillement)
            time.sleep(1)     

class External(multiprocessing.Process):
        def __init__(self):
            super().__init__() 
        def run(self):
            while True:
                time.sleep(1)
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
    m = Market(10)
    p=Weather(22)
    m.start()
    p.start()
    m.join()
    p.join()
    

