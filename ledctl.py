import time
from simple import MQTTClient
from machine import Pin

led=Pin(2,Pin.OUT)

def sub_cb(topic, msg):
    print(topic, msg)
    if topic==b'ledctl':
        if msg==b'ledon':
            led.off()
        if msg==b'ledoff':
            led.on()

c = MQTTClient("umqtt_client", "test.mosquitto.org")
c.set_callback(sub_cb)
c.connect()
c.subscribe(b"ledctl")
while True:
    c.check_msg()
    if led.value()==1:
        c.publish('ledstatus','ledoff')
    if led.value()==0:
        c.publish('ledstatus','ledon')
    time.sleep(1)
