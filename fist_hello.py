from machine import Pin
import dht
from time import sleep
from machine import ADC

led = Pin(12,Pin.OUT)
p_dht = Pin(4,Pin.OPEN_DRAIN)
d = dht.DHT11(p_dht)
d.measure()
print("温度",d.temperature(),"℃")
print("湿度",d.humidity(),"%")
adc = ADC(0)
bat = adc.read()
bat = bat/1024*5.7
print("电压",bat,"V")
while 1:
   led.on()
   sleep(1)
   led.off()
   sleep(1)
