import machine
from machine import RTC
import time
import json
import hashlib
import ubinascii
import pycom
from mqtt import MQTTClient
import _thread
import microphone as mic
import temphumid
import ldr

def sub_cb(topic, msg):
    if msg == b'{"Command":"Red"}': pycom.rgbled(0xff0000)
    if msg == b'{"Command":"Blue"}': pycom.rgbled(0x0004ff)
    if msg == b'{"Command":"Green"}': pycom.rgbled(0x00ff04)
    if msg == b'{"Command":"Yellow"}': pycom.rgbled(0xe5ff00)
    if msg == b'{"Command":"White"}': pycom.rgbled(0xe5ff00)
    if msg == b'{"Command":"Off"}': pycom.rgbled(0x000000)
    print((topic, msg))

with open('config.json') as f:
    config = json.load(f)

topic_pub = 'devices/loqotia-sensors'
topic_sub = 'devices/loqotia-sensors/control'
broker_url = 'devpi'
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest())

c = MQTTClient(client_name, broker_url, user = config["user_mqtt"], password = config["pass_mqtt"])
c.set_callback(sub_cb)
c.connect()
c.subscribe(topic_sub)

rtc = RTC()

def fetch_data():
    while True:
        temp, hum = temphumid.read_data()
        c.publish(topic_pub,'{"loqotia-sensor": {"Darkness":' + str(ldr.read_ldr()) +
                          ',"Temperature":'+ str(temp) +
                          ',"Humidity":' + str(hum) +
                          '}}')

        time.sleep(300)

def mic_read():
    set_rtc()
    while True:
        sound = mic.read_mic()
        if (sound <= 95 and rtc.now()[3] >= 3 and rtc.now()[3] <= 6):
            c.publish(topic_pub,'{"loqotia-alarm": {"On":' + "1" + '}}')
            print("ALARM")
            time.sleep(120)

def set_rtc():
    rtc.ntp_sync("pool.ntp.org")
    time.sleep(.5)
    correctTime = list(rtc.now())
    correctTime[3] += 2
    rtc.init(tuple(correctTime))

_thread.start_new_thread(fetch_data, ())
_thread.start_new_thread(mic_read, ())
