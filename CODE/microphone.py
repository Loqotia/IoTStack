import time
import machine
from machine import Pin, ADC

adc = ADC()
mic = adc.channel(pin='P13', attn = ADC.ATTN_11DB)
time.sleep(2)

def read_mic():
    while True:
        val = int(mic.value() / 40.95 + 52)
        return val
