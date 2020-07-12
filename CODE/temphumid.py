import time
from machine import Pin
from dht import DHT

th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(2)

def read_data():
    result = th.read()
    while not result.is_valid():
        time.sleep(.5)
        result = th.read()
    return(result.temperature - 5,result.humidity - 45)
