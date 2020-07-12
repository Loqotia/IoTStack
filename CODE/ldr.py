import time
import machine
from machine import Pin, ADC

adc = ADC()
ldr = adc.channel(pin='P14', attn = ADC.ATTN_11DB)
time.sleep(2)

def read_ldr():
    meanResult = 0
    for x in range (9):
        result = ldr.value() / 40.95
        meanResult += result
        time.sleep(.5)

    return (int(meanResult / 10))
