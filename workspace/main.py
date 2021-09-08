
def timer_task(self):
  if(wlan.isconnected()):
    #print('timer running')
    t=1
    
  else:
    machine.soft_reset()
    t=1



import os
os.dupterm(None, 1)
from machine import UART
uart = UART(0,9600)
uart.init(9600, bits=8, parity=None, stop=1, rxbuf=50)

import network
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
#wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('MYWIFI', '66668888') # connect to an AP

print('disconnect')
from machine import Timer
tim = Timer(-1)
tim.init(period=10000, mode=Timer.PERIODIC, callback=timer_task)
t=0


