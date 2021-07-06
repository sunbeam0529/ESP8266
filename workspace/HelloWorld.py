from time import sleep
from machine import Pin, I2C
import sh1106
import ntptime
import network
import time
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.fill(0)
display.text('Initing....', 0, 0, 1)
display.show()
led = Pin(2,Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
display.text('connect to wifi', 0, 8, 1)
display.show()
sleep(1)
connecttime=0
while not wlan.isconnected():
  wlan.connect('Ace', '12345678')
  sleep(1)
  connecttime=connecttime+1
  display.text("%d s" % (connecttime,), 0, 16, 1)
  display.show()
if wlan.isconnected():
  display.text("%d s Connected!"%(connecttime), 0, 16, 1)
  display.show()
else :
  display.text("%d s No Network!"%(connecttime), 0, 16, 1)
  display.show()
  while 1:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
sleep(1)
display.fill(0)
display.show()

ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'
ntptime.settime()
nowtime = time.localtime()
display.text("%d.%d.%d"%nowtime[0:3], 0, 0, 1)
display.show()
while 1:
  nowtime = time.localtime()
  display.fill_rect(0,8,128,8,0)
  display.text("%d:%d:%d"%nowtime[3:6], 0, 8, 1)
  display.show()
  led.on()
  sleep(1)
  nowtime = time.localtime()
  display.fill_rect(0,8,128,8,0)
  display.text("%d:%d:%d"%nowtime[3:6], 0, 8, 1)
  display.show()
  led.off()
  sleep(1)

